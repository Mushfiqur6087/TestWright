"""
LangGraph Node Functions

Each function is a LangGraph node that:
  1. Reads what it needs from PipelineState
  2. Instantiates the appropriate agent (reusing existing agent code)
  3. Runs the agent logic
  4. Returns a partial state dict with the fields it produced
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List

from testwright.agents import (
    AssemblerAgent,
    ChunkerAgent,
    ExecutionPlanAgent,
    IdealVerificationAgent,
    NavigationAgent,
    ParserAgent,
    SummaryAgent,
    TestGenerationAgent,
    VerificationFlagAgent,
    VerificationMatcherAgent,
)
from testwright.agents.base import BaseAgent
from testwright.core.state import PipelineState


# ---------------------------------------------------------------------------
# Helper: build an agent from the config stored in state
# ---------------------------------------------------------------------------

def _agent_kwargs(state: PipelineState) -> dict:
    """Extract the common constructor kwargs every agent needs."""
    return dict(
        api_key=state["api_key"],
        model=state["model"],
        provider=state["provider"],
        debug=state["debug"],
        debug_file=state["debug_file"],
    )


# ===========================================================================
# Node 1 -- Parse functional description
# ===========================================================================

def parse_node(state: PipelineState) -> Dict[str, Any]:
    """Parse the raw functional description JSON into structured data."""
    t0 = time.time()
    print("\n[1/11] Parsing functional description...")

    agent = ParserAgent(**_agent_kwargs(state))
    parsed_desc = agent.run(state["functional_desc"])

    print(f"  - Project: {parsed_desc.project_name}")
    print(f"  - Modules found: {len(parsed_desc.modules)}")
    for m in parsed_desc.modules:
        print(f"    * {m.title}: {len(m.workflows)} workflows, {len(m.mentioned_items)} items")
    print(f"  Done in {time.time()-t0:.1f}s")

    return {"parsed_desc": parsed_desc}


# ===========================================================================
# Node 2 -- Build navigation graph
# ===========================================================================

def navigation_node(state: PipelineState) -> Dict[str, Any]:
    """Build the navigation graph from the parsed description."""
    t0 = time.time()
    print("\n[2/11] Building navigation graph...")

    agent = NavigationAgent(**_agent_kwargs(state))
    nav_graph = agent.run(state["parsed_desc"])

    print(f"  - Login module ID: {nav_graph.login_module_id}")
    print(f"  - Page nodes: {len(nav_graph.nodes)}")
    print(f"  Done in {time.time()-t0:.1f}s")

    return {"nav_graph": nav_graph}


# ===========================================================================
# Node 3 -- Chunk modules into workflows
# ===========================================================================

def chunker_node(state: PipelineState) -> Dict[str, Any]:
    """Split each module into workflow-based chunks."""
    t0 = time.time()
    print("\n[3/11] Splitting modules into workflow chunks...")

    agent = ChunkerAgent(**_agent_kwargs(state))
    all_chunks = []

    for module in state["parsed_desc"].modules:
        chunks = agent.run(module)
        all_chunks.extend(chunks)
        print(f"  - {module.title}: {len(chunks)} chunk(s)")
        for chunk in chunks:
            print(f"    * {chunk.workflow_name}")

    print(f"  Total: {len(all_chunks)} chunks | Done in {time.time()-t0:.1f}s")
    return {"all_chunks": all_chunks}


# ===========================================================================
# Node 4 -- Generate module summaries
# ===========================================================================

def summary_node(state: PipelineState) -> Dict[str, Any]:
    """Generate concise module summaries for verification matching."""
    t0 = time.time()
    print("\n[4/11] Generating module summaries...")

    agent = SummaryAgent(**_agent_kwargs(state))
    module_summaries = agent.run(state["parsed_desc"].modules)

    print(f"  - Generated summaries for {len(module_summaries)} modules")
    for ms in module_summaries.values():
        verify_str = f", can verify: {', '.join(ms.can_verify_states)}" if ms.can_verify_states else ""
        action_str = f", modifies: {', '.join(ms.action_states)}" if ms.action_states else ""
        print(f"    * {ms.module_title}{verify_str}{action_str}")
    print(f"  Done in {time.time()-t0:.1f}s")

    return {"module_summaries": module_summaries}


# ===========================================================================
# Node 5 -- Generate test cases for each chunk
# ===========================================================================

def test_generation_node(state: PipelineState) -> Dict[str, Any]:
    """Generate test cases for every workflow chunk in parallel."""
    t0 = time.time()
    chunks = state["all_chunks"]
    max_workers = min(5, len(chunks))
    print(f"\n[5/11] Generating test cases ({len(chunks)} chunks, {max_workers} parallel workers)...")

    kwargs = _agent_kwargs(state)

    def _generate(chunk, idx):
        ct0 = time.time()
        print(f"  - [{idx+1}/{len(chunks)}] Starting: {chunk.module_title} / {chunk.workflow_name}")
        agent = TestGenerationAgent(**kwargs)
        tests = agent.run(chunk)
        print(f"  - [{idx+1}/{len(chunks)}] Done: {chunk.module_title} / {chunk.workflow_name} -> {len(tests)} tests in {time.time()-ct0:.1f}s")
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
            except Exception as e:
                print(f"  !! Chunk [{idx+1}/{len(chunks)}] failed: {e}")
                results[idx] = []

    all_tests = []
    for i in range(len(chunks)):
        all_tests.extend(results.get(i, []))

    print(f"  Total: {len(all_tests)} test cases | Done in {time.time()-t0:.1f}s")
    return {"all_tests": all_tests}


# ===========================================================================
# Node 6 -- Assemble, deduplicate, assign IDs
# ===========================================================================

def assembler_node(state: PipelineState) -> Dict[str, Any]:
    """Assemble test cases -- deduplicate, sort, assign IDs, link to nav graph."""
    t0 = time.time()
    before = len(state["all_tests"])
    print(f"\n[6/11] Assembling test cases (deduplicating {before} raw tests)...")

    agent = AssemblerAgent(**_agent_kwargs(state))
    output = agent.run(
        test_cases=state["all_tests"],
        nav_graph=state["nav_graph"],
        project_name=state["parsed_desc"].project_name,
        base_url=state["parsed_desc"].base_url,
    )
    after = len(output.test_cases)
    removed = before - after
    print(f"  - {after} unique test cases ({removed} duplicates removed)")
    print(f"  Done in {time.time()-t0:.1f}s")

    output.module_summaries = state["module_summaries"]
    return {"output": output}


# ===========================================================================
# Node 7 -- Flag tests needing post-verification
# ===========================================================================

def verification_flag_node(state: PipelineState) -> Dict[str, Any]:
    """Flag positive tests that need post-verification."""
    print("\n[7/11] Flagging positive tests for post-verification...")

    agent = VerificationFlagAgent(**_agent_kwargs(state))
    flagged_tests = agent.run(
        state["output"].test_cases,
        state["module_summaries"],
    )
    flagged_count = sum(1 for tc in flagged_tests if tc.needs_post_verification)
    print(f"  - Flagged {flagged_count} positive tests as needing post-verification")

    return {"flagged_tests": flagged_tests}


# ===========================================================================
# Node 8 -- Generate ideal verification scenarios
# ===========================================================================

def ideal_verification_node(state: PipelineState) -> Dict[str, Any]:
    """Generate ideal verification scenarios for flagged tests."""
    print("\n[8/11] Generating ideal verification scenarios...")

    agent = IdealVerificationAgent(**_agent_kwargs(state))
    ideal_verifications = agent.run(
        state["flagged_tests"],
        state["module_summaries"],
    )
    total_ideals = sum(len(v) for v in ideal_verifications.values())
    print(f"  - Generated {total_ideals} ideal verification scenarios for {len(ideal_verifications)} tests")

    return {"ideal_verifications": ideal_verifications}


# ===========================================================================
# Node 9 -- Match verifications to actual test cases via RAG
# ===========================================================================

def verification_matcher_node(state: PipelineState) -> Dict[str, Any]:
    """Match ideal verifications to existing test cases using RAG search."""
    print("\n[9/11] Matching verifications with RAG...")

    agent = VerificationMatcherAgent(**_agent_kwargs(state))
    final_tests = agent.run(
        flagged_tests=state["flagged_tests"],
        ideal_verifications=state["ideal_verifications"],
        all_test_cases=state["output"].test_cases,
        module_summaries=state["module_summaries"],
        use_embeddings=True,
    )

    return {"final_tests": final_tests}


# ===========================================================================
# Node 10 -- Generate execution plans
# ===========================================================================

def execution_plan_node(state: PipelineState) -> Dict[str, Any]:
    """Compile final execution plans for all verified test cases."""
    print("\n[10/11] Generating execution plans...")

    # Update output test cases with verification data first
    output = state["output"]
    output.test_cases = state["final_tests"]

    agent = ExecutionPlanAgent(**_agent_kwargs(state))
    execution_plans = agent.run(output.test_cases)
    plan_summary = agent.generate_execution_plan_summary(execution_plans)

    print(f"  - Generated {plan_summary.get('total_plans', 0)} execution plans")
    print(f"  - Automated steps: {plan_summary.get('total_automated_steps', 0)}, Manual steps: {plan_summary.get('total_manual_steps', 0)}")
    print(f"  - Automation rate: {plan_summary.get('automation_rate', 0)}%")

    output.execution_plans = execution_plans

    return {
        "output": output,
        "execution_plans": execution_plans,
        "plan_summary": plan_summary,
    }


# ===========================================================================
# Node 11 -- Finalize: summary, graph image, validation, JSON export
# ===========================================================================

def finalize_node(state: PipelineState) -> Dict[str, Any]:
    """Generate summary, nav graph image, validate, and export JSON."""
    import os

    from testwright.exporters.json_exporter import export_json

    t0 = time.time()
    print("\n[11/11] Finalizing output...")

    output = state["output"]
    module_summaries = state["module_summaries"]
    plan_summary = state.get("plan_summary") or {}
    output_dir = state["output_dir"]

    # -- Enhanced summary -----------------------------------------------------
    summary = _generate_enhanced_summary(output.test_cases, module_summaries)
    summary["execution_plans"] = plan_summary
    output.summary = summary

    # -- Navigation graph image -----------------------------------------------
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

    # -- Validation -----------------------------------------------------------
    assembler = AssemblerAgent(**_agent_kwargs(state))
    issues = assembler.validate(output.test_cases)
    if issues:
        print(f"  - Validation issues: {len(issues)}")
        for issue in issues[:5]:
            print(f"    ! {issue}")

    # -- Export JSON -----------------------------------------------------------
    json_path = os.path.join(output_dir, "test-cases.json")
    export_json(output, json_path)
    print(f"  Output saved to: {json_path}")
    print(f"  Done in {time.time()-t0:.1f}s")

    return {"output": output}


# ---------------------------------------------------------------------------
# Helper used by finalize_node
# ---------------------------------------------------------------------------

def _generate_enhanced_summary(test_cases, module_summaries) -> dict:
    """Generate enhanced summary with verification coverage."""
    summary: Dict[str, Any] = {
        "total_tests": len(test_cases),
        "by_type": {"positive": 0, "negative": 0, "edge_case": 0},
        "by_priority": {"High": 0, "Medium": 0, "Low": 0},
        "by_module": {},
        "post_verification": {
            "tests_needing_verification": 0,
            "full_coverage": 0,
            "partial_coverage": 0,
            "no_coverage": 0,
            "coverage_gaps": [],
        },
    }

    all_gaps: set = set()

    for tc in test_cases:
        if tc.test_type in summary["by_type"]:
            summary["by_type"][tc.test_type] += 1
        if tc.priority in summary["by_priority"]:
            summary["by_priority"][tc.priority] += 1
        if tc.module_title not in summary["by_module"]:
            summary["by_module"][tc.module_title] = 0
        summary["by_module"][tc.module_title] += 1

        if tc.needs_post_verification:
            summary["post_verification"]["tests_needing_verification"] += 1
            if tc.verification_coverage == "full":
                summary["post_verification"]["full_coverage"] += 1
            elif tc.verification_coverage == "partial":
                summary["post_verification"]["partial_coverage"] += 1
            else:
                summary["post_verification"]["no_coverage"] += 1
            for gap in tc.coverage_gaps:
                all_gaps.add(gap)

    summary["post_verification"]["coverage_gaps"] = list(all_gaps)[:10]
    return summary
