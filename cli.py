#!/usr/bin/env python3
"""
TestWright CLI - AI-powered test case generation from functional specifications.

Usage:
    testwright --generate --input spec.json --api-key "sk-..." --provider openai --output output/
    testwright export-md --input output/test-cases.json --output output/test-cases.md
"""

import argparse
import json
import sys
from pathlib import Path

import testwright
from testwright.core.generator import TestCaseGenerator
from testwright.exporters.markdown_exporter import load_test_cases, generate_markdown


def main():
    parser = argparse.ArgumentParser(
        description="TestWright - AI-powered test case generation from functional specifications"
    )
    parser.add_argument("--version", action="version", version=f"testwright {testwright.__version__}")

    subparsers = parser.add_subparsers(dest="command")

    # Generate command (also accessible via --generate flag for backward compat)
    parser.add_argument("--generate", action="store_true", help="Generate test cases")
    parser.add_argument("--input", "-i", help="Path to functional description directory or JSON file")
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

    args = parser.parse_args()

    if args.command == "export-md":
        return _export_markdown(args)
    elif args.generate:
        return _generate(args)
    else:
        parser.print_help()
        return 1


def _generate(args):
    """Run the test case generation pipeline."""
    if not args.input:
        print("Error: --input is required for generation")
        return 1
    if not args.api_key:
        print("Error: --api-key is required for generation")
        return 1

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path not found: {input_path}")
        return 1

    # Build functional description from input
    if input_path.is_dir():
        functional_desc = _load_from_directory(input_path)
    else:
        with open(input_path, 'r') as f:
            functional_desc = json.load(f)

    generator = TestCaseGenerator(
        api_key=args.api_key,
        model=args.model,
        provider=args.provider,
        debug=args.debug,
        debug_file=args.debug_file,
    )

    output = generator.generate(functional_desc, output_dir=args.output)

    print(f"\nGeneration complete!")
    print(f"  Total tests: {output.summary.get('total_tests', 0)}")
    print(f"  Output: {args.output}/")
    return 0


def _load_from_directory(dir_path: Path) -> dict:
    """Load functional description from a directory of markdown files."""
    spec_file = dir_path / "functional_specification.md"
    nav_file = dir_path / "navigation.md"
    mock_file = dir_path / "mock_data.md"

    if not spec_file.exists():
        print(f"Error: functional_specification.md not found in {dir_path}")
        sys.exit(1)

    # Read the specification
    spec_text = spec_file.read_text(encoding='utf-8')

    # Parse modules from markdown headings
    modules = []
    current_module = None
    module_id = 0

    for line in spec_text.split('\n'):
        if line.startswith('## '):
            if current_module:
                modules.append(current_module)
            module_id += 1
            title = line[3:].strip()
            current_module = {
                "id": module_id,
                "title": title,
                "description": ""
            }
        elif current_module:
            current_module["description"] += line + "\n"

    if current_module:
        modules.append(current_module)

    # Read navigation overview
    navigation_overview = ""
    if nav_file.exists():
        navigation_overview = nav_file.read_text(encoding='utf-8')

    # Read mock data
    mock_data = ""
    if mock_file.exists():
        mock_data = mock_file.read_text(encoding='utf-8')

    # Build the project name from directory name
    project_name = dir_path.name.replace('-', ' ').replace('_', ' ').title()

    return {
        "project_name": project_name,
        "website_url": "",
        "navigation_overview": navigation_overview,
        "mock_data": mock_data,
        "modules": modules
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


if __name__ == "__main__":
    sys.exit(main() or 0)
