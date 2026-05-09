from typing import Optional

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, StateGraph

from autospectest.framework.orchestrator.nodes import finalize_node, generate_and_critique_node, generate_tests_node
from autospectest.framework.orchestrator.state import PipelineState


def build_graph(checkpointer: Optional[BaseCheckpointSaver] = None):
    graph = StateGraph(PipelineState)

    graph.add_node("generate_and_critique", generate_and_critique_node)
    graph.add_node("generate_tests", generate_tests_node)
    graph.add_node("finalize", finalize_node)

    graph.set_entry_point("generate_and_critique")
    graph.add_edge("generate_and_critique", "generate_tests")
    graph.add_edge("generate_tests", "finalize")
    graph.add_edge("finalize", END)

    return graph.compile(checkpointer=checkpointer) if checkpointer else graph.compile()
