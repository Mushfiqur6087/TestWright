"""Export post-verification data and associated test cases to Markdown."""

from collections import defaultdict


def escape_md(text: str) -> str:
    """Escape markdown table characters and normalize line breaks."""
    if text is None:
        return ""
    text = str(text)
    text = text.replace("\n", "<br>")
    text = text.replace("|", "\\|")
    return text


def truncate(text: str, max_len: int = 140) -> str:
    """Truncate long text for compact table rendering."""
    if not text:
        return ""
    text = str(text)
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def _coverage_key(test_case: dict) -> str:
    coverage = str(test_case.get("verification_coverage", "") or "").strip().lower()
    return coverage if coverage else "unknown"


def _strategy_label(strategy: str) -> str:
    if strategy == "before_after":
        return "Before/After"
    if strategy == "cross_user":
        return "Cross-User"
    return "After Only"


def _type_label(vtype: str) -> str:
    if not vtype:
        return "-"
    return vtype.replace("_", " ").title()


def _confidence_label(raw_confidence) -> str:
    if not isinstance(raw_confidence, (int, float)):
        return "-"
    if raw_confidence <= 0:
        return "-"
    if raw_confidence <= 1:
        return f"{raw_confidence:.0%}"
    return f"{raw_confidence:.0f}%"


def generate_post_verification_markdown(data: dict) -> str:
    """Generate a focused Markdown report with only post-verification data."""
    lines = []

    project_name = data.get("project_name", "Test Cases")
    lines.append(f"# {project_name} - Post-Verification Report")
    lines.append("")
    lines.append(f"**Base URL:** {data.get('base_url', 'N/A')}")
    lines.append(f"**Generated:** {data.get('generated_at', 'N/A')}")
    lines.append("")

    test_cases = data.get("test_cases", []) or []
    execution_plans = data.get("execution_plans", {}) or {}

    test_lookup = {
        tc.get("id"): tc
        for tc in test_cases
        if tc.get("id")
    }

    source_tests = [
        tc for tc in test_cases
        if tc.get("needs_post_verification")
    ]
    source_tests.sort(key=lambda tc: tc.get("id", ""))

    associated_ids = set()
    for tc in source_tests:
        for pv in tc.get("post_verifications", []) or []:
            matched_id = pv.get("matched_test_id")
            if matched_id and matched_id != "-" and matched_id in test_lookup:
                associated_ids.add(matched_id)

    associated_tests = [test_lookup[test_id] for test_id in sorted(associated_ids)]

    coverage_counts = defaultdict(int)
    for tc in source_tests:
        coverage_counts[_coverage_key(tc)] += 1

    summary = data.get("summary", {}) or {}
    post_summary = summary.get("post_verification", {}) or {}

    tests_needing = post_summary.get("tests_needing_verification", len(source_tests))
    full_coverage = post_summary.get("full_coverage", coverage_counts.get("full", 0))
    partial_coverage = post_summary.get("partial_coverage", coverage_counts.get("partial", 0))
    no_coverage = post_summary.get("no_coverage", coverage_counts.get("none", 0))
    minimal_coverage = coverage_counts.get("minimal", 0)

    tests_with_gaps = post_summary.get("tests_with_verification_gaps", 0)
    total_missing = post_summary.get("total_missing_verifications", 0)

    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("|--------|-------|")
    lines.append(f"| Source Tests Needing Verification | {tests_needing} |")
    lines.append(f"| Full Coverage | {full_coverage} |")
    lines.append(f"| Partial Coverage | {partial_coverage} |")
    lines.append(f"| Minimal Coverage | {minimal_coverage} |")
    lines.append(f"| No Coverage | {no_coverage} |")
    lines.append(f"| Tests With Verification Gaps | {tests_with_gaps} |")
    lines.append(f"| Total Missing Verifications | {total_missing} |")
    lines.append(f"| Associated Verification Tests | {len(associated_tests)} |")
    lines.append("")

    by_type = post_summary.get("by_verification_type") or {}
    nonzero_types = [(k, v) for k, v in by_type.items() if v]
    if nonzero_types:
        lines.append("### Generated Verifications by Type")
        lines.append("")
        lines.append("| Type | Count |")
        lines.append("|------|-------|")
        for k, v in nonzero_types:
            lines.append(f"| {_type_label(k)} | {v} |")
        lines.append("")

    by_strategy = post_summary.get("by_strategy") or {}
    nonzero_strats = [(k, v) for k, v in by_strategy.items() if v]
    if nonzero_strats:
        lines.append("### Generated Verifications by Strategy")
        lines.append("")
        lines.append("| Strategy | Count |")
        lines.append("|----------|-------|")
        for k, v in nonzero_strats:
            lines.append(f"| {_strategy_label(k)} | {v} |")
        lines.append("")

    gaps = post_summary.get("coverage_gaps", []) or []
    if gaps:
        lines.append("### Top Coverage Gaps")
        lines.append("")
        for gap in gaps:
            lines.append(f"- {escape_md(gap)}")
        lines.append("")

    lines.append("---")
    lines.append("")

    lines.append("## Post-Verification Source Tests")
    lines.append("")

    if not source_tests:
        lines.append("No post-verification source tests found in this JSON.")
        lines.append("")
    else:
        for tc in source_tests:
            tc_id = tc.get("id", "N/A")
            title = tc.get("title", "N/A")
            lines.append(f"### {tc_id}: {escape_md(title)}")
            lines.append("")

            modifies_state = tc.get("modifies_state", []) or []
            modifies_value = ", ".join(modifies_state) if modifies_state else "-"

            lines.append("| Field | Value |")
            lines.append("|-------|-------|")
            lines.append(f"| Module | {escape_md(tc.get('module_title', 'N/A'))} |")
            lines.append(f"| Workflow | {escape_md(tc.get('workflow', 'N/A'))} |")
            lines.append(f"| Test Type | {escape_md(tc.get('test_type', 'N/A'))} |")
            lines.append(f"| Priority | {escape_md(tc.get('priority', 'N/A'))} |")
            lines.append(f"| Coverage | {escape_md(tc.get('verification_coverage', 'unknown'))} |")
            lines.append(f"| Modifies State | {escape_md(modifies_value)} |")
            lines.append("")

            lines.append("#### Source Test Details")
            lines.append("")
            lines.append(f"**Preconditions:** {escape_md(tc.get('preconditions', 'None'))}")
            lines.append("")
            lines.append("**Steps:**")
            for idx, step in enumerate(tc.get("steps", []) or [], 1):
                lines.append(f"{idx}. {escape_md(step)}")
            lines.append("")
            lines.append(f"**Expected Result:** {escape_md(tc.get('expected_result', 'N/A'))}")
            lines.append("")

            post_verifications = tc.get("post_verifications", []) or []
            lines.append("#### Verification Mapping")
            lines.append("")
            if not post_verifications:
                lines.append("No verification mappings were generated for this source test.")
                lines.append("")
            else:
                lines.append("| # | Ideal Verification | Status | Type | Strategy | Matched Test | Confidence |")
                lines.append("|---|--------------------|--------|------|----------|--------------|------------|")

                for idx, pv in enumerate(post_verifications, 1):
                    ideal = escape_md(truncate(pv.get("ideal", "-"), 120))
                    status = escape_md(pv.get("status", "unknown"))
                    vtype = escape_md(_type_label(pv.get("verification_type", "")))
                    strategy = escape_md(_strategy_label(pv.get("execution_strategy", "after_only")))

                    matched_id = pv.get("matched_test_id", "-")
                    matched_title = pv.get("matched_test_title", "")
                    if matched_id and matched_id != "-":
                        matched_value = f"{matched_id} - {matched_title}" if matched_title else matched_id
                    else:
                        matched_value = "-"

                    confidence = _confidence_label(pv.get("confidence"))

                    lines.append(
                        f"| {idx} | {ideal} | {status} | {vtype} | {strategy} | {escape_md(truncate(matched_value, 90))} | {confidence} |"
                    )

                lines.append("")

            needed = tc.get("needs_new_verification_test", []) or []
            if needed:
                lines.append("#### Verification Tests Needed")
                lines.append("")
                lines.append("| # | Type | Strategy | Target Module | Observer | Suggested Test Title |")
                lines.append("|---|------|----------|---------------|----------|----------------------|")
                for idx, n in enumerate(needed, 1):
                    n_type = escape_md(_type_label(n.get("verification_type", "")))
                    n_strategy = escape_md(_strategy_label(n.get("execution_strategy", "after_only")))
                    n_module = escape_md(n.get("target_module", "-") or "-")
                    n_observer = escape_md(n.get("observer_role", "") or "-")
                    n_title = escape_md(truncate(n.get("suggested_test_title", ""), 100))
                    lines.append(
                        f"| {idx} | {n_type} | {n_strategy} | {n_module} | {n_observer} | {n_title} |"
                    )
                lines.append("")

            coverage_gaps = tc.get("coverage_gaps", []) or []
            if coverage_gaps:
                lines.append("#### Coverage Gaps")
                lines.append("")
                for gap in coverage_gaps:
                    lines.append(f"- {escape_md(gap)}")
                lines.append("")

            plan = execution_plans.get(tc_id, {})
            execution_order = plan.get("execution_order", []) if isinstance(plan, dict) else []
            if execution_order:
                lines.append("#### Execution Plan")
                lines.append("")
                lines.append("| Step | Phase | Action | Test ID | Purpose |")
                lines.append("|------|-------|--------|---------|---------|")
                for step in execution_order:
                    lines.append(
                        "| {step} | {phase} | {action} | {test_id} | {purpose} |".format(
                            step=step.get("step", "?"),
                            phase=escape_md(step.get("phase", "")),
                            action=escape_md(step.get("action", "")),
                            test_id=escape_md(step.get("test_id", "-")),
                            purpose=escape_md(truncate(step.get("purpose", ""), 100)),
                        )
                    )
                lines.append("")

                manual_steps = plan.get("manual_steps", []) if isinstance(plan, dict) else []
                if manual_steps:
                    lines.append("**Manual Verification Required:**")
                    for ms in manual_steps:
                        purpose = escape_md(ms.get("purpose", "")) if isinstance(ms, dict) else escape_md(str(ms))
                        suggested = escape_md(ms.get("suggested_step", "")) if isinstance(ms, dict) else ""
                        reason = escape_md(ms.get("reason", "")) if isinstance(ms, dict) else ""
                        if purpose:
                            lines.append(f"- Purpose: {purpose}")
                        if suggested:
                            lines.append(f"- Suggested Step: {suggested}")
                        if reason:
                            lines.append(f"- Reason: {reason}")
                    lines.append("")

            lines.append("---")
            lines.append("")

    lines.append("## Associated Verification Test Cases")
    lines.append("")
    lines.append("These are matched test cases referenced by post-verification mappings.")
    lines.append("")

    if not associated_tests:
        lines.append("No associated verification test cases were found.")
        lines.append("")
    else:
        lines.append("| TC ID | Module | Title | Type | Priority | Expected Result |")
        lines.append("|-------|--------|-------|------|----------|------------------|")
        for tc in associated_tests:
            lines.append(
                "| {id} | {module} | {title} | {test_type} | {priority} | {expected} |".format(
                    id=escape_md(tc.get("id", "N/A")),
                    module=escape_md(tc.get("module_title", "N/A")),
                    title=escape_md(truncate(tc.get("title", "N/A"), 90)),
                    test_type=escape_md(tc.get("test_type", "N/A")),
                    priority=escape_md(tc.get("priority", "N/A")),
                    expected=escape_md(truncate(tc.get("expected_result", "N/A"), 120)),
                )
            )
        lines.append("")

    return "\n".join(lines)
