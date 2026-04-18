from typing import List, Dict, Optional

from testwright.agents.base import BaseAgent
from testwright.models.schemas import (
    IdealVerification,
    ModuleSummary,
    ProjectContext,
    TestCase,
)


_VALID_STRATEGIES = {"after_only", "before_after", "cross_user"}
_VALID_TYPES = {
    "existence", "absence", "field_persistence", "status_transition",
    "cascading_update", "credential_change", "session_persistence", "financial_delta",
}


class IdealVerificationAgent(BaseAgent):
    """Agent responsible for generating ideal verification scenarios for flagged test cases"""

    @property
    def name(self) -> str:
        return "Ideal Verification Agent"

    @property
    def system_prompt(self) -> str:
        return """You design verification strategies for QA test cases.

For each test, generate 1-3 IDEAL verifications — independent observations that
would prove the test's state-changing action actually persisted (not just that a
success message appeared).

Every verification picks ONE execution_strategy and ONE verification_type from the
fixed taxonomies below. We later match these ideals to existing test cases."""

    def run(
        self,
        flagged_tests: List[TestCase],
        module_summaries: Dict[int, ModuleSummary],
        project_context: Optional[ProjectContext] = None,
    ) -> Dict[str, List[IdealVerification]]:
        """Generate ideal verifications for each flagged test case

        Returns:
            Dict mapping test_case_id to list of IdealVerification objects
        """

        # Only process tests that need verification
        tests_needing_verification = [tc for tc in flagged_tests if tc.needs_post_verification]

        if not tests_needing_verification:
            return {}

        # Build verification context from module summaries
        verification_context = self._build_verification_context(module_summaries)

        # Process in batches to avoid token limits
        all_verifications = {}
        batch_size = 10

        for i in range(0, len(tests_needing_verification), batch_size):
            batch = tests_needing_verification[i:i+batch_size]
            batch_verifications = self._generate_verifications_for_batch(
                batch, verification_context, project_context
            )
            all_verifications.update(batch_verifications)

        return all_verifications

    def _build_verification_context(self, module_summaries: Dict[int, ModuleSummary]) -> str:
        """Build context about what each module can verify (modules with
        verifiable states are highlighted with ✓)."""
        lines = ["ALL MODULES (\u2713 = can verify states):"]
        for summary in module_summaries.values():
            marker = "\u2713" if summary.can_verify_states else " "
            lines.append(f"- [{marker}] {summary.module_title} (module_id={summary.module_id}):")
            lines.append(f"    Summary: {summary.summary}")
            if summary.can_verify_states:
                lines.append(f"    Can verify: {', '.join(summary.can_verify_states)}")
            if summary.action_states:
                lines.append(f"    Modifies: {', '.join(summary.action_states)}")
        return "\n".join(lines)

    def _generate_verifications_for_batch(
        self,
        test_cases: List[TestCase],
        verification_context: str,
        project_context: Optional[ProjectContext] = None,
    ) -> Dict[str, List[IdealVerification]]:
        """Generate ideal verifications for a batch of test cases"""

        # Project context block (domain awareness)
        project_str = ""
        if project_context and (project_context.project_name or project_context.navigation_overview):
            project_str = (
                f"PROJECT: {project_context.project_name or 'Unknown'}\n"
                f"OVERVIEW: {project_context.navigation_overview or 'Not provided'}\n"
                "Use this context for vocabulary; the taxonomies below are domain-agnostic.\n\n"
            )

        # Format test cases for prompt
        tests_text = ""
        for tc in test_cases:
            kind = tc.modification_kind or "unknown"
            tests_text += (
                f"\nTest ID: {tc.id}\n"
                f"Title: {tc.title}\n"
                f"Module: {tc.module_title}\n"
                f"Workflow: {tc.workflow}\n"
                f"Modification kind: {kind}\n"
                f"Modifies state: {', '.join(tc.modifies_state) if tc.modifies_state else 'unknown'}\n"
                f"Steps: {'; '.join(tc.steps[:5])}\n"
                f"Expected: {tc.expected_result}\n"
                f"---\n"
            )

        prompt = f"""{project_str}Generate IDEAL verification scenarios for each test below.

{verification_context}

TEST CASES NEEDING VERIFICATION:
{tests_text}

Each verification MUST pick exactly one EXECUTION_STRATEGY and one VERIFICATION_TYPE.

EXECUTION_STRATEGY:
  after_only    — action CREATES new data; verify it exists.
  before_after  — action MODIFIES an existing value; record before, compare after.
                  You MUST fill before_action and after_action.
  cross_user    — action by user A must be observed by a different role/user B.
                  You MUST fill observer_role with the role that observes
                  (e.g. "checker", "teacher", "admin", "recipient").

VERIFICATION_TYPE:
  existence           — record appears in a listing/table with correct field values
  absence             — deleted or hidden record is provably gone from observer's view
  field_persistence   — updated value survives page refresh AND re-login
  status_transition   — status badge changed AND available action buttons changed
  cascading_update    — related data in another module reflects the change
  credential_change   — old credential fails, new credential succeeds
  session_persistence — change persists after logout / login
  financial_delta     — both sides of a transfer balance (source -, dest +)

EMISSION RULES:
- A success toast is NEVER proof. Do not emit "verify success message" verifications.
- A "create" usually needs existence + (if applicable) cascading_update on aggregates.
- A value transfer between two entities ALWAYS needs financial_delta on BOTH sides
  (one verification per side).
- A status_transition usually needs both the badge change AND the action-button
  change AND any audit/history entry the spec describes.
- A delete needs absence; if it cascades, also cascading_update on related modules.
- A credential_change needs credential_change verification (old fails, new succeeds)
  and session_persistence (the change survives logout/login).
- An action by one role visible to another role needs cross_user.
- Do NOT invent modules — only use modules from the context above.
- Use module names exactly as spelled in the context.
- Use state_to_verify names from the module summaries (or "" if none fits).

OUTPUT JSON SHAPE:
{{
    "test_verifications": [
        {{
            "test_id": "TEST-001",
            "ideal_verifications": [
                {{
                    "description": "Concrete observation to perform",
                    "target_module": "Module that displays this data",
                    "verification_action": "Specific action on that module",
                    "expected_change": "Exact expected outcome",
                    "state_to_verify": "state_name_from_module_summaries",
                    "verification_type": "existence",
                    "execution_strategy": "after_only",
                    "before_action": "",
                    "after_action": "",
                    "observer_role": "",
                    "session_note": ""
                }}
            ]
        }}
    ]
}}

If no verification is achievable for a test, return an empty ideal_verifications array
for that test_id. Include EVERY test_id in the output."""

        try:
            result = self.call_llm_json(prompt, max_tokens=16000)

            verifications = {}
            for item in result.get("test_verifications", []):
                test_id = item.get("test_id")
                if not test_id:
                    continue
                ideal_list = []
                for v in item.get("ideal_verifications", []):
                    strategy = v.get("execution_strategy", "after_only")
                    if strategy not in _VALID_STRATEGIES:
                        strategy = "after_only"

                    vtype = v.get("verification_type", "")
                    if vtype not in _VALID_TYPES:
                        vtype = ""

                    observer_role = v.get("observer_role", "")
                    requires_diff = (strategy == "cross_user") or bool(observer_role)
                    session_note = v.get("session_note", "") or (
                        f"Login as {observer_role}" if observer_role else ""
                    )

                    ideal_list.append(IdealVerification(
                        description=v.get("description", ""),
                        target_module=v.get("target_module", ""),
                        verification_action=v.get("verification_action", ""),
                        expected_change=v.get("expected_change", ""),
                        state_to_verify=v.get("state_to_verify", ""),
                        execution_strategy=strategy,
                        verification_type=vtype,
                        before_action=v.get("before_action", ""),
                        after_action=v.get("after_action", ""),
                        observer_role=observer_role,
                        requires_different_session=requires_diff,
                        session_note=session_note,
                    ))
                verifications[test_id] = ideal_list

            return verifications

        except Exception as e:
            print(f"Warning: Ideal verification generation failed: {e}")
            return {}
