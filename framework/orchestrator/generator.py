"""TestCaseGenerator main orchestrator."""

import json
import os
from typing import Any, Dict, Optional

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from autospectest.framework.agents.base import BaseAgent
from autospectest.framework.orchestrator.graph import build_graph
from autospectest.framework.orchestrator.runs import CHECKPOINT_DB
from autospectest.framework.orchestrator.state import PipelineState
from autospectest.framework.schemas.schemas import TestSuiteOutput


class TestCaseGenerator:
    """
    Main orchestrator for test case generation.

    Uses a compiled LangGraph StateGraph under the hood. When constructed with
    a ``run_id``, an async SQLite checkpointer persists state between nodes so
    an interrupted run can be resumed by passing ``resume=True`` to
    ``generate()``.
    """

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

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def generate(
        self,
        functional_desc: str | Dict[str, Any],
        output_dir: str = "output",
        resume: bool = False,
    ) -> TestSuiteOutput:
        """
        Generate test cases from a functional description.

        Args:
            functional_desc: Path to functional_desc.json **or** an
                already-loaded dict. Ignored when ``resume=True`` (state is
                read from the checkpoint instead).
            output_dir: Directory to save output files
            resume: If True, resume from the last checkpoint instead of
                starting a fresh run. Requires a ``run_id`` on the generator.

        Returns:
            TestSuiteOutput with navigation graph and test cases
        """

        print("=" * 60)
        print("TESTWRIGHT  (LangGraph Pipeline)")
        print("=" * 60)
        if self.run_id:
            print(f"run_id: {self.run_id}"
                  f"{'  (resuming)' if resume else ''}")

        if resume and not self.run_id:
            raise ValueError("resume=True requires a run_id on the generator")

        os.makedirs(output_dir, exist_ok=True)
        if self.debug:
            self.debug_dir = os.path.join(output_dir, "debug")
            os.makedirs(self.debug_dir, exist_ok=True)
            BaseAgent.reset_debug_state()
            print(f"Debug mode: ON  (per-stage logs → {self.debug_dir}/)")

        if self.run_id:
            CHECKPOINT_DB.parent.mkdir(parents=True, exist_ok=True)
            async with AsyncSqliteSaver.from_conn_string(str(CHECKPOINT_DB)) as checkpointer:
                graph = build_graph(checkpointer=checkpointer)
                output = await self._invoke(graph, functional_desc, output_dir, resume)
        else:
            graph = build_graph()
            output = await self._invoke(graph, functional_desc, output_dir, resume)

        self._print_summary(output)
        return output

    def close(self) -> None:
        """No-op kept for API compatibility."""

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    async def _invoke(self, graph, functional_desc, output_dir: str, resume: bool) -> TestSuiteOutput:
        config = {"configurable": {"thread_id": self.run_id}} if self.run_id else None

        if resume:
            final_state = await graph.ainvoke(None, config=config)
        else:
            if isinstance(functional_desc, dict):
                print("\nUsing provided functional description...")
            else:
                print("\nLoading input files...")
                functional_desc = self._load_json(functional_desc)
                print(f"  - Loaded: {functional_desc}")

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

        return final_state["output"]

    @staticmethod
    def _load_json(path: str) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _print_summary(output: TestSuiteOutput):
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)

        summary = output.summary
        print(f"Total Test Cases: {summary.get('total_tests', 0)}")

        print("\nBy Type:")
        for t, count in summary.get("by_type", {}).items():
            print(f"  - {t}: {count}")

        print("\nBy Priority:")
        for p, count in summary.get("by_priority", {}).items():
            print(f"  - {p}: {count}")

        print("\nBy Module:")
        for m, count in summary.get("by_module", {}).items():
            print(f"  - {m}: {count}")

        print(f"\nNavigation Graph:")
        print(f"  - Total nodes: {len(output.navigation_graph.nodes)}")
        if output.navigation_graph.graph_image_path:
            print(f"  - Graph image: {output.navigation_graph.graph_image_path}")
        for node in output.navigation_graph.nodes.values():
            tc_count = len(node.test_case_ids)
            print(f"  - {node.title}: {tc_count} test cases, connects to {len(node.connected_to)} pages")

