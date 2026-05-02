import os
from typing import Any, Dict, Optional

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from autospectest.framework.agents.base import BaseAgent
from autospectest.framework.orchestrator.graph import build_graph
from autospectest.framework.orchestrator.runs import CHECKPOINT_DB
from autospectest.framework.orchestrator.state import PipelineState


class UIASTGenerator:

    def __init__(
        self,
        api_key: str,
        model: str = "openai/gpt-4o",
        debug: bool = False,
        debug_file: str = "debug_log.txt",
        run_id: Optional[str] = None,
    ):
        self.api_key = api_key
        self.model = model
        self.debug = debug
        self.debug_file = debug_file
        self.debug_dir = ""
        self.run_id = run_id

    async def generate(
        self,
        functional_desc: Dict[str, Any],
        output_dir: str = "output",
        resume: bool = False,
    ) -> Optional[Dict[str, Any]]:
        print("=" * 60)
        print("AUTOSPECTEST  (UI-AST Pipeline)")
        print("=" * 60)
        if self.run_id:
            print(f"run_id: {self.run_id}{'  (resuming)' if resume else ''}")

        if resume and not self.run_id:
            raise ValueError("resume=True requires a run_id")

        os.makedirs(output_dir, exist_ok=True)
        if self.debug:
            self.debug_dir = os.path.join(output_dir, "debug")
            os.makedirs(self.debug_dir, exist_ok=True)
            BaseAgent.reset_debug_state()
            print(f"Debug mode: ON  (logs → {self.debug_dir}/)")

        if self.run_id:
            CHECKPOINT_DB.parent.mkdir(parents=True, exist_ok=True)
            async with AsyncSqliteSaver.from_conn_string(str(CHECKPOINT_DB)) as checkpointer:
                graph = build_graph(checkpointer=checkpointer)
                return await self._invoke(graph, functional_desc, output_dir, resume)
        else:
            graph = build_graph()
            return await self._invoke(graph, functional_desc, output_dir, resume)

    async def _invoke(self, graph, functional_desc, output_dir: str, resume: bool):
        config = {"configurable": {"thread_id": self.run_id}} if self.run_id else None

        if resume:
            final_state = await graph.ainvoke(None, config=config)
        else:
            initial_state: PipelineState = {
                "functional_desc": functional_desc,
                "api_key": self.api_key,
                "model": self.model,
                "debug": self.debug,
                "debug_file": self.debug_file,
                "debug_dir": self.debug_dir,
                "output_dir": output_dir,
            }
            final_state = (
                await graph.ainvoke(initial_state, config=config)
                if config
                else await graph.ainvoke(initial_state)
            )

        return final_state.get("output")

    def close(self) -> None:
        pass
