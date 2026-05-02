from typing import Optional

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, StateGraph

from autospectest.framework.orchestrator.nodes import finalize_node, semantic_critic_node, ui_ast_node
from autospectest.framework.orchestrator.state import PipelineState


def build_graph(checkpointer: Optional[BaseCheckpointSaver] = None):
    graph = StateGraph(PipelineState)

    graph.add_node("ui_ast", ui_ast_node)
    graph.add_node("semantic_critic", semantic_critic_node)
    graph.add_node("finalize", finalize_node)

    graph.set_entry_point("ui_ast")
    graph.add_edge("ui_ast", "semantic_critic")
    graph.add_edge("semantic_critic", "finalize")
    graph.add_edge("finalize", END)

    return graph.compile(checkpointer=checkpointer) if checkpointer else graph.compile()
