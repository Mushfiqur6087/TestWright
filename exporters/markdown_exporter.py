"""Export test cases from JSON to human-readable Markdown format."""

import json
from collections import defaultdict


def load_test_cases(input_path: str) -> dict:
    """Load test cases from JSON file."""
    with open(input_path, 'r') as f:
        return json.load(f)


def escape_md(text: str) -> str:
    """Escape markdown special characters and handle newlines for table cells."""
    if not text:
        return ""
    # Replace newlines with <br> for table cells
    text = str(text).replace('\n', '<br>')
    # Escape pipe characters
    text = text.replace('|', '\\|')
    return text


def truncate(text: str, max_len: int = 60) -> str:
    """Truncate text to max length."""
    if not text:
        return ""
    text = str(text)
    if len(text) > max_len:
        return text[:max_len-3] + "..."
    return text


def generate_markdown(data: dict) -> str:
    """Generate markdown content from test case data."""
    lines = []

    # Header
    lines.append(f"# {data.get('project_name', 'Test Cases')}")
    lines.append("")
    lines.append(f"**Base URL:** {data.get('base_url', 'N/A')}")
    lines.append(f"**Generated:** {data.get('generated_at', 'N/A')}")
    lines.append("")

    # Summary
    summary = data.get('summary', {})
    if summary:
        lines.append("## Summary")
        lines.append("")
        lines.append("| Metric | Count |")
        lines.append("|--------|-------|")
        lines.append(f"| **Total Tests** | {summary.get('total_tests', 0)} |")
        lines.append("")

        by_type = summary.get('by_type', {})
        if by_type:
            lines.append("### By Type")
            lines.append("")
            lines.append("| Type | Count |")
            lines.append("|------|-------|")
            for test_type, count in by_type.items():
                lines.append(f"| {test_type.replace('_', ' ').title()} | {count} |")
            lines.append("")

        by_priority = summary.get('by_priority', {})
        if by_priority:
            lines.append("### By Priority")
            lines.append("")
            lines.append("| Priority | Count |")
            lines.append("|----------|-------|")
            for priority, count in by_priority.items():
                lines.append(f"| {priority} | {count} |")
            lines.append("")

        # Post-verification summary
        post_verif = summary.get('post_verification', {})
        if post_verif and post_verif.get('tests_needing_verification', 0) > 0:
            lines.append("### Post-Verification Coverage")
            lines.append("")
            lines.append("| Metric | Count |")
            lines.append("|--------|-------|")
            lines.append(f"| Tests Needing Verification | {post_verif.get('tests_needing_verification', 0)} |")
            lines.append(f"| Full Coverage | {post_verif.get('full_coverage', 0)} |")
            lines.append(f"| Partial Coverage | {post_verif.get('partial_coverage', 0)} |")
            lines.append(f"| No Coverage | {post_verif.get('no_coverage', 0)} |")
            lines.append("")

        # Execution plans summary
        exec_plans = summary.get('execution_plans', {})
        if exec_plans and exec_plans.get('total_plans', 0) > 0:
            lines.append("### Execution Plans")
            lines.append("")
            lines.append("| Metric | Value |")
            lines.append("|--------|-------|")
            lines.append(f"| Total Plans | {exec_plans.get('total_plans', 0)} |")
            lines.append(f"| Automated Steps | {exec_plans.get('total_automated_steps', 0)} |")
            lines.append(f"| Manual Steps | {exec_plans.get('total_manual_steps', 0)} |")
            lines.append(f"| Automation Rate | {exec_plans.get('automation_rate', 0)}% |")
            lines.append("")

    lines.append("---")
    lines.append("")

    # Group test cases by module
    test_cases = data.get('test_cases', [])
    modules = defaultdict(list)
    for tc in test_cases:
        module_title = tc.get('module_title', 'Unknown')
        modules[module_title].append(tc)

    # Test Cases by Module - TABLE FORMAT
    lines.append("## Test Cases")
    lines.append("")

    for module_title, cases in modules.items():
        lines.append(f"### {module_title}")
        lines.append("")

        # Group by test type within module
        by_type = defaultdict(list)
        for tc in cases:
            by_type[tc.get('test_type', 'other')].append(tc)

        type_order = ['positive', 'negative', 'edge_case']
        type_labels = {
            'positive': 'Functional Tests',
            'negative': 'Negative Tests',
            'edge_case': 'Edge Case Tests'
        }

        for test_type in type_order:
            if test_type not in by_type:
                continue

            type_cases = by_type[test_type]
            lines.append(f"#### {type_labels.get(test_type, test_type.title())}")
            lines.append("")

            # Table header
            lines.append("| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |")
            lines.append("|-------|-----------|---------------|-------|-----------------|----------|")

            for tc in type_cases:
                tc_id = tc.get('id', 'N/A')
                title = escape_md(tc.get('title', 'N/A'))
                preconditions = escape_md(tc.get('preconditions', 'None'))
                steps = tc.get('steps', [])
                # Format steps as numbered list with <br>
                steps_str = "<br>".join([f"{i+1}. {escape_md(step)}" for i, step in enumerate(steps)])
                expected = escape_md(tc.get('expected_result', 'N/A'))
                priority = tc.get('priority', 'Medium')

                lines.append(f"| {tc_id} | {title} | {preconditions} | {steps_str} | {expected} | {priority} |")

            lines.append("")

        lines.append("---")
        lines.append("")

    # Post-Verification Details Section
    # Collect all tests that need post-verification
    tests_with_verification = [tc for tc in test_cases if tc.get('needs_post_verification')]

    # Create a lookup dictionary for all test cases by ID
    test_case_lookup = {tc.get('id'): tc for tc in test_cases}

    # Also grab execution plans from data
    execution_plans = data.get('execution_plans', {})

    if tests_with_verification:
        lines.append("## Post-Verification Details")
        lines.append("")
        lines.append("This section shows verification requirements for tests that modify application state.")
        lines.append("Tests using the **before/after** strategy require running a verification test BEFORE")
        lines.append("and AFTER the action to compare values.")
        lines.append("")

        for tc in tests_with_verification:
            tc_id = tc.get('id', 'N/A')
            title = tc.get('title', 'N/A')
            coverage = tc.get('verification_coverage', 'unknown')
            coverage_icon = 'FULL' if coverage == 'full' else ('PARTIAL' if coverage in ['partial', 'minimal'] else 'NONE')
            modifies = tc.get('modifies_state', [])

            lines.append(f"### {tc_id}: {title}")
            lines.append("")
            lines.append(f"**Coverage:** {coverage_icon} {coverage.title()}")
            if modifies:
                lines.append(f"**Modifies State:** {', '.join(modifies)}")
            lines.append("")

            post_verifs = tc.get('post_verifications', [])
            matched_test_ids = set()

            if post_verifs:
                for i, pv in enumerate(post_verifs, 1):
                    ideal = pv.get('ideal', 'N/A')
                    status = pv.get('status', 'unknown')
                    status_icon = 'FOUND' if status == 'found' else ('PARTIAL' if status == 'partial' else 'MISSING')
                    matched_id = pv.get('matched_test_id', '-')
                    matched_title = pv.get('matched_test_title', '')
                    confidence = pv.get('confidence', 0)
                    conf_str = f"{confidence:.0%}" if confidence else "-"
                    strategy = pv.get('execution_strategy', 'after_only')
                    strategy_label = 'Before/After' if strategy == 'before_after' else 'After Only'

                    if matched_id and matched_id != '-':
                        matched_test_ids.add(matched_id)

                    lines.append(f"**{i}. {ideal}**")
                    lines.append("")

                    matched_str = f"{matched_id} ({matched_title})" if matched_id != '-' and matched_title else matched_id
                    lines.append(f"- **Status:** {status_icon} {status}")
                    lines.append(f"- **Strategy:** {strategy_label}")
                    lines.append(f"- **Matched Test:** {matched_str}")
                    lines.append(f"- **Confidence:** {conf_str}")

                    if strategy == 'before_after':
                        before_action = pv.get('before_action', '')
                        after_action = pv.get('after_action', '')
                        if before_action:
                            lines.append(f"- **Before Action:** {before_action}")
                        if after_action:
                            lines.append(f"- **After Action:** {after_action}")

                    if pv.get('requires_different_session'):
                        lines.append(f"- **Session Switch Required:** {pv.get('session_note', 'Different user login needed')}")

                    if pv.get('execution_note'):
                        lines.append(f"- **Execution Note:** {pv.get('execution_note')}")
                    if status != 'found' and pv.get('reason'):
                        lines.append(f"- **Reason:** {pv.get('reason')}")
                    if pv.get('suggested_manual_step'):
                        lines.append(f"- **Manual Step:** {pv.get('suggested_manual_step')}")

                    lines.append("")

            # Coverage gaps
            gaps = tc.get('coverage_gaps', [])
            if gaps:
                lines.append("**Coverage Gaps:**")
                for gap in gaps:
                    lines.append(f"- {gap}")
                lines.append("")

            # Execution Plan (PRE -> ACTION -> POST sequence)
            plan = execution_plans.get(tc_id, {})
            if isinstance(plan, dict):
                exec_order = plan.get('execution_order', [])
            elif hasattr(plan, 'execution_order'):
                exec_order = plan.execution_order
            else:
                exec_order = []

            if exec_order:
                has_ba = plan.get('has_before_after', False) if isinstance(plan, dict) else getattr(plan, 'has_before_after', False)

                lines.append("#### Execution Plan")
                lines.append("")
                if has_ba:
                    lines.append("> **Strategy:** Run verification tests BEFORE and AFTER the action to compare values.")
                    lines.append("")

                # Phase labels
                phase_labels = {
                    'pre_verify': 'PRE-VERIFY',
                    'navigate': 'NAVIGATE',
                    'session': 'SESSION',
                    'action': 'ACTION',
                    'post_verify': 'POST-VERIFY',
                }

                for step in exec_order:
                    step_num = step.get('step', '?')
                    phase = step.get('phase', '')
                    action = step.get('action', '')
                    test_id = step.get('test_id', '')
                    test_title = step.get('test_title', '')
                    purpose = step.get('purpose', '')
                    note = step.get('note', '')

                    label = phase_labels.get(phase, phase.upper())

                    if test_id:
                        lines.append(f"**{step_num}. [{label}] {test_id}** -- {test_title}")
                    else:
                        lines.append(f"**{step_num}. [{label}]** {purpose}")

                    if note:
                        lines.append(f"   > {note}")
                    elif purpose and test_id:
                        lines.append(f"   > {purpose}")

                    limitation = step.get('limitation', '')
                    if limitation:
                        lines.append(f"   > Limitation: {limitation}")

                    lines.append("")

                # Plan notes
                plan_notes = plan.get('notes', '') if isinstance(plan, dict) else getattr(plan, 'notes', '')
                if plan_notes:
                    lines.append(f"**Notes:** {plan_notes}")
                    lines.append("")

                # Manual steps from the plan
                plan_manual = plan.get('manual_steps', []) if isinstance(plan, dict) else getattr(plan, 'manual_steps', [])
                if plan_manual:
                    lines.append("**Manual Verification Required:**")
                    for ms in plan_manual:
                        if isinstance(ms, dict):
                            lines.append(f"- {ms.get('purpose', '')}")
                            suggested = ms.get('suggested_step', '')
                            if suggested:
                                lines.append(f"  - Suggested: {suggested}")
                        else:
                            lines.append(f"- {ms}")
                    lines.append("")

            else:
                # Fallback: show matched test cases in detail (no execution plan)
                if matched_test_ids:
                    lines.append("#### Matched Test Cases")
                    lines.append("")
                    lines.append("Execute these test cases after the action to verify the result:")
                    lines.append("")

                    for matched_id in matched_test_ids:
                        matched_tc = test_case_lookup.get(matched_id)
                        if matched_tc:
                            m_id = matched_tc.get('id', 'N/A')
                            m_title = matched_tc.get('title', 'N/A')
                            m_preconditions = matched_tc.get('preconditions', 'None')
                            m_steps = matched_tc.get('steps', [])
                            m_expected = matched_tc.get('expected_result', 'N/A')
                            m_priority = matched_tc.get('priority', 'Medium')

                            lines.append(f"##### {m_id}: {m_title}")
                            lines.append("")
                            lines.append(f"- **Priority:** {m_priority}")
                            lines.append(f"- **Preconditions:** {m_preconditions}")
                            lines.append(f"- **Steps:**")
                            for si, step in enumerate(m_steps, 1):
                                lines.append(f"  {si}. {step}")
                            lines.append(f"- **Expected Result:** {m_expected}")
                            lines.append("")

            lines.append("---")
            lines.append("")

    # Navigation Graph Info
    nav_graph = data.get('navigation_graph', {})
    if nav_graph:
        lines.append("## Navigation Graph")
        lines.append("")
        if nav_graph.get('graph_image_path'):
            lines.append(f"![Navigation Graph]({nav_graph['graph_image_path']})")
            lines.append("")

        nodes = nav_graph.get('nodes', [])
        if nodes:
            lines.append("### Pages")
            lines.append("")
            lines.append("| Module | URL | Auth Required | Test Cases |")
            lines.append("|--------|-----|---------------|------------|")
            for node in nodes:
                title = node.get('title', 'N/A')
                url = node.get('url_path', 'N/A')
                auth = 'Yes' if node.get('requires_auth') else 'No'
                tc_count = len(node.get('test_case_ids', []))
                lines.append(f"| {title} | {url} | {auth} | {tc_count} |")
            lines.append("")

    return "\n".join(lines)
