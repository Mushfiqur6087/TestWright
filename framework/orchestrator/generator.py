"""TestCaseGenerator main orchestrator."""

import json
import os
from typing import Any, Dict

from autospectest.framework.agents.base import BaseAgent
from autospectest.framework.orchestrator.graph import build_graph
from autospectest.framework.orchestrator.state import PipelineState
from autospectest.framework.schemas.schemas import TestSuiteOutput


class TestCaseGenerator:
    """
    Main orchestrator for test case generation.

    Uses a compiled LangGraph StateGraph under the hood.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        provider: str = "openai",
        debug: bool = False,
        debug_file: str = "debug_log.txt",
    ):
        self.api_key = api_key
        self.model = model
        self.provider = provider
        self.debug = debug
        self.debug_file = debug_file

        # Initialize debug session once
        if debug:
            BaseAgent.reset_debug_state()
            BaseAgent.init_debug_session(debug_file, model)

        # Compile the LangGraph pipeline once
        self.graph = build_graph()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        functional_desc: str | Dict[str, Any],
        output_dir: str = "output",
    ) -> TestSuiteOutput:
        """
        Generate test cases from a functional description.

        Args:
            functional_desc: Path to functional_desc.json **or** an
                already-loaded dict.
            output_dir: Directory to save output files

        Returns:
            TestSuiteOutput with navigation graph and test cases
        """

        print("=" * 60)
        print("TESTWRIGHT  (LangGraph Pipeline)")
        print("=" * 60)
        if self.debug:
            print(f"Debug mode: ON (logging to {self.debug_file})")

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Load inputs -- accept a path string or a pre-loaded dict
        if isinstance(functional_desc, dict):
            print("\nUsing provided functional description...")
        else:
            print("\nLoading input files...")
            functional_desc = self._load_json(functional_desc)
            print(f"  - Loaded: {functional_desc}")

        # Build the initial state for the graph
        initial_state: PipelineState = {
            # Inputs
            "functional_desc": functional_desc,
            # Config
            "api_key": self.api_key,
            "model": self.model,
            "provider": self.provider,
            "debug": self.debug,
            "debug_file": self.debug_file,
            "output_dir": output_dir,
        }

        # Run the graph
        final_state = self.graph.invoke(initial_state)

        # Extract the final output
        output: TestSuiteOutput = final_state["output"]

        # Print summary
        self._print_summary(output)

        return output

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _load_json(path: str) -> Dict[str, Any]:
        """Load a JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _print_summary(output: TestSuiteOutput):
        """Print summary statistics."""
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
