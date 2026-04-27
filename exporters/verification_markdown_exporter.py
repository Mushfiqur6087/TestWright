"""Render verifications.json as a human-readable markdown report."""

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List


def load_verifications(input_path: str) -> dict:
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _esc(text: Any) -> str:
    if text is None:
        return ""
    return str(text).replace("|", "\\|")


def _bullet_list(items: Any) -> str:
    if not items:
        return "-"
    if isinstance(items, str):
        return items
    return "<br>".join(f"- {_esc(x)}" for x in items)


def _resolve_source_test_cases_path(source_path: str, verification_file_path: str = "") -> Path | None:
    """Resolve source_test_cases_file to an existing path if possible."""
    raw = Path(source_path)
    candidates: List[Path] = []

    if raw.is_absolute():
        candidates.append(raw)
    else:
        candidates.append(Path.cwd() / raw)
        if verification_file_path:
            verif_path = Path(verification_file_path).resolve()
            candidates.append(verif_path.parent / raw)
            for parent in verif_path.parents:
                candidates.append(parent / raw)

    seen = set()
    for candidate in candidates:
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def _load_test_case_lookup(data: dict, verification_file_path: str = "") -> Dict[str, Dict[str, Any]]:
    """Load test cases referenced by source_test_cases_file and map by id."""
    source_file = data.get("source_test_cases_file")
    if not source_file:
        return {}

    resolved = _resolve_source_test_cases_path(source_file, verification_file_path=verification_file_path)
    if not resolved:
        return {}

    try:
        with open(resolved, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except Exception:
        return {}

    lookup: Dict[str, Dict[str, Any]] = {}
    for test_case in payload.get("test_cases", []) or []:
        tc_id = test_case.get("id")
        if tc_id:
            lookup[tc_id] = test_case
    return lookup


def _infer_execution_page(
    verification_type: str,
    body: Dict[str, Any],
    test_case: Dict[str, Any] | None,
) -> str:
    """Infer the page/screen where this verification is executed."""
    test_case = test_case or {}

    if verification_type == "same_actor_navigation":
        pre_nav = (body.get("pre_check") or {}).get("navigate_to")
        post_nav = (body.get("post_check") or {}).get("navigate_to")
        if pre_nav and post_nav and pre_nav != post_nav:
            return f"{pre_nav} -> {post_nav}"
        return pre_nav or post_nav or test_case.get("module_title", "")

    if verification_type == "cross_actor":
        return (body.get("actor_b") or {}).get("navigate_to", "") or test_case.get("module_title", "")

    if verification_type == "out_of_band":
        partial_nav = (body.get("in_app_partial_check") or {}).get("navigate_to")
        if partial_nav:
            return f"{partial_nav} (partial in-app check)"
        return "External channel (out_of_band)"

    return test_case.get("module_title", "")


def _render_test_case_context(
    verification_type: str,
    body: Dict[str, Any],
    test_case: Dict[str, Any] | None,
) -> List[str]:
    """Render source test-case details and inferred execution page."""
    if not test_case:
        return []

    lines: List[str] = []
    execution_page = _infer_execution_page(verification_type, body, test_case)

    lines.append("**Test case context**")
    lines.append(f"- title: {test_case.get('title', '')}")
    lines.append(f"- workflow: {test_case.get('workflow', '')}")
    lines.append(f"- execution_page: {execution_page}")

    steps = test_case.get("steps", []) or []
    if steps:
        lines.append("- test_steps:")
        for step in steps:
            lines.append(f"  - {step}")

    expected_result = test_case.get("expected_result", "")
    if expected_result:
        lines.append(f"- expected_result: {expected_result}")

    return lines


def _render_body(
    verification_type: str,
    body: Dict[str, Any],
    test_case: Dict[str, Any] | None = None,
) -> List[str]:
    lines: List[str] = []

    if verification_type == "same_actor_navigation":
        pre = body.get("pre_check") or {}
        post = body.get("post_check") or {}
        lines.append("**Pre-check**")
        lines.append(f"- navigate_to: {pre.get('navigate_to', '')}")
        lines.append(f"- observe:")
        for item in pre.get("observe", []) or []:
            lines.append(f"  - {item}")
        lines.append("")

        context_lines = _render_test_case_context(verification_type, body, test_case)
        if context_lines:
            lines.extend(context_lines)
            lines.append("")

        lines.append("**Post-check**")
        lines.append(f"- navigate_to: {post.get('navigate_to', '')}")
        lines.append(f"- observe:")
        for item in post.get("observe", []) or []:
            lines.append(f"  - {item}")
        lines.append(f"- expected_change: {post.get('expected_change', '')}")

    elif verification_type == "cross_actor":
        a = body.get("actor_a") or {}
        b = body.get("actor_b") or {}
        lines.append("**Actor A (performs action)**")
        lines.append(f"- role: {a.get('role', '')}")
        lines.append(f"- action: {a.get('action', '')}")
        lines.append("")
        lines.append("**Actor B (observes effect)**")
        lines.append(f"- role: {b.get('role', '')}")
        lines.append(f"- session: {b.get('session', '')}")
        lines.append(f"- navigate_to: {b.get('navigate_to', '')}")
        lines.append(f"- observe:")
        for item in b.get("observe", []) or []:
            lines.append(f"  - {item}")
        lines.append(f"- expected_change: {b.get('expected_change', '')}")

    elif verification_type == "out_of_band":
        lines.append(f"- trigger_action: {body.get('trigger_action', '')}")
        lines.append(f"- channel: {body.get('channel', '')}")
        lines.append(f"- recipient: {body.get('recipient', '')}")
        lines.append("- expected_content:")
        for item in body.get("expected_content", []) or []:
            lines.append(f"  - {item}")
        partial = body.get("in_app_partial_check") or {}
        if partial:
            lines.append("- in_app_partial_check:")
            lines.append(f"  - navigate_to: {partial.get('navigate_to', '')}")
            lines.append(f"  - observe: {partial.get('observe', '')}")
        if body.get("verification_method"):
            lines.append(f"- verification_method: {body['verification_method']}")

    elif verification_type == "unobservable_by_design":
        lines.append(f"- reason: {body.get('reason', '')}")
        lines.append(f"- suppressed_assertion: {body.get('suppressed_assertion', '')}")
        lines.append(f"- alternative_assertion: {body.get('alternative_assertion', '')}")
        if body.get("environment_condition"):
            lines.append(f"- environment_condition: {body['environment_condition']}")

    else:
        # Unknown type — dump raw dict for visibility.
        lines.append("```json")
        lines.append(json.dumps(body, indent=2, ensure_ascii=False))
        lines.append("```")

    return lines


def generate_verification_markdown(data: dict, verification_file_path: str = "") -> str:
    lines: List[str] = []
    test_case_lookup = _load_test_case_lookup(data, verification_file_path=verification_file_path)

    project = data.get("project_name", "Verifications")
    lines.append(f"# {project} — Verifications")
    lines.append("")
    lines.append(f"**Base URL:** {data.get('base_url', 'N/A')}")
    lines.append(f"**Generated:** {data.get('generated_at', 'N/A')}")
    lines.append(f"**Source test cases:** {data.get('source_test_cases_file', 'N/A')}")

    spec_files = data.get("source_spec_files", [])
    if spec_files:
        lines.append("**Source spec files:**")
        for s in spec_files:
            lines.append(f"- {s}")
    lines.append("")

    summary = data.get("coverage_summary", {}) or {}
    lines.append("## Coverage Summary")
    lines.append("")
    lines.append("| Coverage | Count |")
    lines.append("|----------|-------|")
    lines.append(f"| Verifiable | {summary.get('verifiable', 0)} |")
    lines.append(f"| Manual only | {summary.get('manual_only', 0)} |")
    lines.append(f"| Not coverable | {summary.get('not_coverable', 0)} |")
    lines.append(f"| **Total records** | **{summary.get('total_records', 0)}** |")
    lines.append("")

    by_type = summary.get("by_type", {}) or {}
    if by_type:
        lines.append("### Breakdown by verification type")
        lines.append("")
        lines.append("| Type | Count |")
        lines.append("|------|-------|")
        for vtype, count in by_type.items():
            lines.append(f"| {vtype} | {count} |")
        lines.append("")

    lines.append("---")
    lines.append("")

    verifications = data.get("verifications", []) or []
    grouped: Dict[str, List[dict]] = defaultdict(list)
    for record in verifications:
        tc_id = record.get("test_case_id", "")
        module = tc_id.split(".", 1)[0] if "." in tc_id else "other"
        grouped[module].append(record)

    lines.append("## Verifications")
    lines.append("")

    for module_key in sorted(grouped.keys()):
        lines.append(f"### Module {module_key}")
        lines.append("")
        for record in sorted(grouped[module_key], key=lambda r: r.get("test_case_id", "")):
            tc_id = record.get("test_case_id", "")
            vtype = record.get("verification_type", "")
            coverage = record.get("coverage", "")
            note = record.get("coverage_note")
            body = record.get("body", {}) or {}
            test_case = test_case_lookup.get(tc_id)

            lines.append(f"#### {tc_id}")
            lines.append("")
            lines.append(f"- **Type:** `{vtype}`")
            lines.append(f"- **Coverage:** `{coverage}`")
            if note:
                lines.append(f"- **Coverage note:** {note}")
            lines.append("")
            lines.extend(_render_body(vtype, body, test_case=test_case))
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)
