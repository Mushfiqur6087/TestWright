"""Workflow Auditor — actor-critic over chunker output.

Audits the workflow chunks produced for a single module against the module's
raw spec text. Returns a structured report listing coverage gaps, ungrounded
chunks, and scope leaks, plus a free-text revision hint the chunker can
consume on a single retry.
"""

from dataclasses import dataclass, field
from typing import List

from autospectest.framework.agents.base import BaseAgent
from autospectest.framework.schemas.schemas import ParsedModule, WorkflowChunk


@dataclass
class WorkflowAuditReport:
    """Result of one audit pass over a module's chunk set.

    All index lists refer to positions in the chunks list passed into ``run``.
    """

    module_id: int
    missing_workflows: List[str] = field(default_factory=list)
    ungrounded_chunk_indices: List[int] = field(default_factory=list)
    scope_violations: List[int] = field(default_factory=list)
    revision_hint: str = ""

    def is_clean(self) -> bool:
        return not (
            self.missing_workflows
            or self.ungrounded_chunk_indices
            or self.scope_violations
        )


class WorkflowAuditorAgent(BaseAgent):
    """Audit one module's chunk set for coverage, grounding, and scope leaks."""

    @property
    def name(self) -> str:
        return "Workflow Auditor Agent"

    @property
    def system_prompt(self) -> str:
        return """You are a meticulous reviewer of workflow extraction output.

You are given:
1. A module's raw functional-spec text.
2. A list of workflow chunks that another agent extracted from that text.

Your job is to flag exactly three classes of problems and nothing else:

A. COVERAGE GAPS — flag a workflow as "missing" ONLY when ALL of these hold:
   1. The spec describes an action a user can CHOOSE to initiate on its own, via a
      distinct entry point (a separate button, link, menu item, or dedicated form/page).
   2. That action has its own success or failure outcome not already covered by any
      existing chunk, even partially.
   3. It represents a meaningful user journey, not a side-effect or sub-step of one.

   Never flag as "missing":
   - Field-level validation or auto-formatting behaviors (phone masking, date parsing,
     SSN/ZIP formatting, real-time input feedback)
   - Display behaviors fired automatically by another action (inline error popups,
     success banners, redirects on completion, status badge changes, price updates)
   - UI convenience features (drag-and-drop reordering, inline rename, expand/collapse)
   - Steps inside a multi-step form that the spec describes as part of one flow
   - Behaviors mentioned as consequences of an action, not as user-initiated actions

   If the existing chunks already cover the module's primary user journeys, return
   missing_workflows = []. Err strongly on the side of NOT flagging — a false
   positive forces an expensive retry and introduces unnecessary chunks downstream.

B. UNGROUNDED CHUNKS — chunks whose workflow_name or workflow_description has no
   plausible support in the spec text. Paraphrasing is fine; fabrication is not.
   If the chunk describes something that the spec does NOT mention at all, flag it.

C. SCOPE VIOLATIONS — chunks that describe functionality belonging to a different
   module (sibling navigation, global search bar, footer links, etc.). The chunker
   sometimes pulls in cross-module concerns; flag those.

Be conservative. Only flag clear violations. When in doubt, do NOT flag — false
positives waste a retry and may degrade output. If everything looks correct,
return empty arrays.

Return strict JSON only."""

    def run(
        self,
        module: ParsedModule,
        chunks: List[WorkflowChunk],
    ) -> WorkflowAuditReport:
        """Audit ``chunks`` against ``module`` and return the structured report."""

        if not chunks:
            return WorkflowAuditReport(module_id=module.id)

        chunk_lines = []
        for i, c in enumerate(chunks):
            chunk_lines.append(
                f"  [{i}] workflow_name={c.workflow_name!r} | description={c.workflow_description!r}"
            )
        chunks_block = "\n".join(chunk_lines)

        prompt = f"""Audit this module's extracted workflow chunks.

Module: {module.title}
Module ID: {module.id}

Module spec text:
\"\"\"
{module.raw_description}
\"\"\"

Mentioned items: {", ".join(module.mentioned_items) or "None"}
Business rules: {"; ".join(module.business_rules) or "None"}
Expected behaviors: {"; ".join(module.expected_behaviors) or "None"}

Extracted workflow chunks (indexed):
{chunks_block}

Return JSON:
{{
  "missing_workflows": ["short workflow name", ...],
  "ungrounded_chunk_indices": [int, ...],
  "scope_violations": [int, ...],
  "revision_hint": "Free-text instruction the chunker should follow on retry. If everything is fine, leave as empty string."
}}

GUIDELINES:
- "missing_workflows" entries must be short workflow names (3-6 words) that the
  spec describes but no chunk represents. If the chunker covered everything, leave empty.
- "ungrounded_chunk_indices" lists indices of chunks whose names/descriptions
  cannot be plausibly derived from the spec text above. Paraphrase is fine.
- "scope_violations" lists indices of chunks that belong to a DIFFERENT module
  (navigation, global features, sibling-module functionality).
- "revision_hint" should be a single sentence the chunker can use to fix the
  extraction. Empty string when nothing is wrong.
- Be conservative — only flag clear problems."""

        try:
            result = self.call_llm_json(prompt, max_tokens=2000)
        except Exception as err:
            print(f"    !! {self.name} | audit failed for '{module.title}': {err}")
            return WorkflowAuditReport(module_id=module.id)

        return self._parse_report(result, module.id, len(chunks))

    async def arun(
        self,
        module: ParsedModule,
        chunks: List[WorkflowChunk],
    ) -> WorkflowAuditReport:
        """Async version of run() — uses acall_llm_json for parallel module processing."""
        if not chunks:
            return WorkflowAuditReport(module_id=module.id)

        chunk_lines = []
        for i, c in enumerate(chunks):
            chunk_lines.append(
                f"  [{i}] workflow_name={c.workflow_name!r} | description={c.workflow_description!r}"
            )
        chunks_block = "\n".join(chunk_lines)

        prompt = f"""Audit this module's extracted workflow chunks.

Module: {module.title}
Module ID: {module.id}

Module spec text:
\"\"\"
{module.raw_description}
\"\"\"

Mentioned items: {", ".join(module.mentioned_items) or "None"}
Business rules: {"; ".join(module.business_rules) or "None"}
Expected behaviors: {"; ".join(module.expected_behaviors) or "None"}

Extracted workflow chunks (indexed):
{chunks_block}

Return JSON:
{{
  "missing_workflows": ["short workflow name", ...],
  "ungrounded_chunk_indices": [int, ...],
  "scope_violations": [int, ...],
  "revision_hint": "Free-text instruction the chunker should follow on retry. If everything is fine, leave as empty string."
}}

GUIDELINES:
- "missing_workflows" entries must be short workflow names (3-6 words) that the
  spec describes but no chunk represents. If the chunker covered everything, leave empty.
- "ungrounded_chunk_indices" lists indices of chunks whose names/descriptions
  cannot be plausibly derived from the spec text above. Paraphrase is fine.
- "scope_violations" lists indices of chunks that belong to a DIFFERENT module
  (navigation, global features, sibling-module functionality).
- "revision_hint" should be a single sentence the chunker can use to fix the
  extraction. Empty string when nothing is wrong.
- Be conservative — only flag clear problems."""

        try:
            result = await self.acall_llm_json(prompt, max_tokens=2000)
        except Exception as err:
            print(f"    !! {self.name} | audit failed for '{module.title}': {err}")
            return WorkflowAuditReport(module_id=module.id)

        return self._parse_report(result, module.id, len(chunks))

    @staticmethod
    def _parse_report(
        result: dict,
        module_id: int,
        chunk_count: int,
    ) -> WorkflowAuditReport:
        """Parse and bounds-check the LLM verdict."""
        missing = result.get("missing_workflows") or []
        if not isinstance(missing, list):
            missing = []
        missing = [str(x).strip() for x in missing if str(x).strip()]

        def _clamp_indices(raw) -> List[int]:
            if not isinstance(raw, list):
                return []
            out: List[int] = []
            for v in raw:
                try:
                    idx = int(v)
                except (TypeError, ValueError):
                    continue
                if 0 <= idx < chunk_count and idx not in out:
                    out.append(idx)
            return out

        ungrounded = _clamp_indices(result.get("ungrounded_chunk_indices"))
        scope = _clamp_indices(result.get("scope_violations"))
        hint = str(result.get("revision_hint") or "").strip()

        return WorkflowAuditReport(
            module_id=module_id,
            missing_workflows=missing,
            ungrounded_chunk_indices=ungrounded,
            scope_violations=scope,
            revision_hint=hint,
        )
