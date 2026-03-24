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
        return """You are an expert QA engineer who understands when test results need external verification.

Your task is to analyze test cases and determine which ones need post-verification -
meaning the test's success should be verified by checking data in another part of the application.

NEEDS POST-VERIFICATION (needs_post_verification = true):
- Data creation: Verify new records appear in list/overview pages
- Data modification: Verify changes are reflected in display pages
- Data transfer/movement: Verify data moved from source to destination
- Submissions: Verify submission appears in history/status pages
- Any action that modifies persistent data viewable elsewhere

DOES NOT NEED POST-VERIFICATION (needs_post_verification = false):
- Login/Logout: Session state, no persistent data change
- Registration: Self-contained, success message is enough
- Read-only pages: Just displaying data, nothing to verify elsewhere
- Negative tests: Validation failures, no state change
- Edge case tests: Usually testing boundaries, not state changes
- Navigation: Just moving between pages
- Password reset requests: External verification (email), out of scope
- Search/Filter: Just filtering displayed data, no state change"""

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

        prompt = f"""Analyze these POSITIVE test cases and determine which ones need post-verification.

AVAILABLE MODULES AND THEIR CAPABILITIES:
{modules_context}

TEST CASES TO ANALYZE:
{self._format_tests(tests_for_analysis)}

For each test case, determine:
1. needs_post_verification: true/false
2. modifies_state: List of states this test modifies (use the state names from module summaries)

Return JSON:
{{
    "flagged_tests": [
        {{
            "test_id": "ACTION-001",
            "needs_post_verification": true,
            "modifies_state": ["relevant_state_name"],
            "reason": "This action modifies data which can be verified in another module"
        }},
        {{
            "test_id": "LOGIN-001",
            "needs_post_verification": false,
            "modifies_state": ["session_status"],
            "reason": "Login only affects session state, no persistent data to verify elsewhere"
        }}
    ]
}}

RULES:
1. Only flag tests that MODIFY data which can be VERIFIED in ANOTHER module
2. If a test modifies data but there's no way to verify it elsewhere, still flag it (we'll handle missing coverage later)
3. Read-only tests should NEVER be flagged
4. Login/logout/registration/password-reset should NOT be flagged
5. Include ALL test cases in the output
6. Use state names that match those defined in the module summaries"""

        try:
            result = self.call_llm_json(prompt, max_tokens=16000)

            # Create lookup for flagged tests
            flags = {item["test_id"]: item for item in result.get("flagged_tests", [])}

            # Update test cases with flags (only actionable tests were sent to LLM)
            for tc in actionable_tests:
                if tc.id in flags:
                    flag_data = flags[tc.id]
                    tc.needs_post_verification = flag_data.get("needs_post_verification", False)
                    tc.modifies_state = flag_data.get("modifies_state", [])

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
