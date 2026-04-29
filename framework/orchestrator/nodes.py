"""
LangGraph node functions for generation-only pipeline.

Each node:
  1. Reads what it needs from PipelineState
  2. Instantiates the corresponding agent
  3. Runs agent logic
  4. Returns fields it produced
"""

import time
from typing import Any, Dict, List

from autospectest.framework.agents import (
    AssemblerAgent,
    NavigationAgent,
    StandardPatternsAgent,
    SummaryAgent,
    TestCaseAuditorAgent,
    TestGenerationAgent,
    WorkflowAuditorAgent,
)
from autospectest.framework.extractors import (
    ChunkerAgent,
    ParserAgent,
)
from autospectest.framework.orchestrator.state import PipelineState
from autospectest.framework.schemas.schemas import ProjectContext


def _agent_kwargs(state: PipelineState) -> dict:
    """Extract constructor kwargs shared by all agents."""
    return dict(
        api_key=state["api_key"],
        model=state["model"],
        debug=state["debug"],
        debug_file=state["debug_file"],
    )


async def parse_node(state: PipelineState) -> Dict[str, Any]:
    """Parse the raw functional description into structured data.

    All modules are parsed in parallel via ParserAgent.arun / asyncio.gather,
    cutting step-1 wall-clock time from O(N modules) to O(1) bounded by the
    LLM semaphore.
    """
    t0 = time.time()
    print("\n[1/8] Parsing functional description (parallelized)...")

    agent = ParserAgent(**_agent_kwargs(state))
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

    agent = NavigationAgent(**_agent_kwargs(state))
    nav_graph = agent.run(state["parsed_desc"])

    print(f"  - Page nodes: {len(nav_graph.nodes)}")
    print(f"  Done in {time.time() - t0:.1f}s")

    return {"nav_graph": nav_graph}


async def chunker_node(state: PipelineState) -> Dict[str, Any]:
    """Split modules into workflow chunks, then audit and (once) revise.

    All modules are processed in parallel via asyncio.gather. For each module:
      1. ChunkerAgent.arun produces an initial chunk set.
      2. WorkflowAuditorAgent.arun reviews for coverage gaps, ungrounded chunks,
         and scope leaks.
      3. On a non-clean audit, bad chunks are dropped, missing workflows are folded
         into module.workflows, and the chunker retries once with the revision hint.
    Capped at one retry per module. Concurrency is bounded by the shared LLM semaphore.
    """
    import asyncio

    t0 = time.time()
    print("\n[3/8] Splitting modules into workflow chunks (with auditor, parallelized)...")

    chunker = ChunkerAgent(**_agent_kwargs(state))
    auditor = WorkflowAuditorAgent(**_agent_kwargs(state))

    parsed_desc = state["parsed_desc"]
    project_context = ProjectContext(
        project_name=parsed_desc.project_name or "",
        navigation_overview=parsed_desc.navigation_overview or "",
    )

    async def process_module(module) -> List[Any]:
        chunks = await chunker.arun(module, project_context=project_context)
        report = await auditor.arun(module, chunks)

        if not report.is_clean():
            kept = [
                c for i, c in enumerate(chunks)
                if i not in report.ungrounded_chunk_indices
                and i not in report.scope_violations
            ]
            dropped = len(chunks) - len(kept)
            print(
                f"  - {module.title}: auditor flagged "
                f"{len(report.missing_workflows)} missing, "
                f"{len(report.ungrounded_chunk_indices)} ungrounded, "
                f"{len(report.scope_violations)} scope-leak; "
                f"dropping {dropped}, retrying chunker"
            )

            if report.missing_workflows:
                existing = {w.lower() for w in module.workflows}
                for w in report.missing_workflows:
                    if w.lower() not in existing:
                        module.workflows.append(w)
                        existing.add(w.lower())

            retry_chunks = await chunker.arun(
                module,
                project_context=project_context,
                revision_hint=report.revision_hint or None,
            )
            chunks = retry_chunks if retry_chunks else kept

        print(f"  - {module.title}: {len(chunks)} chunk(s)")
        for chunk in chunks:
            print(f"    * {chunk.workflow_name}")

        return chunks

    results = await asyncio.gather(*[process_module(m) for m in parsed_desc.modules])
    all_chunks = [c for module_chunks in results for c in module_chunks]

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


async def test_generation_worker_node(state: PipelineState) -> Dict[str, Any]:
    """Generate test cases for a SINGLE workflow chunk, then audit them.

    This node is the target of a Send-API conditional edge: one worker
    instance is fanned out per chunk and they run concurrently in the
    asyncio event loop. Each worker:

        1. Generates an initial test list for the chunk.
        2. Runs the test-case auditor over that list.
        3. Keeps "accept" tests, drops "drop" tests, and — if any "revise"
           verdicts came back — re-runs the generator once with the combined
           redaction hints, audits the retry, and unions the retry's
           accepted tests with the originals.

    Cap is one retry per worker. Downstream assembler dedup absorbs any
    overlap between original-accepted and retry-accepted tests.
    """
    chunk = state["current_chunk"]
    if chunk is None:
        return {"all_tests": []}

    ct0 = time.time()
    print(f"  - worker start: {chunk.module_title} / {chunk.workflow_name}")
    agent_kwargs = _agent_kwargs(state)
    gen_agent = TestGenerationAgent(**agent_kwargs)
    auditor = TestCaseAuditorAgent(**agent_kwargs)

    try:
        tests = await gen_agent.arun(chunk)
    except Exception as err:
        print(f"  !! worker failed for {chunk.workflow_name}: {err}")
        return {"all_tests": []}

    if not tests:
        print(
            f"  - worker done:  {chunk.module_title} / {chunk.workflow_name} "
            f"-> 0 tests in {time.time() - ct0:.1f}s"
        )
        return {"all_tests": []}

    verdicts = await auditor.arun(chunk, tests)
    accepted = [t for t, v in zip(tests, verdicts) if v.verdict == "accept"]
    revise_hints = [
        v.redaction_hint for v in verdicts
        if v.verdict == "revise" and v.redaction_hint
    ]
    dropped = sum(1 for v in verdicts if v.verdict == "drop")
    initial_count = len(tests)

    # Warn if the auditor was unusually aggressive — likely a prompt regression.
    if initial_count and (initial_count - len(accepted)) / initial_count > 0.5:
        print(
            f"  !! auditor dropped/revised >50% for '{chunk.workflow_name}' "
            f"({initial_count - len(accepted)}/{initial_count}); review prompts"
        )

    if revise_hints:
        combined_hint = "; ".join(revise_hints)
        try:
            retry_tests = await gen_agent.arun(chunk, revision_hint=combined_hint)
        except Exception as err:
            print(f"  !! worker retry failed for {chunk.workflow_name}: {err}")
            retry_tests = []

        if retry_tests:
            retry_verdicts = await auditor.arun(chunk, retry_tests)
            retry_accepted = [
                t for t, v in zip(retry_tests, retry_verdicts) if v.verdict == "accept"
            ]
            accepted = accepted + retry_accepted

    print(
        f"  - worker done:  {chunk.module_title} / {chunk.workflow_name} "
        f"-> {len(accepted)} kept (initial {initial_count}, "
        f"dropped {dropped}, revised {len(revise_hints)}) "
        f"in {time.time() - ct0:.1f}s"
    )
    return {"all_tests": accepted}


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

    from autospectest.exporters.json_exporter import export_json

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