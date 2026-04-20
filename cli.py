#!/usr/bin/env python3
"""
TestWright CLI - AI-powered test case generation from functional specifications.

Usage:
    testwright --generate --input spec.md --api-key "sk-..." --provider openai --output output/
    testwright export-md --input output/test-cases.json --output output/test-cases.md
"""

import argparse
import sys
from pathlib import Path

import testwright
from testwright.core.generator import TestCaseGenerator
from testwright.core.verification_pipeline import run_verification
from testwright.exporters.markdown_exporter import generate_markdown, load_test_cases
from testwright.exporters.verification_markdown_exporter import (
    generate_verification_markdown,
    load_verifications,
)


def main():
    parser = argparse.ArgumentParser(
        description="TestWright - AI-powered test case generation from functional specifications"
    )
    parser.add_argument("--version", action="version", version=f"testwright {testwright.__version__}")

    subparsers = parser.add_subparsers(dest="command")

    # Generate command (also accessible via --generate flag for backward compat)
    parser.add_argument("--generate", action="store_true", help="Generate test cases")
    parser.add_argument("--input", "-i", help="Path to functional specification markdown file")
    parser.add_argument("--api-key", help="API key for LLM provider")
    parser.add_argument("--model", default="gpt-4o", help="Model to use (default: gpt-4o)")
    parser.add_argument("--provider", default="openai", choices=["openai", "github", "openrouter"],
                       help="LLM provider (default: openai)")
    parser.add_argument("--output", "-o", default="output", help="Output directory (default: output)")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--debug-file", default="debug_log.txt", help="Debug log file path")
    # Export markdown subcommand
    export_parser = subparsers.add_parser("export-md", help="Export test cases JSON to Markdown")
    export_parser.add_argument("--input", "-i", required=True, help="Input JSON file path")
    export_parser.add_argument("--output", "-o", help="Output Markdown file path")

    # Verify subcommand — generates verifications.json from an existing test-cases.json
    verify_parser = subparsers.add_parser(
        "verify",
        help="Generate verification plans from an already-generated test-cases.json",
    )
    verify_parser.add_argument("--input", "-i", required=True, help="Path to test-cases.json")
    verify_parser.add_argument("--spec", required=True, help="Path to main functional spec markdown")
    verify_parser.add_argument(
        "--cross-role-specs",
        nargs="+",
        default=[],
        help="Optional extra spec files for cross-role verification (e.g. MoodleStudent.md)",
    )
    verify_parser.add_argument("--api-key", required=True, help="API key for LLM provider")
    verify_parser.add_argument("--provider", default="openai", choices=["openai", "github", "openrouter"])
    verify_parser.add_argument("--model", default="gpt-4o")
    verify_parser.add_argument("--output", "-o", help="Output path for verifications.json")
    verify_parser.add_argument("--max-workers", type=int, default=8, help="Parallel LLM calls (default: 8)")
    verify_parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    verify_parser.add_argument("--debug-file", default="debug_log.txt", help="Debug log file path")

    # Export verification markdown subcommand
    export_verif_parser = subparsers.add_parser(
        "export-verification-md",
        help="Export verifications JSON to Markdown",
    )
    export_verif_parser.add_argument("--input", "-i", required=True, help="Input verifications.json path")
    export_verif_parser.add_argument("--output", "-o", help="Output Markdown file path")

    args = parser.parse_args()

    if args.command == "export-md":
        return _export_markdown(args)
    elif args.command == "verify":
        return _verify(args)
    elif args.command == "export-verification-md":
        return _export_verification_markdown(args)
    elif args.generate:
        return _generate(args)
    else:
        parser.print_help()
        return 1


def _generate(args):
    """Run the test case generation pipeline."""
    if not args.api_key:
        print("Error: --api-key is required for generation")
        return 1

    if not args.input:
        print("Error: --input is required for generation")
        return 1

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1
    if input_path.is_dir() or input_path.suffix.lower() != ".md":
        print("Error: --input must be a markdown (.md) file")
        return 1

    functional_desc = _load_from_markdown_file(md_path=input_path)

    # Build output path: dataset/<website>/<website>-<model>
    # unless the user explicitly passed --output
    if args.output != "output":
        output_dir = args.output
    else:
        website_name = functional_desc.get("project_name", "output").replace(" ", "_")
        model_slug = args.model.replace("/", "-")
        base_dir = str(input_path.parent)
        output_dir = str(Path(base_dir) / f"{website_name}-{model_slug}")

    print(f"  Output directory: {output_dir}")

    generator = TestCaseGenerator(
        api_key=args.api_key,
        model=args.model,
        provider=args.provider,
        debug=args.debug,
        debug_file=args.debug_file,
    )

    output = generator.generate(functional_desc, output_dir=output_dir)

    print(f"\nGeneration complete!")
    print(f"  Total tests: {output.summary.get('total_tests', 0)}")
    print(f"  Output: {output_dir}/")
    return 0


def _parse_markdown(text: str) -> tuple:
    """Parse a functional spec markdown into (navigation_overview, modules).

    Any ``## Navigation`` section (case-insensitive) is extracted as the
    navigation overview and excluded from the modules list, so it doesn't
    get processed as a page with testable workflows.
    """
    modules = []
    navigation_overview = ""
    module_id = 0

    current_module = None       # {"id", "title", "description"}
    collecting_nav = False      # True while inside the Navigation section

    for line in text.split('\n'):
        if line.startswith('## '):
            # Close whatever section we were building
            if current_module:
                modules.append(current_module)
                current_module = None
            if collecting_nav:
                collecting_nav = False

            title = line[3:].strip()
            if title.lower().startswith('navigation'):
                collecting_nav = True
            else:
                module_id += 1
                current_module = {"id": module_id, "title": title, "description": ""}
        elif collecting_nav:
            navigation_overview += line + "\n"
        elif current_module:
            current_module["description"] += line + "\n"

    # Flush trailing section
    if current_module:
        modules.append(current_module)

    return navigation_overview.strip(), modules


def _load_from_markdown_file(md_path: Path) -> dict:
    """Load functional description from a markdown file."""
    spec_text = md_path.read_text(encoding='utf-8')
    navigation_overview, modules = _parse_markdown(spec_text)

    project_name = md_path.stem.replace('-', ' ').replace('_', ' ').title()

    return {
        "project_name": project_name,
        "website_url": "",
        "navigation_overview": navigation_overview,
        "modules": modules,
    }


def _export_markdown(args):
    """Export test cases from JSON to Markdown."""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1

    output_path = args.output
    if not output_path:
        output_path = input_path.with_suffix('.md')

    print(f"Reading test cases from: {input_path}")
    data = load_test_cases(str(input_path))

    print("Generating Markdown...")
    markdown = generate_markdown(data)

    print(f"Writing to: {output_path}")
    with open(output_path, 'w') as f:
        f.write(markdown)

    test_count = len(data.get('test_cases', []))
    print(f"Done! Exported {test_count} test cases to Markdown.")
    return 0


def _verify(args):
    """Run the standalone verification pipeline."""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"Error: Spec file not found: {spec_path}")
        return 1

    try:
        run_verification(
            test_cases_json_path=str(input_path),
            spec_path=str(spec_path),
            api_key=args.api_key,
            model=args.model,
            provider=args.provider,
            output_path=args.output,
            cross_role_spec_paths=args.cross_role_specs,
            max_workers=args.max_workers,
            debug=args.debug,
            debug_file=args.debug_file,
        )
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    return 0


def _export_verification_markdown(args):
    """Export verifications.json to markdown."""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1

    output_path = args.output
    if not output_path:
        output_path = input_path.with_suffix(".md")

    print(f"Reading verifications from: {input_path}")
    data = load_verifications(str(input_path))

    print("Generating Markdown...")
    markdown = generate_verification_markdown(data, verification_file_path=str(input_path))

    print(f"Writing to: {output_path}")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    record_count = len(data.get("verifications", []))
    print(f"Done! Exported {record_count} verification records to Markdown.")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
