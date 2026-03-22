from typing import Dict, List

from testwright.agents.base import BaseAgent
from testwright.models.schemas import ParsedModule, ModuleSummary


class SummaryAgent(BaseAgent):
    """Agent responsible for generating concise module summaries for post-verification matching"""

    @property
    def name(self) -> str:
        return "Summary Agent"

    @property
    def system_prompt(self) -> str:
        return """You are an expert at summarizing functional descriptions into concise, actionable summaries.

Your task is to create a 2-line summary of what each module/page does, focusing on:
1. What the page allows users to DO (actions)
2. What information the page SHOWS (data displayed)

These summaries will be used to match test cases that need post-verification with pages that can verify the results."""

    def run(self, modules: List[ParsedModule]) -> Dict[int, ModuleSummary]:
        """Generate summaries for all modules in a single LLM call for efficiency"""

        if not modules:
            return {}

        # Build module descriptions for prompt
        modules_text = ""
        for module in modules:
            modules_text += f"""
Module ID: {module.id}
Title: {module.title}
Description: {module.raw_description[:500]}
Items: {', '.join(module.mentioned_items[:10]) if module.mentioned_items else 'None'}
---
"""

        prompt = f"""Generate concise 2-line summaries for each module below.

For each module, provide:
1. A 2-line summary: Line 1 = what users can DO, Line 2 = what data is SHOWN/displayed
2. Verification keywords: words that indicate this module can verify something (e.g., data display words)
3. Can verify states: what kinds of application states this module can VERIFY/DISPLAY (for read-only or display modules)
4. Action states: what kinds of application states this module MODIFIES (for action modules)

{modules_text}

Return JSON:
{{
    "summaries": [
        {{
            "module_id": 1,
            "summary": "Line 1: Users can view their data and records.\\nLine 2: Displays relevant information and status.",
            "verification_keywords": ["view", "display", "list", "status"],
            "can_verify_states": ["data_display", "record_list"],
            "action_states": []
        }},
        {{
            "module_id": 2,
            "summary": "Line 1: Users can submit or modify data.\\nLine 2: Shows confirmation after action completion.",
            "verification_keywords": [],
            "can_verify_states": [],
            "action_states": ["data_modified", "record_created"]
        }}
    ]
}}

IMPORTANT:
- Keep summaries to exactly 2 lines
- Focus on WHAT the page does, not HOW
- verification_keywords should be single words that appear when this module displays verifiable data
- can_verify_states: States this module can READ/DISPLAY (use descriptive snake_case names based on actual functionality)
- action_states: States this module MODIFIES (use descriptive snake_case names based on actual functionality)
- A module can have both (e.g., a profile page both modifies AND displays profile data)

NAMING CONVENTION FOR STATES:
- Use snake_case descriptive names based on what the module actually does
- Examples: user_profile, item_list, order_history, submission_status, record_data, settings_config
- Be specific to the application domain from the functional description
- Do NOT use generic placeholder names - derive them from the actual module functionality

UI STATE CHANGES — COVER THESE TOO:
Many modules allow users to change the UI layout or preferences. These ARE modifiable
states and must be listed in action_states. Examples:
  - Reordering items (e.g., moving a block, re-arranging sections) → action_state: "layout_order"
  - Starring/favoriting (e.g., marking a course as favourite) → action_state: "favorite_status"
  - Hiding/removing from view (e.g., "Remove from view" option) → action_state: "visibility_status"
  - Toggling modes (e.g., Edit mode on/off) → action_state: "edit_mode_status"
  - Collapsing/expanding sections → usually transient, skip unless persisted

If the same module DISPLAYS the result of these actions (e.g., the Dashboard shows
blocks in their current positions), also add the state to can_verify_states.

CROSS-MODULE VERIFICATION — BE THOROUGH:
A module may be able to verify states that are MODIFIED by a different module. Think
about every piece of data this module displays and where that data could come from.

Examples:
  - A "Grades / User Report" module displays grades → can_verify: "grade_display"
    even though grades are entered in "Assignment Submissions".
  - A "Course Page" displays activities → can_verify: "course_content_display"
    even though activities are added in "Adding Activities".
  - A "Participants" list displays enrolled users → can_verify: "enrollment_list"
    even though enrollment happens in an enrolment dialog."""

        try:
            result = self.call_llm_json(prompt, max_tokens=4000)
            summaries = {}

            for item in result.get("summaries", []):
                module_id = item.get("module_id")
                if module_id is not None:
                    summaries[module_id] = ModuleSummary(
                        module_id=module_id,
                        module_title=next((m.title for m in modules if m.id == module_id), "Unknown"),
                        summary=item.get("summary", ""),
                        verification_keywords=item.get("verification_keywords", []),
                        can_verify_states=item.get("can_verify_states", []),
                        action_states=item.get("action_states", [])
                    )

            # Ensure all modules have summaries (fallback for any missing)
            for module in modules:
                if module.id not in summaries:
                    summaries[module.id] = ModuleSummary(
                        module_id=module.id,
                        module_title=module.title,
                        summary=f"Module: {module.title}. {module.raw_description[:100]}",
                        verification_keywords=[],
                        can_verify_states=[],
                        action_states=[]
                    )

            return summaries

        except Exception as e:
            print(f"Warning: Summary generation failed: {e}")
            # Fallback: create basic summaries
            return {
                module.id: ModuleSummary(
                    module_id=module.id,
                    module_title=module.title,
                    summary=f"Module: {module.title}. {module.raw_description[:100]}",
                    verification_keywords=[],
                    can_verify_states=[],
                    action_states=[]
                )
                for module in modules
            }
