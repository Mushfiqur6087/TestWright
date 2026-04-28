from typing import Dict, List

from autospectest.framework.agents.base import BaseAgent
from autospectest.framework.schemas.schemas import ParsedModule, ModuleSummary


class SummaryAgent(BaseAgent):
    """Agent responsible for generating concise module summaries."""

    @property
    def name(self) -> str:
        return "Summary Agent"

    @property
    def system_prompt(self) -> str:
        return """You are an expert at summarizing functional descriptions into concise, actionable summaries.

Your task is to create a 2-line summary of what each module/page does, focusing on:
1. What the page allows users to DO (actions)
2. What information the page SHOWS (data displayed)

These summaries are used as project context and metadata for generated output."""

    def run(self, modules: List[ParsedModule]) -> Dict[int, ModuleSummary]:
        """Generate summaries for all modules in a single LLM call for efficiency"""

        if not modules:
            return {}

        modules_text = ""
        for module in modules:
            modules_text += f"""
Module ID: {module.id}
Title: {module.title}
Description: {module.raw_description[:500]}
Items: {', '.join(module.mentioned_items[:10]) if module.mentioned_items else 'None'}
---
"""

        prompt = f"""Generate a concise 2-line summary for each module below.

For each module, provide a 2-line summary:
  Line 1 = what users can DO on this page (actions)
  Line 2 = what data is SHOWN/displayed on this page

{modules_text}

Return JSON:
{{
    "summaries": [
        {{
            "module_id": 1,
            "summary": "Line 1: Users can view their data and records.\\nLine 2: Displays relevant information and status."
        }},
        {{
            "module_id": 2,
            "summary": "Line 1: Users can submit or modify data.\\nLine 2: Shows confirmation after action completion."
        }}
    ]
}}

IMPORTANT:
- Keep the summary to exactly 2 lines.
- Focus on WHAT the page does, not HOW.
- Use the project's vocabulary; do not force banking or LMS idioms onto unrelated domains."""

        try:
            result = self.call_llm_json(prompt, max_tokens=8000)
            summaries: Dict[int, ModuleSummary] = {}

            for item in result.get("summaries", []):
                module_id = item.get("module_id")
                if module_id is not None:
                    summaries[module_id] = ModuleSummary(
                        module_id=module_id,
                        module_title=next((m.title for m in modules if m.id == module_id), "Unknown"),
                        summary=item.get("summary", ""),
                    )

            for module in modules:
                if module.id not in summaries:
                    summaries[module.id] = ModuleSummary(
                        module_id=module.id,
                        module_title=module.title,
                        summary=f"Module: {module.title}. {module.raw_description[:100]}",
                    )

            return summaries

        except Exception as e:
            print(f"Warning: Summary generation failed: {e}")
            return {
                module.id: ModuleSummary(
                    module_id=module.id,
                    module_title=module.title,
                    summary=f"Module: {module.title}. {module.raw_description[:100]}",
                )
                for module in modules
            }
