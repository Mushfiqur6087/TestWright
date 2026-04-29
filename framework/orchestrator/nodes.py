"""
LangGraph node functions for generation-only pipeline.

Each node:
  1. Reads what it needs from PipelineState
  2. Instantiates the corresponding agent
  3. Runs agent logic
  4. Returns fields it produced
"""

import asyncio
import os
import time
from typing import Any, Dict, List

from autospectest.framework.agents import (
    AssemblerAgent,
    NavigationAgent,
    StandardPatternsAgent,
    SummaryAgent,
    TestGenerationAgent,
)
from autospectest.framework.agents.base import BaseAgent
from autospectest.framework.extractors import (
    ChunkerAgent,
    ParserAgent,
)
from autospectest.framework.orchestrator.state import PipelineState
from autospectest.framework.schemas.schemas import ProjectContext, WorkflowChunk


def _agent_kwargs(state: PipelineState, stage_file: str) -> dict:
    """Return constructor kwargs for an agent, routing debug output to stage_file.

    When debug_dir is set (--debug mode), each pipeline stage writes to its own
    log file inside <output_dir>/debug/. The header is written once per file via
    init_debug_session (subsequent calls for the same path are no-ops).
    """
    debug: bool = state.get("debug", False)
    debug_dir: str = state.get("debug_dir", "")
    if debug and debug_dir:
        debug_file = os.path.join(debug_dir, stage_file)
        BaseAgent.init_debug_session(debug_file, state["model"])
    else:
        debug_file = state.get("debug_file", "debug_log.txt")
    return dict(
        api_key=state["api_key"],
        model=state["model"],
        debug=debug,
        debug_file=debug_file,
    )


async def parse_node(state: PipelineState) -> Dict[str, Any]:
    """Parse the raw functional description into structured data (parallel per module)."""
    t0 = time.time()
    print("\n[1/8] Parsing functional description (parallel)...")

    agent = ParserAgent(**_agent_kwargs(state, "01_parse.log"))
    parsed_desc = await agent.arun(state["functional_desc"])

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

    agent = NavigationAgent(**_agent_kwargs(state, "02_navigation.log"))
    nav_graph = agent.run(state["parsed_desc"])

    print(f"  - Page nodes: {len(nav_graph.nodes)}")
    print(f"  Done in {time.time() - t0:.1f}s")

    return {"nav_graph": nav_graph}


async def chunker_node(state: PipelineState) -> Dict[str, Any]:
    """Split modules into workflow chunks (parallel per module)."""
    t0 = time.time()
    print("\n[3/8] Splitting modules into workflow chunks (parallel)...")

    agent = ChunkerAgent(**_agent_kwargs(state, "03_chunker.log"))

    parsed_desc = state["parsed_desc"]
    project_context = ProjectContext(
        project_name=parsed_desc.project_name or "",
        navigation_overview=parsed_desc.navigation_overview or "",
    )

    results = await asyncio.gather(
        *[agent.arun(m, project_context=project_context) for m in parsed_desc.modules],
        return_exceptions=True,
    )

    all_chunks = []
    for module, result in zip(parsed_desc.modules, results):
        if isinstance(result, Exception):
            print(f"  !! chunker failed for {module.title}: {result}, using fallback")
            all_chunks.append(WorkflowChunk(
                chunk_id=f"{module.id}_full",
                module_id=module.id,
                module_title=module.title,
                workflow_name="Main workflow",
                workflow_description=module.raw_description[:200] if module.raw_description else "",
                related_items=module.mentioned_items,
                related_rules=module.business_rules,
                related_behaviors=module.expected_behaviors,
                project_context=project_context,
            ))
        else:
            all_chunks.extend(result)
            print(f"  - {module.title}: {len(result)} chunk(s)")
            for chunk in result:
                print(f"    * {chunk.workflow_name}")

    print(f"  Total: {len(all_chunks)} chunks | Done in {time.time() - t0:.1f}s")
    return {"all_chunks": all_chunks}


def summary_node(state: PipelineState) -> Dict[str, Any]:
    """Generate concise summaries for each module."""
    t0 = time.time()
    print("\n[4/8] Generating module summaries...")

    agent = SummaryAgent(**_agent_kwargs(state, "04_summary.log"))
    module_summaries = agent.run(state["parsed_desc"].modules)

    print(f"  - Generated summaries for {len(module_summaries)} modules")
    for module_summary in module_summaries.values():
        print(f"    * {module_summary.module_title}")
    print(f"  Done in {time.time() - t0:.1f}s")

    return {"module_summaries": module_summaries}


async def test_generation_worker_node(state: PipelineState) -> Dict[str, Any]:
    """Generate test cases for a SINGLE workflow chunk.

    This node is the target of a Send-API conditional edge: one worker
    instance is fanned out per chunk and they run concurrently in the
    asyncio event loop. Each worker reads its assigned chunk from
    ``state["current_chunk"]`` and returns its result list under
    ``all_tests``, where the additive reducer concatenates across workers.
    """
    chunk = state["current_chunk"]
    if chunk is None:
        return {"all_tests": []}

    ct0 = time.time()
    print(f"  - worker start: {chunk.module_title} / {chunk.workflow_name}")
    agent = TestGenerationAgent(**_agent_kwargs(state, "05_test_generation.log"))
    try:
        tests = await agent.arun(chunk)
    except Exception as err:
        print(f"  !! worker failed for {chunk.workflow_name}: {err}")
        tests = []
    print(
        f"  - worker done:  {chunk.module_title} / {chunk.workflow_name} "
        f"-> {len(tests)} tests in {time.time() - ct0:.1f}s"
    )
    return {"all_tests": tests}


def test_generation_announce_node(state: PipelineState) -> Dict[str, Any]:
    """Trivial pass-through that prints a banner before the Send fan-out.

    LangGraph requires a node from which a conditional edge originates;
    putting the print here keeps the user-visible progress log intact
    without coupling it to the summary node.
    """
    chunks = state.get("all_chunks") or []
    print(f"\n[5/8] Generating test cases ({len(chunks)} chunks, fanned out via Send API)...")
    return {}


def standard_patterns_node(state: PipelineState) -> Dict[str, Any]:
    """Generate standard quality tests (session security + RBAC)."""
    t0 = time.time()
    print("\n[6/8] Generating standard quality patterns...")

    parsed_desc = state["parsed_desc"]
    project_context = ProjectContext(
        project_name=parsed_desc.project_name or "",
        navigation_overview=parsed_desc.navigation_overview or "",
    )

    agent = StandardPatternsAgent(**_agent_kwargs(state, "06_standard_patterns.log"))
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

    agent = AssemblerAgent(**_agent_kwargs(state, "07_assembler.log"))
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
    from autospectest.exporters.json_exporter import export_json

    t0 = time.time()
    print("\n[8/8] Finalizing output...")

    output = state["output"]
    output_dir = state["output_dir"]

    summary = _generate_summary(output.test_cases)
    output.summary = summary

    print("  Generating navigation graph image...")
    nav_agent = NavigationAgent(**_agent_kwargs(state, "08_finalize.log"))
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

    assembler = AssemblerAgent(**_agent_kwargs(state, "08_finalize.log"))
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