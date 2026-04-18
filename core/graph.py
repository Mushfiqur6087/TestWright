"""
LangGraph Pipeline Definition

Builds and compiles the StateGraph that orchestrates all agents.

Graph topology - full mode (sequential)
========================================

  parse -> navigation -> chunker -> summary -> test_generation
    -> standard_patterns -> assembler -> verification_flag
    -> ideal_verification -> verification_matcher -> execution_plan
    -> finalize -> END

Graph topology - basic mode (no post-verification)
===================================================

  parse -> navigation -> chunker -> summary -> test_generation
    -> standard_patterns -> assembler -> finalize -> END

Graph topology - post_verify mode (load saved + verify only)
=============================================================

  load_assembled -> verification_flag -> ideal_verification
    -> verification_matcher -> execution_plan -> finalize -> END

All steps run sequentially to avoid LangGraph fan-in state-merge
issues that cause duplicate node executions in parallel branches.
``standard_patterns`` emits session/RBAC tests that are merged into
the spec-derived list by ``assembler_node`` before dedup.
"""

from langgraph.graph import END, StateGraph

from testwright.core.nodes import (
    assembler_node,
    chunker_node,
    execution_plan_node,
    finalize_node,
    ideal_verification_node,
    load_assembled_node,
    navigation_node,
    parse_node,
    standard_patterns_node,
    summary_node,
    test_generation_node,
    verification_flag_node,
    verification_matcher_node,
)
from testwright.core.state import PipelineState


def build_graph(mode: str = "full") -> StateGraph:
    """
    Construct and compile the LangGraph pipeline.

    Args:
        mode: ``"full"`` (default) runs all 11 nodes including post-verification
              and execution planning. ``"basic"`` stops after the assembler —
              no verification flagging, ideal verification, RAG matching, or
              execution plan nodes are run. ``"post_verify"`` skips generation
              entirely — loads a saved test-cases.json and runs only the
              verification sub-pipeline (6 nodes).

    Returns a compiled graph that can be invoked with
    ``graph.invoke(initial_state)``.
    """

    graph = StateGraph(PipelineState)

    if mode == "post_verify":
        graph.add_node("load_assembled", load_assembled_node)
        graph.add_node("verification_flag", verification_flag_node)
        graph.add_node("ideal_verification", ideal_verification_node)
        graph.add_node("verification_matcher", verification_matcher_node)
        graph.add_node("execution_plan", execution_plan_node)
        graph.add_node("finalize", finalize_node)

        graph.set_entry_point("load_assembled")
        graph.add_edge("load_assembled", "verification_flag")
        graph.add_edge("verification_flag", "ideal_verification")
        graph.add_edge("ideal_verification", "verification_matcher")
        graph.add_edge("verification_matcher", "execution_plan")
        graph.add_edge("execution_plan", "finalize")
        graph.add_edge("finalize", END)

        return graph.compile()

    # -- Register core nodes (shared by both modes) ---------------------------
    graph.add_node("parse", parse_node)
    graph.add_node("navigation", navigation_node)
    graph.add_node("chunker", chunker_node)
    graph.add_node("summary", summary_node)
    graph.add_node("test_generation", test_generation_node)
    graph.add_node("standard_patterns", standard_patterns_node)
    graph.add_node("assembler", assembler_node)
    graph.add_node("finalize", finalize_node)

    # -- Entry point ----------------------------------------------------------
    graph.set_entry_point("parse")

    # -- Core sequential pipeline (both modes) --------------------------------
    graph.add_edge("parse", "navigation")
    graph.add_edge("navigation", "chunker")
    graph.add_edge("chunker", "summary")
    graph.add_edge("summary", "test_generation")
    graph.add_edge("test_generation", "standard_patterns")
    graph.add_edge("standard_patterns", "assembler")

    if mode == "basic":
        # Skip verification nodes -- go straight to finalize
        graph.add_edge("assembler", "finalize")
    else:
        # -- Sequential verification pipeline (full mode only) ----------------
        graph.add_node("verification_flag", verification_flag_node)
        graph.add_node("ideal_verification", ideal_verification_node)
        graph.add_node("verification_matcher", verification_matcher_node)
        graph.add_node("execution_plan", execution_plan_node)

        graph.add_edge("assembler", "verification_flag")
        graph.add_edge("verification_flag", "ideal_verification")
        graph.add_edge("ideal_verification", "verification_matcher")
        graph.add_edge("verification_matcher", "execution_plan")
        graph.add_edge("execution_plan", "finalize")

    # -- End ------------------------------------------------------------------
    graph.add_edge("finalize", END)

    return graph.compile()
