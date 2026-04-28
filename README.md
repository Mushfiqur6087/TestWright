# AutoSpecTest

**AutoSpecTest** is a tool for automated test generation from functional
specifications using multi-agent orchestration. It converts a markdown
functional specification into:

- structured test cases in JSON,
- a human-readable Markdown report,
- and a generated navigation graph image.

The framework uses a LangGraph-based multi-agent pipeline and supports multiple
LLM providers. A separate verification module cross-checks generated tests
against the source specification.

## Repository Layout

```
AutoSpecTest/
├── dataset/
│   ├── raw_specifications/      # markdown specs (Mifos, Moodle, Parabank, PHPTravels)
│   └── ground_truth/            # human-written tests for evaluation
├── framework/
│   ├── orchestrator/            # LangGraph pipeline (generator, graph, nodes, state)
│   ├── agents/                  # LLM agents (navigation, summary, test_generator, ...)
│   ├── extractors/              # parser, chunker (spec ingestion)
│   ├── schemas/                 # typed dataclasses + enums
│   └── verification/            # verification planner + pipeline
├── baselines/
│   ├── single_prompt/           # zero-shot ablation (stub)
│   └── few_shot/                # k-shot ablation (stub)
├── exporters/                   # JSON / Markdown formatters
└── outputs/                     # <system>/<dataset>/<model>/ artifacts
```

## Current Scope

This repository supports both generation and verification workflows:

- generate test cases from spec input,
- export generated JSON to Markdown,
- generate verification plans from existing test-cases.json using the main
  spec and optional cross-role specs,
- export verification JSON to Markdown.

## Features

- Multi-agent generation pipeline (parse, chunk, summarize, generate, assemble).
- Multi-agent verification pipeline for creating verification steps from test
  cases and specifications.
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

This installs the CLI command `autospectest` via:

```toml
[project.scripts]
autospectest = "autospectest.cli:main"
```

## Quick Start

### 1. Generate Test Cases

```bash
autospectest --generate \
  --input dataset/raw_specifications/Parabank/Parabank.md \
  --api-key "$OPENAI_API_KEY" \
  --provider openai \
  --model gpt-5-mini
```

By default this writes to `outputs/autospectest/Parabank/gpt-5-mini/`.

### 2. Export JSON to Markdown

```bash
autospectest export-md \
  --input outputs/autospectest/Parabank/gpt-5-mini/test-cases.json
```

### 3. Verify Generated Test Cases

```bash
autospectest verify \
  --input outputs/autospectest/Parabank/gpt-5-mini/test-cases.json \
  --spec dataset/raw_specifications/Parabank/Parabank.md \
  --api-key "$OPENAI_API_KEY" \
  --provider openai \
  --model gpt-4o
```

### 4. Export Verification JSON to Markdown

```bash
autospectest export-verification-md \
  --input outputs/autospectest/Parabank/gpt-5-mini/verifications.json
```

### 5. Run as Module (Alternative)

```bash
python -m autospectest --generate \
  --input dataset/raw_specifications/Parabank/Parabank.md \
  --api-key "$OPENAI_API_KEY"
```

## CLI Reference

### Generate

```bash
autospectest --generate [options]
```

Main options:

- `--input, -i`: path to functional specification markdown file (`.md`)
- `--api-key`: provider API key (required for generation)
- `--provider`: `openai | github | openrouter`
- `--model`: model id (default: `gpt-4o`)
- `--output, -o`: output directory (default:
  `outputs/autospectest/<project>/<model>/`)
- `--debug`: enable debug logging
- `--debug-file`: debug log file path

### Export Markdown

```bash
autospectest export-md --input <test-cases.json> [--output <output.md>]
```

If `--output` is omitted, exporter writes beside input using `.md` suffix.

### Verify

```bash
autospectest verify --input <test-cases.json> --spec <spec.md> --api-key <key> [options]
```

Main options:
- `--input, -i`: path to generated test cases JSON file
- `--spec`: path to the main functional spec markdown file
- `--cross-role-specs`: optional extra specs for cross-role verification
- `--api-key`: provider API key
- `--model`: model id (default: `gpt-4o`)
- `--provider`: `openai | github | openrouter`
- `--output, -o`: output path for `verifications.json`
- `--max-workers`: parallel LLM calls (default: `8`)
- `--debug`: enable debug logging

### Export Verification Markdown

```bash
autospectest export-verification-md --input <verifications.json> [--output <output.md>]
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

Generation writes under `outputs/<system>/<dataset>/<model>/`. See
[`outputs/README.md`](outputs/README.md) for the layout convention.

### 1) `test-cases.json`

Primary machine-readable output. Top-level keys:

- `project_name`
- `base_url`
- `generated_at`
- `navigation_overview`
- `navigation_graph`
- `module_summaries`
- `test_cases`
- `summary`

### 2) `navigation_graph.png`

Rendered page/module graph. If graph libraries are unavailable, generation
continues and image is skipped.

### 3) `test-cases.md` (after `export-md`)

Human-readable report including summary tables and grouped test cases.

### 4) `verifications.json` (after `verify`)

Generated verification plans linking test cases back to specification features.
Includes cross-role steps if `--cross-role-specs` was provided.

### 5) `verifications.md` (after `export-verification-md`)

Human-readable markdown formatted version of the verification plans.

## Architecture

### Pipeline Stages

LangGraph generation pipeline (8 nodes):

```text
parse -> navigation -> chunker -> summary -> test_generation
      -> standard_patterns -> assembler -> finalize
```

### Stage Responsibilities

1. `parse` — converts raw functional input into structured
   modules/workflows/rules.
2. `navigation` — builds logical page graph and route/connectivity metadata.
3. `chunker` — splits module content into workflow-centric chunks.
4. `summary` — builds concise per-module metadata for context and reporting.
5. `test_generation` — generates positive/negative/edge cases per workflow chunk.
6. `standard_patterns` — conditionally adds generic session/RBAC quality tests.
7. `assembler` — deduplicates, sorts, assigns IDs, links tests to nav graph,
   computes summary.
8. `finalize` — creates graph image, validates, exports JSON.

## Module Guide

### `framework/orchestrator/`

- `generator.py` (`TestCaseGenerator`) — top-level orchestrator; prepares
  initial state and runs compiled graph.
- `graph.py` — LangGraph topology definition and compile step.
- `nodes.py` — node functions for each pipeline stage.
- `state.py` — `PipelineState` typed schema with reducer annotations.

### `framework/agents/`

- `base.py` — shared LLM client wrapper, provider routing, debug logging.
- `navigation.py` (`NavigationAgent`) — infers navigation graph, login module,
  connectivity; generates graph PNG.
- `summary.py` (`SummaryAgent`) — creates 2-line module summaries.
- `test_generator.py` (`TestGenerationAgent`) — core scenario generation; enforces
  evidence grounding for negative/edge tests.
- `standard_patterns.py` (`StandardPatternsAgent`) — conditional standard tests
  for session security and RBAC.
- `assembler.py` (`AssemblerAgent`) — dedup, ordering, ID generation, final
  validation.

### `framework/extractors/`

- `parser.py` (`ParserAgent`) — parses functional descriptions into structured
  modules/workflows/rules/behaviors.
- `chunker.py` (`ChunkerAgent`) — maps module data into workflow-specific chunks.

### `framework/schemas/`

- `schemas.py` — dataclasses for all pipeline contracts (`ParsedModule`,
  `ParsedFunctionalDescription`, `ProjectContext`, `WorkflowChunk`,
  `ModuleSummary`, `NavigationNode`, `NavigationGraph`, `TestCase`,
  `TestSuiteOutput`).
- `enums.py` — `TestType`, `Priority` enums.

### `framework/verification/`

- `planner.py` (`VerificationPlannerAgent`) — creates detailed test verification
  steps mapping to functional specs.
- `pipeline.py` — orchestrates verification-plan generation given a generated
  `test-cases.json` and a spec.

### `exporters/`

- `json_exporter.py` — serializes `TestSuiteOutput` to JSON.
- `markdown_exporter.py` — converts JSON output into grouped markdown report.
- `verification_json_exporter.py` — outputs verification plans to JSON.
- `verification_markdown_exporter.py` — formats verification JSON to Markdown.

### `baselines/`

Comparator approaches used as ablations against the multi-agent framework.
See [`baselines/README.md`](baselines/README.md).

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
autospectest --generate ... --debug --debug-file debug_log.txt
```

Debug logs include system prompt snapshots, user prompts, raw model responses,
parsed JSON, and token/latency traces.

## Development Notes

- No automated test suite or linter is currently configured.
- Recommended validation path is running generation on datasets in
  `dataset/raw_specifications/`.
- Deduplication is deterministic and dependency-free (exact + normalized
  title/steps).

## Troubleshooting

### Generation requires API key

If generation exits early, ensure `--api-key` is provided.

### Graph image not generated

Install optional graph libraries (`networkx`, `matplotlib`).

### Export command fails on missing file

Ensure generation completed and `test-cases.json` exists at the provided
`--input` path.
