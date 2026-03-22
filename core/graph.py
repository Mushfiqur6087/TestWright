"""
LangGraph Pipeline Definition

Builds and compiles the StateGraph that orchestrates all agents.

Graph topology (sequential)
===========================

  parse -> navigation -> chunker -> summary -> test_generation
    -> assembler -> verification_flag -> ideal_verification
    -> verification_matcher -> execution_plan -> finalize -> END

All steps run sequentially to avoid LangGraph fan-in state-merge
issues that cause duplicate node executions in parallel branches.
"""

from langgraph.graph import END, StateGraph

from testwright.core.nodes import (
    assembler_node,
    chunker_node,
    execution_plan_node,
    finalize_node,
    ideal_verification_node,
    navigation_node,
    parse_node,
    summary_node,
    test_generation_node,
    verification_flag_node,
    verification_matcher_node,
)
from testwright.core.state import PipelineState


def build_graph() -> StateGraph:
    """
    Construct and compile the LangGraph pipeline.

    Returns a compiled graph that can be invoked with
    ``graph.invoke(initial_state)``.
    """

    graph = StateGraph(PipelineState)

    # -- Register nodes -------------------------------------------------------
    graph.add_node("parse", parse_node)
    graph.add_node("navigation", navigation_node)
    graph.add_node("chunker", chunker_node)
    graph.add_node("summary", summary_node)
    graph.add_node("test_generation", test_generation_node)
    graph.add_node("assembler", assembler_node)
    graph.add_node("verification_flag", verification_flag_node)
    graph.add_node("ideal_verification", ideal_verification_node)
    graph.add_node("verification_matcher", verification_matcher_node)
    graph.add_node("execution_plan", execution_plan_node)
    graph.add_node("finalize", finalize_node)

    # -- Entry point ----------------------------------------------------------
    graph.set_entry_point("parse")

    # -- Sequential pipeline --------------------------------------------------
    graph.add_edge("parse", "navigation")
    graph.add_edge("navigation", "chunker")
    graph.add_edge("chunker", "summary")
    graph.add_edge("summary", "test_generation")
    graph.add_edge("test_generation", "assembler")

    # -- Sequential verification pipeline -------------------------------------
    graph.add_edge("assembler", "verification_flag")
    graph.add_edge("verification_flag", "ideal_verification")
    graph.add_edge("ideal_verification", "verification_matcher")
    graph.add_edge("verification_matcher", "execution_plan")
    graph.add_edge("execution_plan", "finalize")

    # -- End ------------------------------------------------------------------
    graph.add_edge("finalize", END)

    return graph.compile()
