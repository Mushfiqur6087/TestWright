"""LangGraph pipeline definition for test generation."""

from typing import List, Optional

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.constants import Send
from langgraph.graph import END, StateGraph

from autospectest.framework.orchestrator.nodes import (
    assembler_node,
    chunker_node,
    finalize_node,
    navigation_node,
    parse_node,
    standard_patterns_node,
    summary_node,
    test_generation_announce_node,
    test_generation_worker_node,
)
from autospectest.framework.orchestrator.state import PipelineState


def _fan_out_test_generation(state: PipelineState) -> List[Send]:
    """Conditional edge router that emits one Send per chunk.

    Each Send dispatches a ``test_generation_worker`` invocation with the
    chunk pinned in ``current_chunk``. Workers run concurrently inside
    ``ainvoke`` and their results merge through the additive ``all_tests``
    reducer before the graph proceeds to ``standard_patterns``.
    """
    chunks = state.get("all_chunks") or []
    if not chunks:
        # No chunks → skip fan-out, go straight to standard patterns. Returning
        # an empty list of Sends is invalid; LangGraph treats a string as a
        # destination, so we route to the next sequential node directly.
        return ["standard_patterns"]  # type: ignore[return-value]
    return [
        Send("test_generation_worker", {**state, "current_chunk": chunk})
        for chunk in chunks
    ]


def build_graph(checkpointer: Optional[BaseCheckpointSaver] = None) -> StateGraph:
    """
    Construct and compile the generation-only LangGraph pipeline.

    Per-chunk test generation runs as a Send-API map-reduce: the
    ``test_generation_announce`` node prints a banner and a conditional edge
    fans out one ``test_generation_worker`` per chunk; their outputs merge
    through the ``all_tests`` reducer before ``standard_patterns``.

    If ``checkpointer`` is provided, the compiled graph persists state between
    nodes so an interrupted run can be resumed by re-invoking with the same
    ``thread_id`` (passed via ``config={"configurable": {"thread_id": ...}}``)
    and a ``None`` initial state.
    """

    graph = StateGraph(PipelineState)

    # -- Register core nodes --------------------------------------------------
    graph.add_node("parse", parse_node)
    graph.add_node("navigation", navigation_node)
    graph.add_node("chunker", chunker_node)
    graph.add_node("summary", summary_node)
    graph.add_node("test_generation_announce", test_generation_announce_node)
    graph.add_node("test_generation_worker", test_generation_worker_node)
    graph.add_node("standard_patterns", standard_patterns_node)
    graph.add_node("assembler", assembler_node)
    graph.add_node("finalize", finalize_node)

    # -- Entry point ----------------------------------------------------------
    graph.set_entry_point("parse")

    # -- Core sequential pipeline ---------------------------------------------
    graph.add_edge("parse", "navigation")
    graph.add_edge("navigation", "chunker")
    graph.add_edge("chunker", "summary")
    graph.add_edge("summary", "test_generation_announce")

    # -- Send-API fan-out: one worker per chunk ------------------------------
    graph.add_conditional_edges(
        "test_generation_announce",
        _fan_out_test_generation,
        ["test_generation_worker", "standard_patterns"],
    )
    graph.add_edge("test_generation_worker", "standard_patterns")

    # -- Resume sequential pipeline after fan-in -----------------------------
    graph.add_edge("standard_patterns", "assembler")
    graph.add_edge("assembler", "finalize")

    # -- End ------------------------------------------------------------------
    graph.add_edge("finalize", END)

    return graph.compile(checkpointer=checkpointer) if checkpointer else graph.compile()
