from typing import List, Dict

from testwright.agents.base import BaseAgent
from testwright.models.schemas import TestCase, ModuleSummary


class VerificationFlagAgent(BaseAgent):
    """Agent responsible for flagging test cases that need post-verification"""

    @property
    def name(self) -> str:
        return "Verification Flag Agent"

    @property
    def system_prompt(self) -> str:
        return """You decide which positive tests modify persistent state and therefore need
post-verification (an independent observation that proves the change).

For each test, output:
- needs_post_verification: true if the test CREATES, UPDATES, DELETES,
  TRANSITIONS status, or CHANGES credentials on persistent data.
- modifies_state: short list of state names from the module summaries.
- modification_kind: "create" | "update" | "delete" | "status_transition"
                  | "credential_change" | "none"

needs_post_verification = false for: pure read/observe, navigation, search/filter,
login, logout, account registration, validation/edge cases, and password-reset
requests sent by email (the actual reset flow that changes the credential DOES need
verification — old credential fails, new one succeeds).

A success toast alone is NEVER proof. If a test only triggers a toast and does not
write data viewable elsewhere, still flag it (the gap will be tracked downstream)."""

    # ---- Heuristic pre-filter for read-only tests -------------------------
    # Steps/results containing ONLY these words are almost certainly read-only
    # and should never be flagged as state-changing.
    _READ_ONLY_STEP_INDICATORS = {
        "check", "verify", "observe", "confirm", "locate", "ensure",
        "view", "scroll", "look", "inspect", "see",
    }
    _READ_ONLY_RESULT_INDICATORS = {
        "displayed", "visible", "present", "shown", "appears",
        "is displayed", "is visible", "is present",
    }

    def _is_likely_read_only(self, tc: TestCase) -> bool:
        """Return True if every step is observational and the result is purely display.

        Examples that ARE read-only:
            Steps:    ["Check if the heading is visible", "Verify the table is displayed"]
            Expected: "Heading is displayed correctly"

        Examples that are NOT read-only:
            Steps:    ["Enter a valid name", "Click Save"]
            Expected: "Record is saved successfully"
        """
        # Check steps — every step must start with a read-only verb
        for step in tc.steps:
            first_word = step.strip().split()[0].lower().rstrip(".,:") if step.strip() else ""
            if first_word not in self._READ_ONLY_STEP_INDICATORS:
                return False

        # Check expected result — must contain a display-related phrase
        expected_lower = tc.expected_result.lower()
        if not any(ind in expected_lower for ind in self._READ_ONLY_RESULT_INDICATORS):
            return False

        return True

    def run(
        self,
        test_cases: List[TestCase],
        module_summaries: Dict[int, ModuleSummary]
    ) -> List[TestCase]:
        """Flag test cases that need post-verification"""

        # Only process positive test cases - negative and edge cases don't need verification
        positive_tests = [tc for tc in test_cases if tc.test_type == "positive"]
        other_tests = [tc for tc in test_cases if tc.test_type != "positive"]

        if not positive_tests:
            return test_cases

        # --- Pre-filter: skip obviously read-only tests before LLM call ------
        # This prevents the LLM from accidentally flagging "Verify X is displayed"
        # tests as state-changing, which was a source of false-positive flags.
        actionable_tests = []
        read_only_tests = []
        for tc in positive_tests:
            if self._is_likely_read_only(tc):
                tc.needs_post_verification = False
                tc.modifies_state = []
                tc.modification_kind = "none"
                read_only_tests.append(tc)
            else:
                actionable_tests.append(tc)

        if read_only_tests:
            print(f"  - Pre-filter skipped {len(read_only_tests)} read-only tests")

        if not actionable_tests:
            return positive_tests + other_tests

        # Build context about modules for the LLM
        modules_context = self._build_modules_context(module_summaries)

        # Build test cases for analysis (only actionable ones)
        tests_for_analysis = []
        for tc in actionable_tests:
            tests_for_analysis.append({
                "id": tc.id,
                "title": tc.title,
                "module": tc.module_title,
                "workflow": tc.workflow,
                "steps": tc.steps[:5],  # First 5 steps for context
                "expected_result": tc.expected_result
            })

        prompt = f"""Analyze these POSITIVE test cases and decide which ones need post-verification.

AVAILABLE MODULES AND THEIR CAPABILITIES:
{modules_context}

TEST CASES TO ANALYZE:
{self._format_tests(tests_for_analysis)}

For each test case, output:
1. needs_post_verification: true/false
2. modifies_state: list of state names (use names from the module summaries above)
3. modification_kind: one of "create" | "update" | "delete" | "status_transition"
                     | "credential_change" | "none"

Return JSON:
{{
    "flagged_tests": [
        {{
            "test_id": "ACTION-001",
            "needs_post_verification": true,
            "modifies_state": ["relevant_state_name"],
            "modification_kind": "create",
            "reason": "Brief explanation"
        }}
    ]
}}

RULES:
1. Flag any test that creates / updates / deletes / transitions status / changes a credential
   on persistent data — even if no module currently displays it (the gap is tracked downstream).
2. modification_kind="none" iff needs_post_verification=false.
3. Read-only / search / filter / navigation tests are never flagged.
4. Login, logout, and account registration are not flagged.
5. Password-reset REQUEST (email link) is not flagged; the actual password CHANGE is flagged
   with modification_kind="credential_change".
6. Include ALL test cases in the output.
7. Use state names that match those in the module summaries."""

        try:
            result = self.call_llm_json(prompt, max_tokens=16000)

            # Create lookup for flagged tests
            flags = {item["test_id"]: item for item in result.get("flagged_tests", [])}

            # Update test cases with flags (only actionable tests were sent to LLM)
            valid_kinds = {
                "create", "update", "delete", "status_transition",
                "credential_change", "none",
            }
            for tc in actionable_tests:
                if tc.id in flags:
                    flag_data = flags[tc.id]
                    tc.needs_post_verification = flag_data.get("needs_post_verification", False)
                    tc.modifies_state = flag_data.get("modifies_state", [])
                    kind = flag_data.get("modification_kind", "")
                    tc.modification_kind = kind if kind in valid_kinds else (
                        "none" if not tc.needs_post_verification else ""
                    )

            # Combine back: actionable (LLM-flagged) + read-only (pre-filtered) + other types
            return actionable_tests + read_only_tests + other_tests

        except Exception as e:
            print(f"Warning: Verification flagging failed: {e}")
            return test_cases

    def _build_modules_context(self, module_summaries: Dict[int, ModuleSummary]) -> str:
        """Build a context string describing all modules"""
        lines = []
        for summary in module_summaries.values():
            lines.append(f"- {summary.module_title}:")
            lines.append(f"    Summary: {summary.summary}")
            if summary.can_verify_states:
                lines.append(f"    Can verify: {', '.join(summary.can_verify_states)}")
            if summary.action_states:
                lines.append(f"    Modifies: {', '.join(summary.action_states)}")
        return "\n".join(lines)

    def _format_tests(self, tests: List[dict]) -> str:
        """Format tests for prompt"""
        lines = []
        for t in tests:
            lines.append(f"- {t['id']}: {t['title']}")
            lines.append(f"  Module: {t['module']}, Workflow: {t['workflow']}")
            lines.append(f"  Expected: {t['expected_result'][:100]}")
        return "\n".join(lines)
