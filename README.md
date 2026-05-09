# AutoSpecTest

Convert natural-language functional specifications into structured, machine-readable UI Abstract Syntax Trees (UI-AST). The UI-AST captures every interactive element — forms, buttons, tabs, wizards, data tables, conditional logic, and state-bound actions — in a deterministic JSON schema ready for test generation or automated validation.

---

## How it works

A functional spec markdown file goes in; two JSON files come out.

```
spec.md (## Module sections)
    │
    ▼
┌──────────────────────────────────────────────────────────┐
│  AutoSpecTest Pipeline                                   │
│                                                          │
│  ┌─────────────────────────────────────────────────┐     │
│  │  [1/3] generate_and_critique (parallel)         │     │
│  │                                                 │     │
│  │  For each module (concurrent):                  │     │
│  │    attempt 1: UIASTAgent → SemanticCritic       │     │
│  │      verdict=yes  ───────────────────► done     │     │
│  │      verdict=retry → fixes[] fed back           │     │
│  │    attempt 2: UIASTAgent(fixes) → Critic        │     │
│  │      verdict=yes  ───────────────────► done     │     │
│  │      verdict=retry → fixes[] fed back           │     │
│  │    attempt 3: UIASTAgent(fixes) → ship as-is   │     │
│  └─────────────────────────────────────────────────┘     │
│                          ↓                               │
│  ┌─────────────────────────────────────────────────┐     │
│  │  [2/3] generate_tests (parallel, 3 calls each)  │     │
│  │                                                 │     │
│  │  For each module (concurrent):                  │     │
│  │    TestPositiveAgent  ┐                         │     │
│  │    TestNegativeAgent  ├─ parallel → merge       │     │
│  │    TestEdgeAgent      ┘                         │     │
│  └─────────────────────────────────────────────────┘     │
│                          ↓                               │
│  ┌──────────────────────────┐                            │
│  │  [3/3] finalize          │ → ui-ast.json              │
│  │                          │ → semantic-critique.json   │
│  │                          │ → test-cases.json          │
│  └──────────────────────────┘                            │
└──────────────────────────────────────────────────────────┘
```

**Stage 1 — UIASTAgent + SemanticCriticAgent** — For each module, the generator emits a UI component tree and the critic audits it with a binary `yes/retry` verdict. On retry, the critic's `fixes[]` array is fed directly back to the generator. Maximum 3 attempts per module.

**Stage 2 — Three test agents** — For each module, three agents run in parallel against the approved AST: positive tests (happy paths, state transitions, lifecycle flows), negative tests (validation failures, constraint violations, precondition violations), and edge/boundary tests (threshold boundaries, unusual interaction paths). Results are merged into a single per-module test suite with sequential TC IDs.

Modules run concurrently across all stages.

---

## Installation

**Requirements:** Python 3.9+

```bash
git clone https://github.com/your-org/AutoSpecTest
cd AutoSpecTest
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

After installation, the `autospectest` command is available in the venv.

---

## Quick start

```bash
autospectest --generate \
  --input dataset/raw_specifications/my-app-spec.md \
  --api-key "sk-..." \
  --model "openai/gpt-4o" \
  --output outputs/my-run
```

This writes three files to `outputs/my-run/`:
- `ui-ast.json` — the generated UI-AST
- `semantic-critique.json` — the critic's final verdict and audit for each module
- `test-cases.json` — merged positive/negative/edge test cases for each module

---

## Input format

The input is a markdown file. Each `## ` heading becomes one module. A `## Navigation` section is extracted as metadata and not processed as a module.

```markdown
# My Application

## Navigation
Sidebar with links to Clients, Reports, Settings.

## Clients
The Clients page is a data table with columns Name, Status, Account Number.
Rows have a three-dot menu with View and Deactivate (only when Status is Active).
A checkbox column enables bulk Export. The table is sortable by Name and Status.

## Create Client
A wizard with 3 steps: Basic Info, Contact, Review.
Step 1 collects First Name (required), Last Name (required), Email (required, must be valid email).
Step 2 collects Phone, Address (required).
Step 3 is read-only review. Submit creates the client in Pending status.
```

The file stem (e.g. `my-app-spec`) becomes the project name in the output.

---

## CLI reference

```
autospectest --generate --input SPEC --api-key KEY [options]
autospectest --resume RUN_ID --api-key KEY
```

| Flag | Default | Description |
|------|---------|-------------|
| `--input` / `-i` | — | Path to `.md` spec file (required for `--generate`) |
| `--api-key` | — | API key for the LLM provider |
| `--model` | `openai/gpt-4o` | LiteLLM model string (must include provider prefix) |
| `--output` / `-o` | `outputs/autospectest/<project>/<model>/` | Output directory |
| `--max-concurrency` | `10` | Max concurrent in-flight LLM calls |
| `--debug` | off | Write per-stage debug logs to `<output>/debug/` |
| `--resume RUN_ID` | — | Resume an interrupted run from its checkpoint |
| `--version` | — | Print version and exit |

---

## LLM providers

All LLM calls go through [LiteLLM](https://github.com/BerriAI/litellm). The `--model` flag accepts any LiteLLM model string with a provider prefix:

```bash
# OpenAI
--model openai/gpt-4o
--model openai/gpt-4o-mini

# Anthropic
--model anthropic/claude-3-5-sonnet-20241022

# OpenRouter (proxies 100+ models)
--model openrouter/anthropic/claude-3.5-sonnet
--model openrouter/openai/gpt-4o

# GitHub Models
--model github/gpt-4o
```

The `--api-key` value is passed directly to LiteLLM and must match the provider (OpenAI key for OpenAI models, Anthropic key for Anthropic, OpenRouter key for OpenRouter, etc.).

Parameters unsupported by a given model (e.g. `temperature` on o-series models) are silently dropped — no manual per-model configuration needed.

---

## Output files

### `ui-ast.json`

```json
{
  "project_name": "My Application",
  "generated_at": "2026-05-03T12:00:00Z",
  "modules": [
    {
      "module_id": 1,
      "module_title": "Clients",
      "ast": {
        "module_name": "Clients",
        "components": {
          "Clients_Table": {
            "type": "data_table",
            "sortable_columns": ["Name", "Status"],
            "row_actions": [
              { "action_name": "View" },
              { "action_name": "Deactivate", "preconditions": ["status must be Active"] }
            ],
            "bulk_actions": [{ "action_name": "Export" }]
          }
        }
      },
      "attempts": 1
    }
  ]
}
```

### `semantic-critique.json`

```json
{
  "project_name": "My Application",
  "generated_at": "2026-05-03T12:00:00Z",
  "modules": [
    {
      "module_id": 1,
      "module_title": "Clients",
      "critique": {
        "verdict": "yes",
        "summary": "All interactive elements captured correctly.",
        "missing": [],
        "phantoms": [],
        "fixes": []
      },
      "forced_ship": false
    }
  ]
}
```

**`forced_ship: true`** means the module hit the 3-attempt cap — the final attempt's output was shipped regardless of the critic's verdict. Check `critique.missing` and `critique.fixes` to understand what to fix in the spec or prompt.

---

### `test-cases.json`

```json
{
  "project_name": "My Application",
  "generated_at": "2026-05-03T12:00:00Z",
  "model": "openai/gpt-4o",
  "modules": [
    {
      "module": "Clients",
      "test_cases": [
        {
          "tc_id": "TC-001",
          "category": "positive",
          "test_case": "View client with all fields filled",
          "preconditions": ["User logged in", "At least one client exists"],
          "steps": ["Navigate to Clients page", "Click View on any row"],
          "expected_result": "Client detail page opens showing all client information",
          "priority": "high"
        },
        {
          "tc_id": "TC-010",
          "category": "negative",
          "test_case": "Attempt Deactivate on already Inactive client",
          "preconditions": ["User logged in", "Client in Inactive status"],
          "steps": ["Open client detail page", "Observe action bar"],
          "expected_result": "Deactivate action is not available",
          "priority": "high"
        },
        {
          "tc_id": "TC-015",
          "category": "edge",
          "subcategory": "interaction_edge",
          "test_case": "Double-click Export button on bulk selection",
          "preconditions": ["User logged in", "Multiple clients exist"],
          "steps": ["Select 3 clients via checkbox", "Double-click Export"],
          "expected_result": "Export triggered once, not twice",
          "priority": "low"
        }
      ],
      "summary": {
        "total": 18,
        "positive": 8,
        "negative": 6,
        "boundary": 2,
        "edge": 2,
        "high_priority": 10,
        "medium_priority": 6,
        "low_priority": 2
      }
    }
  ],
  "total_summary": {
    "total_modules": 1,
    "total_tests": 18,
    "positive": 8,
    "negative": 6,
    "boundary": 2,
    "edge": 2,
    "high_priority": 10,
    "medium_priority": 6,
    "low_priority": 2
  }
}
```

Each test case has `category` (`positive | negative | edge`) set automatically during merge. Edge test cases also carry `subcategory` (`boundary | input_edge | interaction_edge | state_edge | data_edge`). TC IDs are renumbered sequentially across all categories within each module.

---

## UI-AST schema

The AST captures **interactive elements only**. The critic enforces this — passive display labels ("the page shows the client name") produce zero expected items and are not emitted.

| Component type | Used for |
|---|---|
| `form` | Single-page forms with `fields` |
| `wizard` | Multi-step forms with `steps[]`, each step has `fields` |
| `tab_container` | Pages with `tabs[]`, each tab has `fields` and can nest more `tabs[]` |
| `data_table` | Tables with `row_actions[]`, `bulk_actions[]`, `sortable_columns[]` |
| `state_bound_action_bar` | Action buttons that change by entity state (Pending/Active/Closed) with `states{}` |
| `repeating_group` | Add-row patterns; has `item_fields{}`, optional `min`/`max` |

Field-level attributes: `type`, `required`, `required_when`, `visible_when`, `enabled_when`, `options[]`, `constraints[]`.

Action-level attributes: `on_success`, `preconditions[]`, `fields{}` (for modal/inline forms triggered by the action).

---

## Resumability

Every run gets a unique run ID (`<project>-YYYYMMDD-HHmmss-<6char>`). If a run is interrupted mid-pipeline, resume it with:

```bash
autospectest --resume my-app-20260503-120000-abc123 --api-key "sk-..."
```

The run ID is printed at the start of every `--generate` invocation. Checkpoints are stored in `outputs/.checkpoints/autospectest.sqlite`; sidecar metadata (original inputs) lives in `outputs/.checkpoints/<run-id>.json`.

---

## Debug mode

```bash
autospectest --generate --input spec.md --api-key "..." --model openai/gpt-4o \
  --output outputs/debug-run --debug
```

With `--debug`, two log files are written to `outputs/debug-run/debug/`:

| File | Contents |
|------|----------|
| `01_ui_ast.log` | System prompt, user prompt, and raw LLM response for every UIASTAgent call |
| `02_semantic_critic.log` | Same for every SemanticCriticAgent call |

Useful for diagnosing why the critic keeps retrying or why a particular field is missing.

---

## Docker

```bash
docker build -t autospectest .

# Mount a host directory for outputs
docker run --rm \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/dataset:/app/dataset \
  autospectest \
  --generate \
  --input dataset/raw_specifications/my-spec.md \
  --api-key "sk-..." \
  --model openai/gpt-4o
```

The Docker image installs dependencies in a separate layer so source-only changes rebuild in seconds. Runs as a non-root user to avoid root-owned output files on bind mounts.

---

## Dataset and baselines

- `dataset/raw_specifications/` — Input markdown specs
- `dataset/ground_truth/` — Reference UI-AST outputs for evaluation
- `baselines/` — Single-prompt and few-shot reference implementations for ablation studies; see `baselines/README.md`

---

## Concurrency tuning

`--max-concurrency` controls how many LLM calls can be in-flight simultaneously across all modules. The default of 10 is safe for most providers. Lower it if you hit rate limits; raise it for providers with high per-minute token quotas.

The retry loop means a single module can make up to 6 LLM calls (3 generator + 3 critic). With 10 modules and `--max-concurrency 10`, peak concurrency is bounded at 10 regardless of how many modules are retrying simultaneously.
