from typing import Annotated, Any, Dict, List, TypedDict


def _last_value(old, new):
    return new if new is not None else old


def _extend(old, new):
    if old is None:
        old = []
    if new is None:
        return old
    return list(old) + list(new)


class PipelineState(TypedDict, total=False):
    # Inputs
    functional_desc: Annotated[Dict[str, Any], _last_value]

    # Config
    api_key: Annotated[str, _last_value]
    model: Annotated[str, _last_value]
    debug: Annotated[bool, _last_value]
    debug_file: Annotated[str, _last_value]
    debug_dir: Annotated[str, _last_value]
    output_dir: Annotated[str, _last_value]

    # UI-AST results (one entry per module)
    ui_ast_results: Annotated[List[Dict[str, Any]], _last_value]

    # Stage 2 — semantic audit results (one entry per module)
    semantic_critique_results: Annotated[List[Dict[str, Any]], _last_value]

    # Final assembled output dict
    output: Annotated[Dict[str, Any], _last_value]
