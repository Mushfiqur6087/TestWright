import asyncio
import json
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from autospectest.framework.agents.base import BaseAgent
from autospectest.framework.agents.semantic_critic_agent import SemanticCriticAgent
from autospectest.framework.agents.test_edge_agent import TestEdgeAgent
from autospectest.framework.agents.test_negative_agent import TestNegativeAgent
from autospectest.framework.agents.test_positive_agent import TestPositiveAgent
from autospectest.framework.agents.ui_ast_agent import UIASTAgent
from autospectest.framework.orchestrator.state import PipelineState

MAX_ATTEMPTS = 3


def _agent_kwargs(state: PipelineState, stage_file: str) -> dict:
    debug: bool = state.get("debug", False)
    debug_dir: str = state.get("debug_dir", "")
    if debug and debug_dir:
        debug_file = os.path.join(debug_dir, stage_file)
        BaseAgent.init_debug_session(debug_file, state["model"])
    else:
        debug_file = state.get("debug_file", "debug_log.txt")
    return dict(api_key=state["api_key"], model=state["model"], debug=debug, debug_file=debug_file)


async def generate_and_critique_node(state: PipelineState) -> Dict[str, Any]:
    t0 = time.time()
    modules = state["functional_desc"].get("modules", [])
    desc_by_id = {m["id"]: m["description"] for m in modules}

    print(f"\n[1/3] Generating UI-AST with critic-guided retry ({len(modules)} module(s))...")

    ast_agent = UIASTAgent(**_agent_kwargs(state, "01_ui_ast.log"))
    critic_agent = SemanticCriticAgent(**_agent_kwargs(state, "02_semantic_critic.log"))

    async def _process_module(module: Dict[str, Any]) -> Dict[str, Any]:
        desc = desc_by_id.get(module["id"], "")
        fixes: List[str] = []
        ast: Dict[str, Any] = {}
        critique: Dict[str, Any] = {}

        for attempt in range(MAX_ATTEMPTS):
            label = f"attempt {attempt + 1}/{MAX_ATTEMPTS}"

            ast = await ast_agent.arun(module, fixes=fixes if fixes else None)

            critique = await critic_agent.arun(desc, ast)
            verdict = critique.get("verdict", "retry")

            if verdict == "yes":
                n = len(ast.get("components", {}))
                print(f"  OK {module['title']} | {label} | {n} component(s)")
                return {"ast": ast, "critique": critique, "attempts": attempt + 1}

            fixes = critique.get("fixes", [])
            missing = len(critique.get("missing", []))
            phantoms = len(critique.get("phantoms", []))

            if attempt < MAX_ATTEMPTS - 1:
                print(
                    f"  ~~ {module['title']} | {label} | verdict=retry"
                    f" | missing={missing} phantoms={phantoms} | retrying..."
                )
            else:
                print(
                    f"  !! {module['title']} | max attempts reached"
                    f" | missing={missing} phantoms={phantoms} | shipping final attempt"
                )

        return {"ast": ast, "critique": critique, "attempts": MAX_ATTEMPTS, "forced_ship": True}

    raw = await asyncio.gather(*[_process_module(m) for m in modules], return_exceptions=True)

    ui_ast_results = []
    semantic_critique_results = []

    for module, r in zip(modules, raw):
        if isinstance(r, Exception):
            print(f"  !! Failed for {module['title']}: {r}")
            ui_ast_results.append({
                "module_id": module["id"],
                "module_title": module["title"],
                "error": str(r),
                "ast": {},
            })
            semantic_critique_results.append({
                "module_id": module["id"],
                "module_title": module["title"],
                "critique": None,
                "error": str(r),
            })
        else:
            ui_ast_results.append({
                "module_id": module["id"],
                "module_title": module["title"],
                "ast": r["ast"],
                "attempts": r["attempts"],
            })
            semantic_critique_results.append({
                "module_id": module["id"],
                "module_title": module["title"],
                "critique": r["critique"],
                "forced_ship": r.get("forced_ship", False),
            })

    print(f"  Done in {time.time() - t0:.1f}s")
    return {
        "ui_ast_results": ui_ast_results,
        "semantic_critique_results": semantic_critique_results,
    }


async def generate_tests_node(state: PipelineState) -> Dict[str, Any]:
    t0 = time.time()
    modules = state["functional_desc"].get("modules", [])
    ui_ast_results = state.get("ui_ast_results", [])

    ast_by_id = {r["module_id"]: r.get("ast", {}) for r in ui_ast_results}
    desc_by_id = {m["id"]: m["description"] for m in modules}

    # Skip modules that failed AST generation (empty ast)
    runnable = [m for m in modules if ast_by_id.get(m["id"])]
    skipped = len(modules) - len(runnable)

    total_calls = len(runnable) * 3
    print(f"\n[2/3] Generating test cases ({total_calls} calls across {len(runnable)} module(s))...")
    if skipped:
        print(f"  Skipping {skipped} module(s) with no AST.")

    pos_agent = TestPositiveAgent(**_agent_kwargs(state, "03_test_positive.log"))
    neg_agent = TestNegativeAgent(**_agent_kwargs(state, "04_test_negative.log"))
    edge_agent = TestEdgeAgent(**_agent_kwargs(state, "05_test_edge.log"))

    async def _process_module(module: Dict[str, Any]) -> Dict[str, Any]:
        title = module["title"]
        ast = ast_by_id[module["id"]]
        desc = desc_by_id.get(module["id"], "")

        pos, neg, edge = await asyncio.gather(
            pos_agent.arun(title, ast, desc),
            neg_agent.arun(title, ast, desc),
            edge_agent.arun(title, ast, desc),
            return_exceptions=True,
        )

        merged = _merge_module_tests(title, pos, neg, edge)
        total = merged["summary"]["total"]
        print(f"  OK {title} | {total} test(s) (pos={merged['summary']['positive']} neg={merged['summary']['negative']} edge={merged['summary']['boundary'] + merged['summary']['edge']})")
        return merged

    raw = await asyncio.gather(*[_process_module(m) for m in runnable], return_exceptions=True)

    test_results = []
    for module, r in zip(runnable, raw):
        if isinstance(r, Exception):
            print(f"  !! Failed for {module['title']}: {r}")
            test_results.append({
                "module": module["title"],
                "error": str(r),
                "test_cases": [],
                "summary": {"total": 0, "positive": 0, "negative": 0, "boundary": 0, "edge": 0,
                            "high_priority": 0, "medium_priority": 0, "low_priority": 0},
            })
        else:
            test_results.append(r)

    print(f"  Done in {time.time() - t0:.1f}s")
    return {"test_results": test_results}


def _merge_module_tests(
    module_title: str,
    positive: Any,
    negative: Any,
    edge: Any,
) -> Dict[str, Any]:
    def _safe_cases(result: Any, category: str) -> List[Dict[str, Any]]:
        if isinstance(result, Exception) or not isinstance(result, dict):
            return []
        cases = result.get("test_cases", [])
        for c in cases:
            c["category"] = category
        return cases

    pos_cases = _safe_cases(positive, "positive")
    neg_cases = _safe_cases(negative, "negative")
    edge_cases = _safe_cases(edge, "edge")
    all_cases = pos_cases + neg_cases + edge_cases

    # Renumber TCs sequentially across all categories
    for i, tc in enumerate(all_cases, 1):
        tc["tc_id"] = f"TC-{i:03d}"

    def _count(cases: List, priority: str) -> int:
        return sum(1 for c in cases if c.get("priority") == priority)

    edge_summary = edge.get("summary", {}) if isinstance(edge, dict) else {}

    return {
        "module": module_title,
        "test_cases": all_cases,
        "summary": {
            "total": len(all_cases),
            "positive": len(pos_cases),
            "negative": len(neg_cases),
            "boundary": edge_summary.get("boundary", 0),
            "edge": edge_summary.get("edge", 0),
            "high_priority": _count(all_cases, "high"),
            "medium_priority": _count(all_cases, "medium"),
            "low_priority": _count(all_cases, "low"),
        },
    }


def finalize_node(state: PipelineState) -> Dict[str, Any]:
    t0 = time.time()
    print("\n[3/3] Saving output...")

    output_dir = state["output_dir"]
    functional_desc = state["functional_desc"]

    output = {
        "project_name": functional_desc.get("project_name", ""),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "modules": state.get("ui_ast_results", []),
    }

    ui_ast_path = os.path.join(output_dir, "ui-ast.json")
    with open(ui_ast_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"  Saved UI-AST to:       {ui_ast_path}")

    ui_ast_md_path = os.path.join(output_dir, "ui-ast.md")
    with open(ui_ast_md_path, "w", encoding="utf-8") as f:
        f.write(_render_ui_ast_md(output))
    print(f"  Saved UI-AST (md):     {ui_ast_md_path}")

    critique_results = state.get("semantic_critique_results")
    if critique_results is not None:
        critique_output = {
            "project_name": functional_desc.get("project_name", ""),
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "modules": critique_results,
        }
        critique_path = os.path.join(output_dir, "semantic-critique.json")
        with open(critique_path, "w", encoding="utf-8") as f:
            json.dump(critique_output, f, indent=2)
        print(f"  Saved critique to:     {critique_path}")

        critique_md_path = os.path.join(output_dir, "semantic-critique.md")
        with open(critique_md_path, "w", encoding="utf-8") as f:
            f.write(_render_critique_md(critique_output))
        print(f"  Saved critique (md):   {critique_md_path}")

    test_results = state.get("test_results")
    if test_results is not None:
        total_tests = sum(r.get("summary", {}).get("total", 0) for r in test_results)
        tests_output = {
            "project_name": functional_desc.get("project_name", ""),
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "model": state.get("model", ""),
            "modules": test_results,
            "total_summary": {
                "total_modules": len(test_results),
                "total_tests": total_tests,
                "positive": sum(r.get("summary", {}).get("positive", 0) for r in test_results),
                "negative": sum(r.get("summary", {}).get("negative", 0) for r in test_results),
                "boundary": sum(r.get("summary", {}).get("boundary", 0) for r in test_results),
                "edge": sum(r.get("summary", {}).get("edge", 0) for r in test_results),
                "high_priority": sum(r.get("summary", {}).get("high_priority", 0) for r in test_results),
                "medium_priority": sum(r.get("summary", {}).get("medium_priority", 0) for r in test_results),
                "low_priority": sum(r.get("summary", {}).get("low_priority", 0) for r in test_results),
            },
        }
        tests_path = os.path.join(output_dir, "test-cases.json")
        with open(tests_path, "w", encoding="utf-8") as f:
            json.dump(tests_output, f, indent=2)
        print(f"  Saved test cases to:   {tests_path}  ({total_tests} total)")

        tests_md_path = os.path.join(output_dir, "test-cases.md")
        with open(tests_md_path, "w", encoding="utf-8") as f:
            f.write(_render_test_cases_md(tests_output))
        print(f"  Saved test cases (md): {tests_md_path}")

    print(f"  Done in {time.time() - t0:.1f}s")
    return {"output": output}


# ---------------------------------------------------------------------------
# Markdown renderers
# ---------------------------------------------------------------------------

def _md_escape(text: str) -> str:
    """Escape pipe characters and collapse newlines for markdown table cells."""
    if not isinstance(text, str):
        text = str(text)
    return text.replace("|", "\\|").replace("\n", " ")


def _render_ui_ast_md(data: dict) -> str:
    lines = []
    lines.append(f"# UI-AST — {data.get('project_name', '')}")
    lines.append("")
    lines.append(f"Generated: {data.get('generated_at', '')}")
    lines.append("")

    for module in data.get("modules", []):
        title = module.get("module_title", "Unknown")
        attempts = module.get("attempts")
        error = module.get("error")

        lines.append(f"## {title}")
        lines.append("")

        if error:
            lines.append(f"> **Error:** {error}")
            lines.append("")
            continue

        if attempts is not None:
            lines.append(f"Attempts: {attempts}")
            lines.append("")

        ast = module.get("ast", {})
        if not ast:
            lines.append("*(no AST generated)*")
            lines.append("")
            continue

        lines.append("```json")
        lines.append(json.dumps(ast, indent=2))
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


def _render_critique_md(data: dict) -> str:
    lines = []
    lines.append(f"# Semantic Critique — {data.get('project_name', '')}")
    lines.append("")
    lines.append(f"Generated: {data.get('generated_at', '')}")
    lines.append("")

    for module in data.get("modules", []):
        title = module.get("module_title", "Unknown")
        lines.append(f"## {title}")
        lines.append("")

        error = module.get("error")
        if error:
            lines.append(f"> **Error:** {error}")
            lines.append("")
            continue

        critique = module.get("critique") or {}
        forced = module.get("forced_ship", False)

        verdict = critique.get("verdict", "—")
        verdict_label = "yes" if verdict == "yes" else "retry (forced ship)" if forced else "retry"
        lines.append(f"**Verdict:** {verdict_label}  ")
        lines.append(f"**Forced ship:** {'yes' if forced else 'no'}  ")
        lines.append("")

        summary = critique.get("summary", "")
        if summary:
            lines.append(f"{summary}")
            lines.append("")

        missing = critique.get("missing", [])
        if missing:
            lines.append("**Missing:**")
            lines.append("")
            for item in missing:
                lines.append(f"- {item}")
            lines.append("")
        else:
            lines.append("**Missing:** none")
            lines.append("")

        phantoms = critique.get("phantoms", [])
        if phantoms:
            lines.append("**Phantoms (hallucinations):**")
            lines.append("")
            for item in phantoms:
                lines.append(f"- {item}")
            lines.append("")
        else:
            lines.append("**Phantoms:** none")
            lines.append("")

        fixes = critique.get("fixes", [])
        if fixes:
            lines.append("**Fixes applied:**")
            lines.append("")
            for fix in fixes:
                lines.append(f"- {fix}")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def _render_test_cases_md(data: dict) -> str:
    lines = []
    lines.append(f"# Test Cases — {data.get('project_name', '')}")
    lines.append("")
    lines.append(f"Generated: {data.get('generated_at', '')}  ")
    lines.append(f"Model: {data.get('model', '')}  ")
    lines.append("")

    total = data.get("total_summary", {})
    if total:
        lines.append("## Summary")
        lines.append("")
        lines.append("| Modules | Total | Positive | Negative | Edge | High | Medium | Low |")
        lines.append("|---------|-------|----------|----------|------|------|--------|-----|")
        edge_total = total.get("boundary", 0) + total.get("edge", 0)
        lines.append(
            f"| {total.get('total_modules', 0)}"
            f" | {total.get('total_tests', 0)}"
            f" | {total.get('positive', 0)}"
            f" | {total.get('negative', 0)}"
            f" | {edge_total}"
            f" | {total.get('high_priority', 0)}"
            f" | {total.get('medium_priority', 0)}"
            f" | {total.get('low_priority', 0)} |"
        )
        lines.append("")

    _CATEGORY_ORDER = [("positive", "Positive Tests"), ("negative", "Negative Tests"), ("edge", "Edge & Boundary Tests")]

    for module in data.get("modules", []):
        module_name = module.get("module", "Unknown")
        lines.append(f"## {module_name}")
        lines.append("")

        error = module.get("error")
        if error:
            lines.append(f"> **Error:** {error}")
            lines.append("")
            continue

        summary = module.get("summary", {})
        if summary:
            edge_total = summary.get("boundary", 0) + summary.get("edge", 0)
            lines.append(
                f"Total: **{summary.get('total', 0)}** "
                f"(positive: {summary.get('positive', 0)}, "
                f"negative: {summary.get('negative', 0)}, "
                f"edge: {edge_total})"
            )
            lines.append("")

        all_cases = module.get("test_cases", [])
        by_category: Dict[str, List] = {"positive": [], "negative": [], "edge": []}
        for tc in all_cases:
            cat = tc.get("category", "edge")
            by_category.setdefault(cat, []).append(tc)

        for cat_key, cat_label in _CATEGORY_ORDER:
            cases = by_category.get(cat_key, [])
            if not cases:
                continue

            lines.append(f"### {cat_label}")
            lines.append("")
            lines.append("| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |")
            lines.append("|-------|-----------|---------------|-------|-----------------|----------|")

            for tc in cases:
                tc_id = tc.get("tc_id", "")
                name = _md_escape(tc.get("test_case", ""))
                preconds = tc.get("preconditions", [])
                preconds_str = _md_escape(", ".join(preconds) if isinstance(preconds, list) else str(preconds))
                steps = tc.get("steps", [])
                steps_str = _md_escape(" → ".join(steps) if isinstance(steps, list) else str(steps))
                expected = _md_escape(tc.get("expected_result", ""))
                priority = tc.get("priority", "")
                subcategory = tc.get("subcategory", "")
                tc_id_cell = f"{tc_id} ({subcategory})" if subcategory else tc_id

                lines.append(f"| {tc_id_cell} | {name} | {preconds_str} | {steps_str} | {expected} | {priority} |")

            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)
