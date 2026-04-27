"""
LangGraph node functions for generation-only pipeline.

Each node:
  1. Reads what it needs from PipelineState
  2. Instantiates the corresponding agent
  3. Runs agent logic
  4. Returns fields it produced
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List

from testwright.agents import (
    AssemblerAgent,
    ChunkerAgent,
    NavigationAgent,
    ParserAgent,
    StandardPatternsAgent,
    SummaryAgent,
    TestGenerationAgent,
)
from testwright.core.state import PipelineState
from testwright.models.schemas import ProjectContext


def _agent_kwargs(state: PipelineState) -> dict:
    """Extract constructor kwargs shared by all agents."""
    return dict(
        api_key=state["api_key"],
        model=state["model"],
        provider=state["provider"],
        debug=state["debug"],
        debug_file=state["debug_file"],
    )


def parse_node(state: PipelineState) -> Dict[str, Any]:
    """Parse the raw functional description into structured data."""
    t0 = time.time()
    print("\n[1/8] Parsing functional description...")

    agent = ParserAgent(**_agent_kwargs(state))
    parsed_desc = agent.run(state["functional_desc"])

    print(f"  - Project: {parsed_desc.project_name}")
    print(f"  - Modules found: {len(parsed_desc.modules)}")
    for module in parsed_desc.modules:
        print(f"    * {module.title}: {len(module.workflows)} workflows, {len(module.mentioned_items)} items")
    print(f"  Done in {time.time() - t0:.1f}s")

    return {"parsed_desc": parsed_desc}


def navigation_node(state: PipelineState) -> Dict[str, Any]:
    """Build navigation graph from parsed description."""
    t0 = time.time()
    print("\n[2/8] Building navigation graph...")

    agent = NavigationAgent(**_agent_kwargs(state))
    nav_graph = agent.run(state["parsed_desc"])

    print(f"  - Page nodes: {len(nav_graph.nodes)}")
    print(f"  Done in {time.time() - t0:.1f}s")

    return {"nav_graph": nav_graph}


def chunker_node(state: PipelineState) -> Dict[str, Any]:
    """Split modules into workflow chunks."""
    t0 = time.time()
    print("\n[3/8] Splitting modules into workflow chunks...")

    agent = ChunkerAgent(**_agent_kwargs(state))
    all_chunks = []

    parsed_desc = state["parsed_desc"]
    project_context = ProjectContext(
        project_name=parsed_desc.project_name or "",
        navigation_overview=parsed_desc.navigation_overview or "",
    )

    for module in parsed_desc.modules:
        chunks = agent.run(module, project_context=project_context)
        all_chunks.extend(chunks)
        print(f"  - {module.title}: {len(chunks)} chunk(s)")
        for chunk in chunks:
            print(f"    * {chunk.workflow_name}")

    print(f"  Total: {len(all_chunks)} chunks | Done in {time.time() - t0:.1f}s")
    return {"all_chunks": all_chunks}


def summary_node(state: PipelineState) -> Dict[str, Any]:
    """Generate concise summaries for each module."""
    t0 = time.time()
    print("\n[4/8] Generating module summaries...")

    agent = SummaryAgent(**_agent_kwargs(state))
    module_summaries = agent.run(state["parsed_desc"].modules)

    print(f"  - Generated summaries for {len(module_summaries)} modules")
    for module_summary in module_summaries.values():
        print(f"    * {module_summary.module_title}")
    print(f"  Done in {time.time() - t0:.1f}s")

    return {"module_summaries": module_summaries}


def test_generation_node(state: PipelineState) -> Dict[str, Any]:
    """Generate test cases for workflow chunks in parallel."""
    t0 = time.time()
    chunks = state["all_chunks"]
    max_workers = min(5, len(chunks))
    print(f"\n[5/8] Generating test cases ({len(chunks)} chunks, {max_workers} parallel workers)...")

    kwargs = _agent_kwargs(state)

    def _generate(chunk, idx):
        ct0 = time.time()
        print(f"  - [{idx + 1}/{len(chunks)}] Starting: {chunk.module_title} / {chunk.workflow_name}")
        agent = TestGenerationAgent(**kwargs)
        tests = agent.run(chunk)
        print(
            f"  - [{idx + 1}/{len(chunks)}] Done: {chunk.module_title} / {chunk.workflow_name} "
            f"-> {len(tests)} tests in {time.time() - ct0:.1f}s"
        )
        return tests

    results: Dict[int, List] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(_generate, chunk, i): i
            for i, chunk in enumerate(chunks)
        }
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                results[idx] = future.result()
            except Exception as err:
                print(f"  !! Chunk [{idx + 1}/{len(chunks)}] failed: {err}")
                results[idx] = []

    all_tests = []
    for idx in range(len(chunks)):
        all_tests.extend(results.get(idx, []))

    print(f"  Total: {len(all_tests)} test cases | Done in {time.time() - t0:.1f}s")
    return {"all_tests": all_tests}


def standard_patterns_node(state: PipelineState) -> Dict[str, Any]:
    """Generate standard quality tests (session security + RBAC)."""
    t0 = time.time()
    print("\n[6/8] Generating standard quality patterns...")

    parsed_desc = state["parsed_desc"]
    project_context = ProjectContext(
        project_name=parsed_desc.project_name or "",
        navigation_overview=parsed_desc.navigation_overview or "",
    )

    agent = StandardPatternsAgent(**_agent_kwargs(state))
    std_tests = agent.run(
        parsed_desc=parsed_desc,
        nav_graph=state["nav_graph"],
        project_context=project_context,
    )
    print(f"  - {len(std_tests)} standard pattern tests | Done in {time.time() - t0:.1f}s")
    return {"standard_pattern_tests": std_tests}


def assembler_node(state: PipelineState) -> Dict[str, Any]:
    """Assemble, deduplicate, sort, and ID test cases."""
    t0 = time.time()
    spec_tests = state.get("all_tests") or []
    std_tests = state.get("standard_pattern_tests") or []
    combined = list(spec_tests) + list(std_tests)
    before = len(combined)
    print(
        f"\n[7/8] Assembling test cases "
        f"({len(spec_tests)} spec + {len(std_tests)} standard = {before} raw)..."
    )

    agent = AssemblerAgent(**_agent_kwargs(state))
    output = agent.run(
        test_cases=combined,
        nav_graph=state["nav_graph"],
        project_name=state["parsed_desc"].project_name,
        base_url=state["parsed_desc"].base_url,
    )
    after = len(output.test_cases)
    removed = before - after
    print(f"  - {after} unique test cases ({removed} duplicates removed)")
    print(f"  Done in {time.time() - t0:.1f}s")

    output.module_summaries = state["module_summaries"]
    output.navigation_overview = state["parsed_desc"].navigation_overview or ""
    return {"output": output}


def finalize_node(state: PipelineState) -> Dict[str, Any]:
    """Generate summary, graph image, validate, and export JSON."""
    import os

    from testwright.exporters.json_exporter import export_json

    t0 = time.time()
    print("\n[8/8] Finalizing output...")

    output = state["output"]
    output_dir = state["output_dir"]

    summary = _generate_summary(output.test_cases)
    output.summary = summary

    print("  Generating navigation graph image...")
    nav_agent = NavigationAgent(**_agent_kwargs(state))
    graph_image_path = os.path.join(output_dir, "navigation_graph.png")
    generated_path = nav_agent.generate_graph_image(
        nav_graph=output.navigation_graph,
        output_path=graph_image_path,
        title=f"{output.project_name} - Navigation Graph",
    )
    if generated_path:
        output.navigation_graph.graph_image_path = generated_path
        print(f"  - Graph image saved to: {generated_path}")
    else:
        print("  - Graph image generation skipped")

    assembler = AssemblerAgent(**_agent_kwargs(state))
    issues = assembler.validate(output.test_cases)
    if issues:
        print(f"  - Validation issues: {len(issues)}")
        for issue in issues[:5]:
            print(f"    ! {issue}")

    json_path = os.path.join(output_dir, "test-cases.json")
    export_json(output, json_path)
    print(f"  Output saved to: {json_path}")
    print(f"  Done in {time.time() - t0:.1f}s")

    return {"output": output}


def _generate_summary(test_cases) -> dict:
    """Generate summary for test case counts."""
    summary: Dict[str, Any] = {
        "total_tests": len(test_cases),
        "by_type": {"positive": 0, "negative": 0, "edge_case": 0},
        "by_priority": {"High": 0, "Medium": 0, "Low": 0},
        "by_module": {},
    }

    for test_case in test_cases:
        if test_case.test_type in summary["by_type"]:
            summary["by_type"][test_case.test_type] += 1
        if test_case.priority in summary["by_priority"]:
            summary["by_priority"][test_case.priority] += 1
        if test_case.module_title not in summary["by_module"]:
            summary["by_module"][test_case.module_title] = 0
        summary["by_module"][test_case.module_title] += 1

    return summary