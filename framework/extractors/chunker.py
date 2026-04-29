from typing import List, Optional

from autospectest.framework.agents.base import BaseAgent
from autospectest.framework.schemas.schemas import ParsedModule, ProjectContext, WorkflowChunk


class ChunkerAgent(BaseAgent):
    """Agent responsible for splitting modules into workflow-based chunks"""

    @property
    def name(self) -> str:
        return "Chunker Agent"

    @property
    def system_prompt(self) -> str:
        return """You are an expert at analyzing functional descriptions and mapping elements to workflows.

Your task is to take a module with multiple workflows and intelligently determine which items,
business rules, and behaviors belong to each workflow.

CRITICAL RULES:
1. Map items/rules/behaviors ONLY to workflows where they are actually used
2. An item can belong to multiple workflows if it's shared
3. DO NOT invent new items or rules - only use what was extracted
4. Provide a clear description of what each workflow does
5. Most modules should have only 1-2 primary workflows - do not over-segment

WHAT IS A WORKFLOW:
A workflow is a top-level user action that (a) has its own distinct entry point —
a separate button, link, menu item, or page the user navigates to independently —
and (b) produces its own success or failure outcome. Examples across application types:
  • "Submit registration form", "Book a hotel room", "Approve a loan application"
  • "Execute a stock trade", "Enroll participants", "Create a journal entry"

WHAT IS NOT A WORKFLOW — fold these into their parent workflow instead:
  • Field-level validation or auto-formatting (phone masking, date parsing, ZIP)
  • Inline error display or success messages triggered by another action
  • Redirects that happen automatically after a workflow completes
  • Real-time UI updates (tab switching, dynamic price/count updates, expand/collapse)
  • Sub-steps within a single multi-step form (filling sections, confirming before submit)
  • Status-indicator or display-only behaviors (masked account numbers, color-coded badges)

TARGET: 1–3 workflows per module. When in doubt, consolidate into the closest workflow.

FIELD-LEVEL GRANULARITY:
1. Preserve individual field names exactly as provided (including "(required)" suffix)
2. Do NOT group fields together - keep them as separate items
3. Each field with validation rules should retain its associated rules
4. This granularity enables per-field test case generation for comprehensive coverage"""

    def run(
        self,
        module: ParsedModule,
        project_context: Optional[ProjectContext] = None,
        revision_hint: Optional[str] = None,
    ) -> List[WorkflowChunk]:
        """Split a module into workflow-based chunks.

        ``project_context`` is attached to every emitted chunk so that
        downstream agents (test generator, verifier) have awareness of the
        application domain without needing pipeline-wide wiring.

        ``revision_hint`` carries guidance from the workflow auditor on a
        retry — when set, the chunker always goes through the LLM mapping
        path so the hint can influence both workflow selection and item
        assignment, even when only 0 or 1 workflows were originally detected.
        """

        # On a hinted retry, force the LLM path so the hint can add or remove
        # workflows that the parser/short-circuits would otherwise miss.
        if revision_hint:
            return self._split_by_workflows(module, project_context, revision_hint=revision_hint)

        # If no workflows detected, create a single "full" chunk
        if not module.workflows:
            return [WorkflowChunk(
                chunk_id=f"{module.id}_full",
                module_id=module.id,
                module_title=module.title,
                workflow_name="Main workflow",
                workflow_description=module.raw_description[:200],
                related_items=module.mentioned_items,
                related_rules=module.business_rules,
                related_behaviors=module.expected_behaviors,
                project_context=project_context,
            )]

        # If only one workflow, no need to split
        if len(module.workflows) == 1:
            return [WorkflowChunk(
                chunk_id=f"{module.id}_workflow_0",
                module_id=module.id,
                module_title=module.title,
                workflow_name=module.workflows[0],
                workflow_description=f"Primary workflow for {module.title}",
                related_items=module.mentioned_items,
                related_rules=module.business_rules,
                related_behaviors=module.expected_behaviors,
                project_context=project_context,
            )]

        # Multiple workflows - use LLM to map items to workflows
        return self._split_by_workflows(module, project_context)

    async def arun(
        self,
        module: ParsedModule,
        project_context: Optional[ProjectContext] = None,
        revision_hint: Optional[str] = None,
    ) -> List[WorkflowChunk]:
        """Async version of run() — uses acall_llm_json for parallel module processing."""
        if revision_hint:
            return await self._asplit_by_workflows(module, project_context, revision_hint=revision_hint)
        if not module.workflows:
            return [WorkflowChunk(
                chunk_id=f"{module.id}_full",
                module_id=module.id,
                module_title=module.title,
                workflow_name="Main workflow",
                workflow_description=module.raw_description[:200],
                related_items=module.mentioned_items,
                related_rules=module.business_rules,
                related_behaviors=module.expected_behaviors,
                project_context=project_context,
            )]
        if len(module.workflows) == 1:
            return [WorkflowChunk(
                chunk_id=f"{module.id}_workflow_0",
                module_id=module.id,
                module_title=module.title,
                workflow_name=module.workflows[0],
                workflow_description=f"Primary workflow for {module.title}",
                related_items=module.mentioned_items,
                related_rules=module.business_rules,
                related_behaviors=module.expected_behaviors,
                project_context=project_context,
            )]
        return await self._asplit_by_workflows(module, project_context)

    async def _asplit_by_workflows(
        self,
        module: ParsedModule,
        project_context: Optional[ProjectContext] = None,
        revision_hint: Optional[str] = None,
    ) -> List[WorkflowChunk]:
        """Async version of _split_by_workflows — same logic, uses acall_llm_json."""
        workflows_list = "\n".join([f"  {i+1}. {w}" for i, w in enumerate(module.workflows)]) or "  (none detected — infer the primary workflow from the description)"
        items_list = ", ".join(module.mentioned_items) if module.mentioned_items else "None"
        rules_list = "\n".join([f"  - {r}" for r in module.business_rules]) if module.business_rules else "None"
        behaviors_list = "\n".join([f"  - {b}" for b in module.expected_behaviors]) if module.expected_behaviors else "None"

        hint_block = ""
        if revision_hint:
            hint_block = (
                "\n\nAUDITOR REVISION HINT (from a prior pass) — apply faithfully:\n"
                f"  {revision_hint}\n"
                "Use this to add missing workflows, drop out-of-scope ones, "
                "or correct ungrounded names.\n"
            )

        prompt = f"""Analyze this module and map its elements to the appropriate workflows.{hint_block}

Module: {module.title}
Description: {module.raw_description}

Workflows detected:
{workflows_list}

Mentioned Items: {items_list}

Business Rules:
{rules_list}

Expected Behaviors:
{behaviors_list}

For EACH workflow, determine:
1. Which items are used in that workflow
2. Which business rules apply to that workflow
3. Which expected behaviors are relevant to that workflow
4. A brief description of what the workflow does

Return a JSON object:
{{
    "workflow_chunks": [
        {{
            "workflow_name": "exact workflow name from list above",
            "workflow_description": "brief description of what this workflow does",
            "related_items": ["item1", "item2"],
            "related_rules": ["rule1", "rule2"],
            "related_behaviors": ["behavior1", "behavior2"]
        }}
    ]
}}

IMPORTANT:
- Include ALL workflows from the list above
- Only use items/rules/behaviors that were provided - do not invent new ones
- An item/rule/behavior can appear in multiple workflows if relevant
- Use EXACT text from the provided lists
- Focus on the primary testable workflows - navigation links don't need separate chunks

FIELD-LEVEL GRANULARITY:
- Preserve individual field names (do not group them)
- Include the "(required)" suffix on field names if present
- Each required field should be listed separately to enable per-field test generation
- Include all validation rules related to individual fields
"""

        try:
            result = await self.acall_llm_json(prompt, max_tokens=16000)
            chunks = []

            for i, chunk_data in enumerate(result.get("workflow_chunks", [])):
                chunks.append(WorkflowChunk(
                    chunk_id=f"{module.id}_workflow_{i}",
                    module_id=module.id,
                    module_title=module.title,
                    workflow_name=chunk_data.get("workflow_name", f"Workflow {i+1}"),
                    workflow_description=chunk_data.get("workflow_description", ""),
                    related_items=chunk_data.get("related_items", []),
                    related_rules=chunk_data.get("related_rules", []),
                    related_behaviors=chunk_data.get("related_behaviors", []),
                    project_context=project_context,
                ))

            returned_workflows = {c.workflow_name.lower() for c in chunks}
            for i, workflow in enumerate(module.workflows):
                if workflow.lower() not in returned_workflows:
                    chunks.append(WorkflowChunk(
                        chunk_id=f"{module.id}_workflow_{len(chunks)}",
                        module_id=module.id,
                        module_title=module.title,
                        workflow_name=workflow,
                        workflow_description=f"Workflow: {workflow}",
                        related_items=[],
                        related_rules=[],
                        related_behaviors=[],
                        project_context=project_context,
                    ))

            chunks = self._consolidate_chunks(chunks, module.title)

            if len(chunks) > 1:
                all_names = [c.workflow_name for c in chunks]
                for chunk in chunks:
                    chunk.sibling_workflows = [w for w in all_names if w != chunk.workflow_name]

            return chunks if chunks else self._fallback_chunks(module, project_context)

        except Exception as e:
            print(f"Warning: Async workflow splitting failed for module {module.title}: {e}")
            return self._fallback_chunks(module, project_context)

    def _split_by_workflows(
        self,
        module: ParsedModule,
        project_context: Optional[ProjectContext] = None,
        revision_hint: Optional[str] = None,
    ) -> List[WorkflowChunk]:
        """Use LLM to intelligently map items/rules/behaviors to workflows"""

        workflows_list = "\n".join([f"  {i+1}. {w}" for i, w in enumerate(module.workflows)]) or "  (none detected — infer the primary workflow from the description)"
        items_list = ", ".join(module.mentioned_items) if module.mentioned_items else "None"
        rules_list = "\n".join([f"  - {r}" for r in module.business_rules]) if module.business_rules else "None"
        behaviors_list = "\n".join([f"  - {b}" for b in module.expected_behaviors]) if module.expected_behaviors else "None"

        hint_block = ""
        if revision_hint:
            hint_block = (
                "\n\nAUDITOR REVISION HINT (from a prior pass) — apply faithfully:\n"
                f"  {revision_hint}\n"
                "Use this to add missing workflows, drop out-of-scope ones, "
                "or correct ungrounded names.\n"
            )

        prompt = f"""Analyze this module and map its elements to the appropriate workflows.{hint_block}

Module: {module.title}
Description: {module.raw_description}

Workflows detected:
{workflows_list}

Mentioned Items: {items_list}

Business Rules:
{rules_list}

Expected Behaviors:
{behaviors_list}

For EACH workflow, determine:
1. Which items are used in that workflow
2. Which business rules apply to that workflow
3. Which expected behaviors are relevant to that workflow
4. A brief description of what the workflow does

Return a JSON object:
{{
    "workflow_chunks": [
        {{
            "workflow_name": "exact workflow name from list above",
            "workflow_description": "brief description of what this workflow does",
            "related_items": ["item1", "item2"],
            "related_rules": ["rule1", "rule2"],
            "related_behaviors": ["behavior1", "behavior2"]
        }}
    ]
}}

IMPORTANT:
- Include ALL workflows from the list above
- Only use items/rules/behaviors that were provided - do not invent new ones
- An item/rule/behavior can appear in multiple workflows if relevant
- Use EXACT text from the provided lists
- Focus on the primary testable workflows - navigation links don't need separate chunks

FIELD-LEVEL GRANULARITY:
- Preserve individual field names (do not group them)
- Include the "(required)" suffix on field names if present
- Each required field should be listed separately to enable per-field test generation
- Include all validation rules related to individual fields
"""

        try:
            result = self.call_llm_json(prompt, max_tokens=16000)
            chunks = []

            for i, chunk_data in enumerate(result.get("workflow_chunks", [])):
                chunks.append(WorkflowChunk(
                    chunk_id=f"{module.id}_workflow_{i}",
                    module_id=module.id,
                    module_title=module.title,
                    workflow_name=chunk_data.get("workflow_name", f"Workflow {i+1}"),
                    workflow_description=chunk_data.get("workflow_description", ""),
                    related_items=chunk_data.get("related_items", []),
                    related_rules=chunk_data.get("related_rules", []),
                    related_behaviors=chunk_data.get("related_behaviors", []),
                    project_context=project_context,
                ))

            # If LLM didn't return all workflows, add missing ones
            returned_workflows = {c.workflow_name.lower() for c in chunks}
            for i, workflow in enumerate(module.workflows):
                if workflow.lower() not in returned_workflows:
                    chunks.append(WorkflowChunk(
                        chunk_id=f"{module.id}_workflow_{len(chunks)}",
                        module_id=module.id,
                        module_title=module.title,
                        workflow_name=workflow,
                        workflow_description=f"Workflow: {workflow}",
                        related_items=[],
                        related_rules=[],
                        related_behaviors=[],
                        project_context=project_context,
                    ))

            chunks = self._consolidate_chunks(chunks, module.title)

            # Annotate each chunk with sibling workflow names for cross-chunk dedup
            if len(chunks) > 1:
                all_names = [c.workflow_name for c in chunks]
                for chunk in chunks:
                    chunk.sibling_workflows = [w for w in all_names if w != chunk.workflow_name]

            return chunks if chunks else self._fallback_chunks(module, project_context)

        except Exception as e:
            print(f"Warning: Workflow splitting failed for module {module.title}: {e}")
            return self._fallback_chunks(module, project_context)

    def _fallback_chunks(
        self,
        module: ParsedModule,
        project_context: Optional[ProjectContext] = None,
    ) -> List[WorkflowChunk]:
        """Fallback: create one chunk per workflow with all items"""
        chunks = []

        for i, workflow in enumerate(module.workflows):
            chunks.append(WorkflowChunk(
                chunk_id=f"{module.id}_workflow_{i}",
                module_id=module.id,
                module_title=module.title,
                workflow_name=workflow,
                workflow_description=f"Workflow: {workflow}",
                related_items=module.mentioned_items,  # Give all items to each workflow
                related_rules=module.business_rules,
                related_behaviors=module.expected_behaviors,
                project_context=project_context,
            ))

        chunks = self._consolidate_chunks(chunks, module.title)

        # Annotate each chunk with sibling workflow names for cross-chunk dedup
        if len(chunks) > 1:
            all_names = [c.workflow_name for c in chunks]
            for chunk in chunks:
                chunk.sibling_workflows = [w for w in all_names if w != chunk.workflow_name]

        return chunks

    # ------------------------------------------------------------------
    # Deterministic consolidation safety net
    # ------------------------------------------------------------------

    _MAX_CHUNKS_PER_MODULE = 4

    def _consolidate_chunks(
        self,
        chunks: List[WorkflowChunk],
        module_title: str,
    ) -> List[WorkflowChunk]:
        """Merge chunks by shared colon-delimited prefix, then cap at 6.

        Fires after LLM/workflow splitting so parser drift can't fan out
        20 chunks for a single menu-heavy module. Pure Python — no LLM call.
        """
        if len(chunks) <= 1:
            return chunks

        merged = self._merge_by_shared_prefix(chunks, module_title)
        capped = self._cap_chunk_count(merged, module_title)
        return capped

    def _merge_by_shared_prefix(
        self,
        chunks: List[WorkflowChunk],
        module_title: str,
    ) -> List[WorkflowChunk]:
        """Group chunks whose workflow_name shares a common prefix up to the
        first colon, then merge each group into a single chunk."""
        groups: Dict[str, List[WorkflowChunk]] = {}
        order: List[str] = []
        for c in chunks:
            name = c.workflow_name or ""
            if ":" in name:
                key = name.split(":", 1)[0].strip().lower()
            else:
                key = name.strip().lower()
            if key not in groups:
                groups[key] = []
                order.append(key)
            groups[key].append(c)

        out: List[WorkflowChunk] = []
        for key in order:
            bucket = groups[key]
            if len(bucket) == 1:
                out.append(bucket[0])
                continue

            prefix = bucket[0].workflow_name.split(":", 1)[0].strip() if ":" in bucket[0].workflow_name else bucket[0].workflow_name.strip()
            merged_name = f"{prefix} actions"
            merged_chunk = self._merge_chunks(bucket, merged_name)
            action_titles = [c.workflow_name for c in bucket]
            print(
                f"    [consolidate] {module_title}: merged {len(bucket)} chunks "
                f"with prefix '{prefix}' -> '{merged_name}' "
                f"(was: {', '.join(action_titles)})"
            )
            out.append(merged_chunk)

        return out

    def _cap_chunk_count(
        self,
        chunks: List[WorkflowChunk],
        module_title: str,
    ) -> List[WorkflowChunk]:
        """If still > _MAX_CHUNKS_PER_MODULE, repeatedly merge the smallest
        chunk into its nearest neighbor (by original order)."""
        if len(chunks) <= self._MAX_CHUNKS_PER_MODULE:
            return chunks

        working = list(chunks)
        while len(working) > self._MAX_CHUNKS_PER_MODULE:
            sizes = [
                len(c.related_items) + len(c.related_rules) + len(c.related_behaviors)
                for c in working
            ]
            smallest_idx = min(range(len(working)), key=lambda i: sizes[i])

            # Pick neighbor: prefer right neighbor, fall back to left.
            if smallest_idx + 1 < len(working):
                neighbor_idx = smallest_idx + 1
            else:
                neighbor_idx = smallest_idx - 1

            left, right = sorted([smallest_idx, neighbor_idx])
            a, b = working[left], working[right]
            merged_name = f"{a.workflow_name} + {b.workflow_name}"
            merged_chunk = self._merge_chunks([a, b], merged_name)
            print(
                f"    [consolidate] {module_title}: hit cap {self._MAX_CHUNKS_PER_MODULE}, "
                f"merged '{a.workflow_name}' + '{b.workflow_name}'"
            )
            working = working[:left] + [merged_chunk] + working[right + 1:]

        return working

    def _merge_chunks(
        self,
        bucket: List[WorkflowChunk],
        merged_name: str,
    ) -> WorkflowChunk:
        """Concatenate related_items/rules/behaviors, dedup by string equality,
        preserving first-seen order."""
        first = bucket[0]
        items = self._dedup_preserve_order(
            [x for c in bucket for x in c.related_items]
        )
        rules = self._dedup_preserve_order(
            [x for c in bucket for x in c.related_rules]
        )
        behaviors = self._dedup_preserve_order(
            [x for c in bucket for x in c.related_behaviors]
        )
        descriptions = [c.workflow_description for c in bucket if c.workflow_description]
        description = " | ".join(self._dedup_preserve_order(descriptions))

        return WorkflowChunk(
            chunk_id=first.chunk_id,
            module_id=first.module_id,
            module_title=first.module_title,
            workflow_name=merged_name,
            workflow_description=description or first.workflow_description,
            related_items=items,
            related_rules=rules,
            related_behaviors=behaviors,
            project_context=first.project_context,
        )

    @staticmethod
    def _dedup_preserve_order(seq: List[str]) -> List[str]:
        seen = set()
        out = []
        for x in seq:
            key = x.strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            out.append(x)
        return out
