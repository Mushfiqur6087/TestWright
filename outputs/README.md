# Outputs

Generated artifacts from AutoSpecTest and its baselines, organized by:

```
outputs/
└── <system>/            # autospectest | single_prompt | few_shot | ...
    └── <dataset>/       # Parabank | Mifos | MoodleStudent | ...
        └── <model>/     # gpt-4o | gpt-5-mini | gpt-4-mini | ...
            ├── test-cases.json
            ├── test-cases.md
            ├── verifications.json   # if `autospectest verify` was run
            ├── verifications.md
            └── navigation_graph.png
```

This shape makes per-dataset, per-model comparisons across systems trivial to
diff in evaluation scripts and to cite in paper tables.

## Conventional system slugs

| Slug            | Source                              |
|-----------------|-------------------------------------|
| `autospectest`  | The proposed multi-agent framework  |
| `single_prompt` | `baselines/single_prompt/`          |
| `few_shot`      | `baselines/few_shot/`               |

## Conventional model slugs

Model slugs are the model id with `/` replaced by `-` (e.g. `gpt-4o`,
`gpt-5-mini`, `openai-gpt-4o-mini`, `meta-llama-llama-3.1-70b-instruct`).
