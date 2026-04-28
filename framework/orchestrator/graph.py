"""LangGraph pipeline definition for test generation."""

from langgraph.graph import END, StateGraph

from autospectest.framework.orchestrator.nodes import (
    assembler_node,
    chunker_node,
    finalize_node,
    navigation_node,
    parse_node,
    standard_patterns_node,
    summary_node,
    test_generation_node,
)
from autospectest.framework.orchestrator.state import PipelineState


def build_graph() -> StateGraph:
    """
    Construct and compile the generation-only LangGraph pipeline.

    Returns a compiled graph that can be invoked with
    ``graph.invoke(initial_state)``.
    """

    graph = StateGraph(PipelineState)

    # -- Register core nodes --------------------------------------------------
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

    # -- Core sequential pipeline ---------------------------------------------
    graph.add_edge("parse", "navigation")
    graph.add_edge("navigation", "chunker")
    graph.add_edge("chunker", "summary")
    graph.add_edge("summary", "test_generation")
    graph.add_edge("test_generation", "standard_patterns")
    graph.add_edge("standard_patterns", "assembler")
    graph.add_edge("assembler", "finalize")

    # -- End ------------------------------------------------------------------
    graph.add_edge("finalize", END)

    return graph.compile()
