# Few-Shot Baseline (stub)

Same shape as the single-prompt baseline, but with **k in-context exemplars**
sourced from `dataset/ground_truth/`. Tests how much of the gap between
single-prompt and AutoSpecTest is closed simply by giving the model concrete
examples of well-formed test cases.

## Planned interface

```bash
python -m baselines.few_shot \
  --input dataset/raw_specifications/Parabank/Parabank.md \
  --shots dataset/ground_truth/Mifos.md dataset/ground_truth/Parabank.md \
  --k 3 \
  --api-key "$OPENAI_API_KEY" \
  --provider openai \
  --model gpt-4o
```

Writes to `outputs/few_shot/<project>/<model>/test-cases.json`.

## Implementation notes

- Sample exemplars from `dataset/ground_truth/` excluding the project under
  test (no train/test leakage).
- Document `k` and the exemplar selection method in the paper — both matter for
  reproducibility.
- Reuse `autospectest.framework.agents.base.BaseAgent` for the LLM call.

**Status:** stub.
