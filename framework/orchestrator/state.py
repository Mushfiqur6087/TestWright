"""
LangGraph State Schema

Defines the typed state that flows through the entire pipeline graph.
Each node reads from and writes to this shared state.

Reducer annotations are required for LangGraph >= 1.0 so that
fan-in from parallel branches (navigation, test_generation, summary
-> assembler) correctly merges all state fields.
"""

from typing import Annotated, Any, Dict, List, Optional, TypedDict

from autospectest.framework.schemas.schemas import (
    ModuleSummary,
    NavigationGraph,
    ParsedFunctionalDescription,
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


def _extend(old, new):
    """Reducer: concatenate lists across parallel fan-in branches.

    Used for ``all_tests``: each Send-API worker emits its per-chunk test list
    and the reducer accumulates them into the final ordered list. Tolerates
    None on either side so the field can stay unset until the first worker
    writes to it.
    """
    if old is None:
        old = []
    if new is None:
        return old
    return list(old) + list(new)


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
    # Per-chunk payload for Send-API fan-out workers. Each worker reads exactly
    # one chunk via this field; the reducer keeps the latest write because each
    # branch sets it once with its own value.
    current_chunk: Annotated[Optional[WorkflowChunk], _last_value]
    # Workers concatenate their results here via the additive reducer.
    all_tests: Annotated[List[TestCase], _extend]

    # -- Step 5b: Standard Patterns (session + RBAC) --------------------------
    standard_pattern_tests: Annotated[List[TestCase], _last_value]

    # -- Step 6: Assembler ----------------------------------------------------
    output: Annotated[TestSuiteOutput, _last_value]
