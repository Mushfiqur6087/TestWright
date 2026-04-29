# AutoSpecTest

Automated test case generation from functional specifications using a
multi-agent LangGraph pipeline. Give it a markdown spec; it produces structured
test cases (JSON + Markdown) and an optional navigation graph image.

## Requirements

- [Docker](https://docs.docker.com/get-docker/)
- An API key for your LLM provider (OpenAI, OpenRouter, GitHub Models, …)

## Quick Start

```bash
git clone https://github.com/<you>/AutoSpecTest.git
cd AutoSpecTest
docker build -t autospectest .
```

Run generation against one of the bundled specs:

```bash
docker run --rm \
  -v "$(pwd)/outputs:/app/outputs" \
  autospectest \
  --generate \
  --input dataset/raw_specifications/Parabank/Parabank.md \
  --api-key "$OPENAI_API_KEY" \
  --model openai/gpt-4o
```

Results are written to `./outputs/autospectest/Parabank/openai-gpt-4o/` on your
host machine.

To use **your own spec file**, mount it into the container:

```bash
docker run --rm \
  -v "$(pwd)/outputs:/app/outputs" \
  -v "$(pwd)/myspec.md:/app/myspec.md:ro" \
  autospectest \
  --generate \
  --input myspec.md \
  --api-key "$OPENAI_API_KEY" \
  --model openai/gpt-4o
```

## Model Strings

AutoSpecTest uses [LiteLLM](https://docs.litellm.ai) model strings —
`provider/model-name`. Examples:

| Provider | `--model` value |
|---|---|
| OpenAI | `openai/gpt-4o` |
| OpenRouter | `openrouter/anthropic/claude-3.5-sonnet` |
| GitHub Models | `github/gpt-4o` |

## Commands

All commands follow the same `docker run` pattern. Replace the arguments after
the image name.

### Generate test cases

```bash
docker run --rm \
  -v "$(pwd)/outputs:/app/outputs" \
  autospectest \
  --generate \
  --input dataset/raw_specifications/Parabank/Parabank.md \
  --api-key "$OPENAI_API_KEY" \
  --model openai/gpt-4o
```

On start the tool prints a `run_id`. If the run is interrupted, resume it with:

```bash
docker run --rm \
  -v "$(pwd)/outputs:/app/outputs" \
  autospectest \
  --resume <run_id> \
  --api-key "$OPENAI_API_KEY"
```

Optional flags:

| Flag | Default | Description |
|---|---|---|
| `--output, -o` | auto | Override output directory |
| `--max-concurrency` | `10` | Max parallel LLM calls |
| `--debug` | off | Write verbose debug log alongside the other outputs |
| `--debug-file` | `<output-dir>/debug_log.txt` | Override debug log path |

To run with debug logging (log lands in the same output directory as `test-cases.json`):

```bash
docker run --rm \
  -v "$(pwd)/outputs:/app/outputs" \
  autospectest \
  --generate \
  --input dataset/raw_specifications/Parabank/Parabank.md \
  --api-key "$OPENAI_API_KEY" \
  --model openai/gpt-4o \
  --debug
```

### Export test cases to Markdown

```bash
docker run --rm \
  -v "$(pwd)/outputs:/app/outputs" \
  autospectest \
  export-md \
  --input outputs/autospectest/Parabank/openai-gpt-4o/test-cases.json
```

Output defaults to the same directory with a `.md` suffix.

### Verify test cases against the spec

```bash
docker run --rm \
  -v "$(pwd)/outputs:/app/outputs" \
  autospectest \
  verify \
  --input outputs/autospectest/Parabank/openai-gpt-4o/test-cases.json \
  --spec dataset/raw_specifications/Parabank/Parabank.md \
  --api-key "$OPENAI_API_KEY" \
  --model openai/gpt-4o
```

Optional: `--cross-role-specs <file> [<file> ...]` for multi-role specs,
`--max-workers N` (default `8`).

### Export verification results to Markdown

```bash
docker run --rm \
  -v "$(pwd)/outputs:/app/outputs" \
  autospectest \
  export-verification-md \
  --input outputs/autospectest/Parabank/openai-gpt-4o/verifications.json
```

## Bundled Specs

The image includes four real-world specs under `dataset/raw_specifications/`:

| Project | Path |
|---|---|
| Parabank | `dataset/raw_specifications/Parabank/Parabank.md` |
| Moodle (teacher) | `dataset/raw_specifications/Moodle/MoodleTeacher.md` |
| Moodle (student) | `dataset/raw_specifications/Moodle/MoodleStudent.md` |
| PHPTravels | `dataset/raw_specifications/PHPTravels/PHPTravels.md` |
| Mifos | `dataset/raw_specifications/Mifos/Mifos.md` |

## Output Layout

```
outputs/
└── autospectest/
    └── <project>/
        └── <model>/
            ├── test-cases.json       # machine-readable test suite
            ├── test-cases.md         # human-readable report (after export-md)
            ├── navigation_graph.png  # page-connectivity graph
            ├── verifications.json    # verification plans (after verify)
            ├── verifications.md      # verification report (after export-verification-md)
            └── debug_log.txt         # verbose LLM log (only with --debug; gitignored)
```

Interrupted run checkpoints are stored under `outputs/.checkpoints/` and can
be safely deleted once a run completes successfully.
