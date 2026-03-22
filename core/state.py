"""
LangGraph State Schema

Defines the typed state that flows through the entire pipeline graph.
Each node reads from and writes to this shared state.

Reducer annotations are required for LangGraph >= 1.0 so that
fan-in from parallel branches (navigation, test_generation, summary
-> assembler) correctly merges all state fields.
"""

from typing import Annotated, Any, Dict, List, Optional, TypedDict

from testwright.models.schemas import (
    IdealVerification,
    ModuleSummary,
    NavigationGraph,
    ParsedFunctionalDescription,
    ParsedModule,
    TestCase,
    TestSuiteOutput,
    WorkflowChunk,
)


# -- Reducers ----------------------------------------------------------------
# LangGraph needs a reducer for every field that could be set
# by parallel branches fanning into a single node.

def _last_value(old, new):
    """Reducer: always take the latest (newest) value."""
    return new if new is not None else old


class PipelineState(TypedDict, total=False):
    """
    Shared state flowing through the LangGraph pipeline.

    Fields are populated progressively as each node executes.
    ``total=False`` makes all fields optional so nodes can write
    only the fields they produce.

    Every field that is written by a parallel branch uses an
    ``Annotated[..., _last_value]`` reducer so fan-in merges work.
    """

    # -- Inputs ---------------------------------------------------------------
    functional_desc: Annotated[Dict[str, Any], _last_value]

    # -- Config ---------------------------------------------------------------
    api_key: Annotated[str, _last_value]
    model: Annotated[str, _last_value]
    provider: Annotated[str, _last_value]
    debug: Annotated[bool, _last_value]
    debug_file: Annotated[str, _last_value]
    output_dir: Annotated[str, _last_value]

    # -- Step 1: Parser -------------------------------------------------------
    parsed_desc: Annotated[ParsedFunctionalDescription, _last_value]

    # -- Step 2: Navigation (parallel branch A) -------------------------------
    nav_graph: Annotated[NavigationGraph, _last_value]

    # -- Step 3: Chunker ------------------------------------------------------
    all_chunks: Annotated[List[WorkflowChunk], _last_value]

    # -- Step 4: Summary (parallel branch C) ----------------------------------
    module_summaries: Annotated[Dict[int, ModuleSummary], _last_value]

    # -- Step 5: Test Generation ----------------------------------------------
    all_tests: Annotated[List[TestCase], _last_value]

    # -- Step 6: Assembler ----------------------------------------------------
    output: Annotated[TestSuiteOutput, _last_value]

    # -- Step 7: Verification Flag --------------------------------------------
    flagged_tests: Annotated[List[TestCase], _last_value]

    # -- Step 8: Ideal Verification -------------------------------------------
    ideal_verifications: Annotated[Dict[str, List[IdealVerification]], _last_value]

    # -- Step 9: Verification Matcher -----------------------------------------
    final_tests: Annotated[List[TestCase], _last_value]

    # -- Step 10: Execution Plan ----------------------------------------------
    execution_plans: Annotated[Dict[str, Any], _last_value]
    plan_summary: Annotated[Dict[str, Any], _last_value]
