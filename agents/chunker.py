from typing import List

from testwright.agents.base import BaseAgent
from testwright.models.schemas import ParsedModule, WorkflowChunk


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

FIELD-LEVEL GRANULARITY:
1. Preserve individual field names exactly as provided (including "(required)" suffix)
2. Do NOT group fields together - keep them as separate items
3. Each field with validation rules should retain its associated rules
4. This granularity enables per-field test case generation for comprehensive coverage"""

    def run(self, module: ParsedModule) -> List[WorkflowChunk]:
        """Split a module into workflow-based chunks"""

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
                related_behaviors=module.expected_behaviors
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
                related_behaviors=module.expected_behaviors
            )]

        # Multiple workflows - use LLM to map items to workflows
        return self._split_by_workflows(module)

    def _split_by_workflows(self, module: ParsedModule) -> List[WorkflowChunk]:
        """Use LLM to intelligently map items/rules/behaviors to workflows"""

        workflows_list = "\n".join([f"  {i+1}. {w}" for i, w in enumerate(module.workflows)])
        items_list = ", ".join(module.mentioned_items) if module.mentioned_items else "None"
        rules_list = "\n".join([f"  - {r}" for r in module.business_rules]) if module.business_rules else "None"
        behaviors_list = "\n".join([f"  - {b}" for b in module.expected_behaviors]) if module.expected_behaviors else "None"

        prompt = f"""Analyze this module and map its elements to the appropriate workflows.

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
            result = self.call_llm_json(prompt, max_tokens=4000)
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
                    related_behaviors=chunk_data.get("related_behaviors", [])
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
                        related_behaviors=[]
                    ))

            return chunks if chunks else self._fallback_chunks(module)

        except Exception as e:
            print(f"Warning: Workflow splitting failed for module {module.title}: {e}")
            return self._fallback_chunks(module)

    def _fallback_chunks(self, module: ParsedModule) -> List[WorkflowChunk]:
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
                related_behaviors=module.expected_behaviors
            ))

        return chunks
