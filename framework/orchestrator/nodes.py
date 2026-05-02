import asyncio
import json
import os
import time
from datetime import datetime
from typing import Any, Dict

from autospectest.framework.agents.base import BaseAgent
from autospectest.framework.agents.semantic_critic_agent import SemanticCriticAgent
from autospectest.framework.agents.ui_ast_agent import UIASTAgent
from autospectest.framework.orchestrator.state import PipelineState


def _agent_kwargs(state: PipelineState, stage_file: str) -> dict:
    debug: bool = state.get("debug", False)
    debug_dir: str = state.get("debug_dir", "")
    if debug and debug_dir:
        debug_file = os.path.join(debug_dir, stage_file)
        BaseAgent.init_debug_session(debug_file, state["model"])
    else:
        debug_file = state.get("debug_file", "debug_log.txt")
    return dict(api_key=state["api_key"], model=state["model"], debug=debug, debug_file=debug_file)


async def ui_ast_node(state: PipelineState) -> Dict[str, Any]:
    t0 = time.time()
    modules = state["functional_desc"].get("modules", [])
    print(f"\n[1/3] Generating UI-AST for {len(modules)} module(s) in parallel...")

    agent = UIASTAgent(**_agent_kwargs(state, "01_ui_ast.log"))

    results = await asyncio.gather(
        *[agent.arun(m) for m in modules],
        return_exceptions=True,
    )

    ui_ast_results = []
    for module, result in zip(modules, results):
        if isinstance(result, Exception):
            print(f"  !! Failed for {module['title']}: {result}")
            ui_ast_results.append({
                "module_id": module["id"],
                "module_title": module["title"],
                "error": str(result),
                "ast": {},
            })
        else:
            n_components = len(result.get("components", {}))
            print(f"  - {module['title']}: {n_components} component(s)")
            ui_ast_results.append({
                "module_id": module["id"],
                "module_title": module["title"],
                "ast": result,
            })

    print(f"  Done in {time.time() - t0:.1f}s")
    return {"ui_ast_results": ui_ast_results}


async def semantic_critic_node(state: PipelineState) -> Dict[str, Any]:
    t0 = time.time()
    ui_ast_results = state.get("ui_ast_results", [])
    desc_by_id = {m["id"]: m["description"] for m in state["functional_desc"].get("modules", [])}
    print(f"\n[2/3] Running Semantic Critic for {len(ui_ast_results)} module(s)...")

    agent = SemanticCriticAgent(**_agent_kwargs(state, "02_semantic_critic.log"))

    async def _audit_one(entry: Dict[str, Any]) -> Dict[str, Any]:
        if entry.get("error"):
            return {
                "module_id": entry["module_id"],
                "module_title": entry["module_title"],
                "critique": None,
                "error": f"Skipped (upstream error): {entry['error']}",
            }
        critique = await agent.arun(desc_by_id.get(entry["module_id"], ""), entry.get("ast", {}))
        return {
            "module_id": entry["module_id"],
            "module_title": entry["module_title"],
            "critique": critique,
            "error": None,
        }

    raw = await asyncio.gather(*[_audit_one(e) for e in ui_ast_results], return_exceptions=True)

    results = []
    for entry, r in zip(ui_ast_results, raw):
        if isinstance(r, Exception):
            print(f"  !! Critique failed for {entry['module_title']}: {r}")
            results.append({
                "module_id": entry["module_id"],
                "module_title": entry["module_title"],
                "critique": None,
                "error": str(r),
            })
        else:
            verdict = (r.get("critique") or {}).get("verdict", "?")
            score = (r.get("critique") or {}).get("score", 0.0)
            print(f"  - {r['module_title']}: verdict={verdict}, score={score:.2f}")
            results.append(r)

    print(f"  Done in {time.time() - t0:.1f}s")
    return {"semantic_critique_results": results}


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
    print(f"  Saved UI-AST to:  {ui_ast_path}")

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
        print(f"  Saved critique to: {critique_path}")

    print(f"  Done in {time.time() - t0:.1f}s")
    return {"output": output}
