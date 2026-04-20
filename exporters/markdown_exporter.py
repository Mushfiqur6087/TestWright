"""Export test cases from JSON to human-readable Markdown format."""

import json
from collections import defaultdict


def load_test_cases(input_path: str) -> dict:
    """Load test cases from JSON file."""
    with open(input_path, "r", encoding="utf-8") as file:
        return json.load(file)


def escape_md(text: str) -> str:
    """Escape markdown table characters and normalize line breaks."""
    if not text:
        return ""
    escaped = str(text).replace("\n", "<br>")
    return escaped.replace("|", "\\|")


def generate_markdown(data: dict) -> str:
    """Generate markdown content from test case data."""
    lines = []

    lines.append(f"# {data.get('project_name', 'Test Cases')}")
    lines.append("")
    lines.append(f"**Base URL:** {data.get('base_url', 'N/A')}")
    lines.append(f"**Generated:** {data.get('generated_at', 'N/A')}")
    lines.append("")

    summary = data.get("summary", {})
    if summary:
        lines.append("## Summary")
        lines.append("")
        lines.append("| Metric | Count |")
        lines.append("|--------|-------|")
        lines.append(f"| **Total Tests** | {summary.get('total_tests', 0)} |")
        lines.append("")

        by_type = summary.get("by_type", {})
        if by_type:
            lines.append("### By Type")
            lines.append("")
            lines.append("| Type | Count |")
            lines.append("|------|-------|")
            for test_type, count in by_type.items():
                lines.append(f"| {test_type.replace('_', ' ').title()} | {count} |")
            lines.append("")

        by_priority = summary.get("by_priority", {})
        if by_priority:
            lines.append("### By Priority")
            lines.append("")
            lines.append("| Priority | Count |")
            lines.append("|----------|-------|")
            for priority, count in by_priority.items():
                lines.append(f"| {priority} | {count} |")
            lines.append("")

    lines.append("---")
    lines.append("")

    test_cases = data.get("test_cases", [])
    modules = defaultdict(list)
    for test_case in test_cases:
        module_title = test_case.get("module_title", "Unknown")
        modules[module_title].append(test_case)

    lines.append("## Test Cases")
    lines.append("")

    type_order = ["positive", "negative", "edge_case", "standard"]
    type_labels = {
        "positive": "Functional Tests",
        "negative": "Negative Tests",
        "edge_case": "Edge Case Tests",
        "standard": "Standard Quality Patterns",
    }

    for module_title, cases in modules.items():
        lines.append(f"### {module_title}")
        lines.append("")

        by_type = defaultdict(list)
        for test_case in cases:
            by_type[test_case.get("test_type", "other")].append(test_case)

        for test_type in type_order:
            if test_type not in by_type:
                continue

            lines.append(f"#### {type_labels.get(test_type, test_type.title())}")
            lines.append("")
            lines.append("| TC ID | Test Case | Preconditions | Steps | Expected Result | Priority |")
            lines.append("|-------|-----------|---------------|-------|-----------------|----------|")

            for test_case in by_type[test_type]:
                tc_id = test_case.get("id", "N/A")
                title = escape_md(test_case.get("title", "N/A"))
                preconditions = escape_md(test_case.get("preconditions", "None"))
                steps = test_case.get("steps", [])
                steps_str = "<br>".join([
                    f"{idx + 1}. {escape_md(step)}"
                    for idx, step in enumerate(steps)
                ])
                expected = escape_md(test_case.get("expected_result", "N/A"))
                priority = test_case.get("priority", "Medium")

                lines.append(
                    f"| {tc_id} | {title} | {preconditions} | {steps_str} | {expected} | {priority} |"
                )

            lines.append("")

        lines.append("---")
        lines.append("")

    nav_graph = data.get("navigation_graph", {})
    if nav_graph:
        lines.append("## Navigation Graph")
        lines.append("")

        if nav_graph.get("graph_image_path"):
            lines.append(f"![Navigation Graph]({nav_graph['graph_image_path']})")
            lines.append("")

        nodes = nav_graph.get("nodes", [])
        if nodes:
            lines.append("### Pages")
            lines.append("")
            lines.append("| Module | URL | Test Cases |")
            lines.append("|--------|-----|------------|")

            for node in nodes:
                title = node.get("title", "N/A")
                url = node.get("url_path", "N/A")
                tc_count = len(node.get("test_case_ids", []))
                lines.append(f"| {title} | {url} | {tc_count} |")

            lines.append("")

    return "\n".join(lines)
