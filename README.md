# TestWright

TestWright is an AI-powered test case generation tool.

It converts a functional specification into:

- structured test cases in JSON,
- a human-readable Markdown report,
- and a generated navigation graph image.

The project uses a LangGraph-based multi-agent pipeline and supports multiple LLM providers.

## Current Scope

This repository is currently configured for **generation-only** flow:

- generate test cases from spec input,
- export generated JSON to Markdown.

Post-verification pipeline components are not part of the active architecture.

## Features

- Multi-agent generation pipeline (parse, chunk, summarize, generate, assemble).
- Provider support: OpenAI, GitHub Models, OpenRouter.
- Mixed test types: positive, negative, edge_case, standard.
- Built-in standard quality patterns (session and RBAC) when applicable.
- Deterministic deduplication and ID assignment.
- Navigation graph extraction and optional PNG visualization.
- JSON and Markdown outputs.

## Requirements

- Python 3.9+
- Network access to chosen LLM provider

Runtime dependencies (from `pyproject.toml`):

- `langgraph`
- `httpx`

Optional (for navigation graph image rendering):

- `networkx`
- `matplotlib`
- `scipy` (optional layout enhancement; graceful fallback exists)

## Installation

```bash
pip install -e .
```

This installs the CLI command `testwright` via:

```toml
[project.scripts]
testwright = "testwright.cli:main"
```

## Quick Start

### 1. Generate Test Cases

```bash
testwright --generate \
  --input Dataset/Parabank/Parabank.md \
  --api-key "$OPENAI_API_KEY" \
  --provider openai \
  --model gpt-5-mini \
  --output Output/Parabank
```

### 2. Export JSON to Markdown

```bash
testwright export-md \
  --input Output/Parabank/test-cases.json \
  --output Output/Parabank/test-cases.md
```

### 3. Run as Module (Alternative)

```bash
python -m testwright --generate --input Dataset/Parabank/Parabank.md --api-key "$OPENAI_API_KEY"
```

## CLI Reference

### Generate

```bash
testwright --generate [options]
```

Main options:

- `--input, -i`: path to functional specification markdown file (`.md`)
- `--api-key`: provider API key (required for generation)
- `--provider`: `openai | github | openrouter`
- `--model`: model id (default: `gpt-4o`)
- `--output, -o`: output directory
- `--debug`: enable debug logging
- `--debug-file`: debug log file path

### Export Markdown

```bash
testwright export-md --input <test-cases.json> [--output <output.md>]
```

If `--output` is omitted, exporter writes beside input using `.md` suffix.

## Input Format

Generation accepts markdown functional specification files only.

### Functional Specification (`--input`)

- Must be a `.md` file.
- Parsed into modules using `## <Section Title>` headings.
- If a `## Navigation` section exists, it is extracted as navigation overview.

### Mock Data

`mock_data` is not used by the active generation pipeline.

## Output Artifacts

Generation writes to your chosen output directory.

### 1) `test-cases.json`

Primary machine-readable output.

Top-level keys:

- `project_name`
- `base_url`
- `generated_at`
- `navigation_overview`
- `navigation_graph`
- `module_summaries`
- `test_cases`
- `summary`

### 2) `navigation_graph.png`

Rendered page/module graph. If graph libraries are unavailable, generation continues and image is skipped.

### 3) `test-cases.md` (after export command)

Human-readable report including summary tables and grouped test cases.

## Output Data Contracts

### Test Case Object

Each entry in `test_cases` contains:

- `id` (assigned by assembler, e.g. `5.TRAFUN-001`)
- `title`
- `module_id`
- `module_title`
- `workflow`
- `test_type` (`positive | negative | edge_case | standard`)
- `priority` (`High | Medium | Low`)
- `preconditions`
- `steps` (list of strings)
- `expected_result`
- optional `spec_evidence` (used for grounded negative/edge tests)

### Navigation Graph

`navigation_graph` contains:

- `login_module_id`
- `graph_image_path`
- `nodes[]`, each with:
  - `module_id`
  - `title`
  - `requires_auth`
  - `url_path`
  - `connected_to[]`
  - `test_case_ids[]`

### Summary

`summary` contains counters:

- `total_tests`
- `by_type`
- `by_priority`
- `by_module`

## Architecture

### Pipeline Stages

Current LangGraph pipeline (8 nodes):

```text
parse -> navigation -> chunker -> summary -> test_generation
      -> standard_patterns -> assembler -> finalize
```

### Stage Responsibilities

1. `parse`
   - converts raw functional input into structured modules/workflows/rules.
2. `navigation`
   - builds logical page graph and route/connectivity metadata.
3. `chunker`
   - splits module content into workflow-centric chunks.
4. `summary`
   - builds concise per-module metadata for context and reporting.
5. `test_generation`
   - generates positive/negative/edge cases per workflow chunk.
6. `standard_patterns`
   - conditionally adds generic session/RBAC quality tests.
7. `assembler`
   - deduplicates, sorts, assigns IDs, links tests to nav graph, computes summary.
8. `finalize`
   - creates graph image, validates, exports JSON.

## Directory and Module Guide

### Top-Level Files

- `cli.py`
  - CLI entry implementation: parse args, load input, run generator, export markdown.
- `__main__.py`
  - `python -m testwright` entrypoint.
- `__init__.py`
  - package exports and version.
- `pyproject.toml`
  - package metadata, dependencies, script entrypoint.
- `CLAUDE.md`
  - repository guidance doc for code-assistant workflows.

### `agents/`

- `base.py`
  - shared LLM client wrapper, provider routing, debug logging, JSON parsing helper.
- `parser.py` (`ParserAgent`)
  - parses functional descriptions into structured modules/workflows/rules/behaviors.
  - extracts explicit system constraints.
- `navigation.py` (`NavigationAgent`)
  - infers navigation graph, login module, connectivity; generates graph PNG.
- `chunker.py` (`ChunkerAgent`)
  - maps module data into workflow-specific chunks.
- `summary.py` (`SummaryAgent`)
  - creates 2-line module summaries plus verify/action state metadata.
- `test_generator.py` (`TestGenerationAgent`)
  - core scenario generation logic and prompt policy.
  - enforces evidence grounding for negative/edge tests.
- `standard_patterns.py` (`StandardPatternsAgent`)
  - emits conditional standard tests for session security and RBAC.
- `assembler.py` (`AssemblerAgent`)
  - dedup, ordering, ID generation, summary creation, and final validation.
- `__init__.py`
  - agent exports.

### `core/`

- `generator.py` (`TestCaseGenerator`)
  - top-level orchestrator; prepares initial state and runs compiled graph.
- `graph.py`
  - LangGraph topology definition and compile step.
- `nodes.py`
  - node functions for each pipeline stage.
- `state.py`
  - `PipelineState` typed schema with reducer annotations.
- `__init__.py`
  - core exports.

### `models/`

- `schemas.py`
  - dataclasses for all pipeline contracts:
    - `ParsedModule`, `ParsedFunctionalDescription`
    - `ProjectContext`, `WorkflowChunk`
    - `ModuleSummary`
    - `NavigationNode`, `NavigationGraph`
    - `TestCase`, `TestSuiteOutput`
- `enums.py`
  - `TestType`, `Priority` enums.
- `__init__.py`
  - model exports.

### `exporters/`

- `json_exporter.py`
  - serializes `TestSuiteOutput` to JSON.
- `markdown_exporter.py`
  - converts JSON output into grouped markdown report.
- `__init__.py`
  - exporter exports.

### Data and Output Folders

- `Dataset/`
  - example real-world markdown specifications (`Parabank`, `Moodle`, `PHPTravels`, `Mifos`).
- `Output/`
  - generated artifacts (JSON, PNG, optional Markdown exports).

### Packaging Metadata

- `testwright.egg-info/`
  - generated packaging metadata from editable install.

## Provider Integration

`BaseAgent` supports:

- `openai` -> `https://api.openai.com/v1`
- `github` -> `https://models.inference.ai.azure.com`
- `openrouter` -> `https://openrouter.ai/api/v1`

Model-token behavior:

- `gpt-5` and `o*` models use `max_completion_tokens`.
- other models use `max_tokens`.

## Debug Logging

Enable with:

```bash
testwright --generate ... --debug --debug-file debug_log.txt
```

Debug logs include:

- system prompt snapshots,
- user prompts,
- raw model responses,
- parsed JSON,
- token/latency traces.

## Development Notes

- No automated test suite or linter is currently configured.
- Recommended validation path is running generation on datasets in `Dataset/`.
- Deduplication is deterministic and dependency-free (exact + normalized title/steps).

## Troubleshooting

### Generation requires API key

If generation exits early, ensure `--api-key` is provided.

### Graph image not generated

Install optional graph libraries (`networkx`, `matplotlib`).

### Export command fails on missing file

Ensure generation completed and `test-cases.json` exists at the provided `--input` path.
