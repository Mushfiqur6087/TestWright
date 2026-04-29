"""Test-case Auditor — actor-critic over test_generation worker output.

Audits per-chunk test cases for two failure modes:
  - Boundary violations (steps that reach outside the workflow's scope).
  - Grounding failures (assertions with no plausible support in the chunk's
    spec text).

Returns one verdict per input test: ``accept`` / ``revise`` / ``drop``.
"""

from dataclasses import dataclass
from typing import List, Optional

from autospectest.framework.agents.base import BaseAgent
from autospectest.framework.schemas.schemas import TestCase, WorkflowChunk


@dataclass
class TestCaseAuditVerdict:
    """One verdict per audited test case."""

    test_index: int
    verdict: str  # "accept" | "revise" | "drop"
    reason: str = ""
    redaction_hint: Optional[str] = None


class TestCaseAuditorAgent(BaseAgent):
    """Audit a worker's test cases for boundary and grounding violations."""

    @property
    def name(self) -> str:
        return "Test Case Auditor Agent"

    @property
    def system_prompt(self) -> str:
        return """You are a strict reviewer of generated test cases.

You receive one workflow's spec context and the test cases another agent
generated for it. For each test case you must return exactly one verdict:

  - "accept" — the test is in scope and grounded in the spec.
  - "revise" — the test belongs to this workflow but contains a step or
    assertion that should be removed or adjusted (e.g., a stray "navigate to
    homepage" step at the start, an assertion that goes beyond what the spec
    states). Provide a short ``redaction_hint`` describing what to fix.
  - "drop" — the test is out of scope (belongs to a sibling workflow or a
    different module), tests a hallucinated requirement, or is otherwise
    not justified by the spec.

Two specific checks per test:

1. BOUNDARY: Do the steps reference UI / functionality outside the active
   workflow? Sibling workflows are listed explicitly. Global navigation,
   header/footer links, and unrelated modules are out of scope.

2. GROUNDING: Does each assertion have plausible support in the spec
   excerpt below? Paraphrase is fine; fabrication is not. Tests that verify
   conditions the spec never describes (e.g., specific error messages not
   mentioned, fields not listed, behavior not specified) should be flagged.

Be conservative. Only flag clear violations — false positives reduce the
final test count without improving quality.

Return strict JSON only, with one verdict per input test in the same order."""

    def _build_prompt(self, chunk: WorkflowChunk, tests: List[TestCase]) -> str:
        siblings = ", ".join(chunk.sibling_workflows) or "(none)"
        rules = "\n".join(f"  - {r}" for r in chunk.related_rules) or "  (none)"
        behaviors = "\n".join(f"  - {b}" for b in chunk.related_behaviors) or "  (none)"

        test_blocks = []
        for i, t in enumerate(tests):
            steps_str = "\n".join(f"      {n+1}. {s}" for n, s in enumerate(t.steps))
            test_blocks.append(
                f"  [{i}] title={t.title!r}\n"
                f"      type={t.test_type} priority={t.priority}\n"
                f"      preconditions={t.preconditions!r}\n"
                f"      steps:\n{steps_str}\n"
                f"      expected={t.expected_result!r}"
            )
        tests_block = "\n".join(test_blocks)

        return f"""Audit these test cases.

Module: {chunk.module_title}
Workflow under test: {chunk.workflow_name}
Workflow description: {chunk.workflow_description}
Sibling workflows in this module (out of scope for this audit): {siblings}

Available items: {", ".join(chunk.related_items) or "None"}

Business rules:
{rules}

Expected behaviors:
{behaviors}

Test cases to audit (indexed):
{tests_block}

Return JSON:
{{
  "verdicts": [
    {{
      "test_index": int,
      "verdict": "accept" | "revise" | "drop",
      "reason": "one short sentence",
      "redaction_hint": "what to fix on retry — REQUIRED for revise, OMIT for accept/drop"
    }},
    ...
  ]
}}

RULES:
- Emit exactly one verdict per test case, in input order.
- "accept" is the default. Only return "revise" or "drop" for clear problems.
- For "revise", redaction_hint MUST be specific (e.g., "Remove step 1 'Navigate to
  homepage' — not part of this workflow's scope.").
- For "drop", explain why in `reason` (e.g., "Tests global search, which is a
  sibling workflow.").
- Do NOT propose new tests. You are auditing what was given, not generating."""

    def run(self, chunk: WorkflowChunk, tests: List[TestCase]) -> List[TestCaseAuditVerdict]:
        import asyncio
        return asyncio.run(self.arun(chunk, tests))

    async def arun(
        self,
        chunk: WorkflowChunk,
        tests: List[TestCase],
    ) -> List[TestCaseAuditVerdict]:
        """Audit ``tests`` produced for ``chunk`` and return one verdict per test."""
        if not tests:
            return []

        prompt = self._build_prompt(chunk, tests)
        try:
            result = await self.acall_llm_json(prompt, max_tokens=4000)
        except Exception as err:
            print(f"    !! {self.name} | audit failed for '{chunk.workflow_name}': {err}")
            # On audit failure, default to accepting everything — better to ship
            # potentially noisy tests than lose them all.
            return [TestCaseAuditVerdict(test_index=i, verdict="accept") for i in range(len(tests))]

        return self._parse_verdicts(result, len(tests))

    @staticmethod
    def _parse_verdicts(result: dict, count: int) -> List[TestCaseAuditVerdict]:
        """Parse and bounds-check the LLM verdict list. Missing entries default to accept."""
        raw = result.get("verdicts") or []
        if not isinstance(raw, list):
            raw = []

        by_index: dict = {}
        for entry in raw:
            if not isinstance(entry, dict):
                continue
            try:
                idx = int(entry.get("test_index"))
            except (TypeError, ValueError):
                continue
            if not (0 <= idx < count):
                continue
            verdict = str(entry.get("verdict") or "").lower().strip()
            if verdict not in ("accept", "revise", "drop"):
                verdict = "accept"
            hint_raw = entry.get("redaction_hint")
            hint = str(hint_raw).strip() if hint_raw else None
            by_index[idx] = TestCaseAuditVerdict(
                test_index=idx,
                verdict=verdict,
                reason=str(entry.get("reason") or "").strip(),
                redaction_hint=hint,
            )

        return [
            by_index.get(i, TestCaseAuditVerdict(test_index=i, verdict="accept"))
            for i in range(count)
        ]
