# Baselines

Comparator approaches used as **ablations** in the AutoSpecTest evaluation.
Each subdirectory implements one prompting strategy that does **not** use the
multi-agent orchestration pipeline, so we can quantify how much of
AutoSpecTest's quality comes from agent decomposition vs. raw LLM capacity.

All baselines must:
1. Read a functional specification from
   `dataset/raw_specifications/<project>/<spec>.md`.
2. Produce a `test-cases.json` whose schema matches
   [`framework/schemas/schemas.py`](../framework/schemas/schemas.py)
   (`TestSuiteOutput`) so the existing [`exporters/`](../exporters/)
   work unchanged.
3. Write outputs under
   `outputs/<system>/<dataset>/<model>/test-cases.json` where `<system>` is the
   slug of the baseline directory (e.g. `single_prompt`, `few_shot`).

## Slugs

| Subdir              | System slug      | Status |
|---------------------|------------------|--------|
| `single_prompt/`    | `single_prompt`  | stub   |
| `few_shot/`         | `few_shot`       | stub   |
