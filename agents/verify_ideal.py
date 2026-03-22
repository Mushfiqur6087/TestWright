from typing import List, Dict

from testwright.agents.base import BaseAgent
from testwright.models.schemas import TestCase, ModuleSummary, IdealVerification


class IdealVerificationAgent(BaseAgent):
    """Agent responsible for generating ideal verification scenarios for flagged test cases"""

    @property
    def name(self) -> str:
        return "Ideal Verification Agent"

    @property
    def system_prompt(self) -> str:
        return """You are an expert QA engineer who designs verification strategies for test cases.

Your task is to generate IDEAL verification scenarios — what SHOULD be checked to confirm
a test actually succeeded. You must choose the right EXECUTION STRATEGY for each verification:

EXECUTION STRATEGIES:
1. "before_after" — The verification test must run TWICE: once BEFORE the action (to record
   a baseline value) and once AFTER (to compare and confirm the change). Use this when the
   action MODIFIES existing data and the only way to prove the change is by comparing
   before vs after values.
   Examples: checking that a numeric value changed, verifying a counter updated,
   confirming data was modified in-place.

2. "after_only" — The verification test runs only AFTER the action. Use this when the action
   CREATES new data or produces a result that didn't exist before — you just need to check
   it appeared.
   Examples: a new record appears in a list, a confirmation message is shown,
   a new entry in history/log.

SESSION AWARENESS:
If the verification requires viewing data from a DIFFERENT user's perspective (e.g., the
action was performed by user A but the result should be visible to user B), set
requires_different_session=true and explain who needs to be logged in.

These are IDEAL verifications — we'll later match them to actual test cases that exist."""

    def run(
        self,
        flagged_tests: List[TestCase],
        module_summaries: Dict[int, ModuleSummary]
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
            batch_verifications = self._generate_verifications_for_batch(batch, verification_context)
            all_verifications.update(batch_verifications)

        return all_verifications

    def _build_verification_context(self, module_summaries: Dict[int, ModuleSummary]) -> str:
        """Build context about what each module can verify.

        Lists ALL modules (not just those with can_verify_states) so the LLM
        can discover cross-module verification opportunities.  Modules that
        CAN verify states are highlighted.

        Example output:
            MODULES (can_verify_states highlighted):
            - Dashboard:
                Summary: ...
                Can verify: activity_schedule, user_dashboard   <-- highlighted
            - Course Page:
                Summary: ...
                (no verifiable states)
        """
        lines = ["ALL MODULES (modules that can verify states are marked with \u2713):"]
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
        verification_context: str
    ) -> Dict[str, List[IdealVerification]]:
        """Generate ideal verifications for a batch of test cases"""

        # Format test cases for prompt
        tests_text = ""
        for tc in test_cases:
            tests_text += f"""
Test ID: {tc.id}
Title: {tc.title}
Module: {tc.module_title}
Workflow: {tc.workflow}
Modifies State: {', '.join(tc.modifies_state) if tc.modifies_state else 'Unknown'}
Steps: {'; '.join(tc.steps[:5])}
Expected Result: {tc.expected_result}
---
"""

        prompt = f"""Generate IDEAL verification scenarios for each test case below.

{verification_context}

TEST CASES NEEDING VERIFICATION:
{tests_text}

For each test case, generate 1-3 ideal verifications that would confirm the test truly succeeded.

CRITICAL — CROSS-MODULE VERIFICATION RULE:
When choosing target_module, consider ALL modules in the list above — not just the module
where the action takes place. Many actions are best verified from a DIFFERENT module.

Examples of cross-module verification:
  - Teacher grades a submission (module: "Assignment Submissions") → verified in
    "Assignment (Student View)" where the student sees their grade, AND in
    "Gradebook / Grader Report" where the grade appears in the report.
  - Teacher creates an assignment (module: "Adding Activities") → verified in
    "Course Page" where the activity appears in sections, AND in
    "Activities (Student View)" where students see it listed.
  - User enrolls a participant (module: "Participants") → verified in
    "Participants" list where the new user appears (same module is OK too).

If MULTIPLE modules can verify the same state, generate SEPARATE ideal verifications
for each target module. This maximises the chance of finding a matching test case later.

For EACH verification, you MUST choose an execution_strategy:
- "before_after": When the action MODIFIES existing data. The same verification test runs
  BEFORE the action (to record the baseline) and AFTER (to confirm the change).
  You must fill in before_action and after_action.
- "after_only": When the action CREATES new data or a result that didn't previously exist.
  The verification test only needs to run after the action to confirm the new data appeared.

Also determine if verification requires a DIFFERENT user session:
- requires_different_session: true if a different user must log in to verify
- session_note: description of who needs to be logged in (e.g., "Login as the recipient user")

═══════════════════════════════════════════════════════════
FEW-SHOT EXAMPLES — Study these patterns carefully
═══════════════════════════════════════════════════════════

EXAMPLE 1: Money movement between two entities (transfer, send, move)
─────────────────────────────────────────────────────────
If a test moves money/value from entity A to entity B, you MUST generate at
minimum TWO verifications — one for the SOURCE and one for the DESTINATION:

  Verification 1 (SOURCE side):
    description: "Verify the source balance decreased by the transferred amount"
    execution_strategy: "before_after"
    before_action: "Record the source balance before the action"
    after_action: "Compare the source balance and confirm it decreased by the exact amount"

  Verification 2 (DESTINATION side):
    description: "Verify the destination balance increased by the transferred amount"
    execution_strategy: "before_after"
    before_action: "Record the destination balance before the action"
    after_action: "Compare the destination balance and confirm it increased by the exact amount"

This pattern applies to ANY action that moves value between two places: fund transfers,
payments to payees, inter-account movements, sending money, etc. Always verify BOTH sides.

EXAMPLE 2: Action that creates a new entity AND deducts from an existing one
─────────────────────────────────────────────────────────
If a test creates something new (new record, new entry) AND also affects an
existing value, generate verifications for BOTH aspects:

  Verification 1 (NEW entity):
    description: "Verify the newly created entity appears in the appropriate listing"
    execution_strategy: "after_only"
    before_action: ""
    after_action: ""

  Verification 2 (EXISTING value affected):
    description: "Verify the existing value reflects the deduction from creation"
    execution_strategy: "before_after"
    before_action: "Record the current value before the action"
    after_action: "Compare and confirm the value decreased by the expected amount"

EXAMPLE 3: Content creation verified on a different page (LMS/CMS pattern)
─────────────────────────────────────────────────────────
If a test creates content (e.g., a teacher adds an assignment, a user creates a post,
an admin adds a course), verify the content appears on ALL relevant listing/overview pages,
not just the page where it was created:

  Verification 1 (Primary listing page):
    description: "Verify the new content appears on the main listing page in the correct section"
    execution_strategy: "after_only"
    before_action: ""
    after_action: ""

  Verification 2 (Secondary navigation/index):
    description: "Verify the new content appears in the navigation index or sidebar"
    execution_strategy: "after_only"
    before_action: ""
    after_action: ""

This pattern applies to ANY content management action: adding activities to a course,
creating forum posts, uploading resources, adding quiz questions, etc. Content created
in a configuration/editing interface should be verified in the user-facing views.

EXAMPLE 4: Grading/scoring action that updates a cross-module report (LMS pattern)
─────────────────────────────────────────────────────────
If a test enters a grade, score, or evaluation in one module and the result should appear
in a summary/report module, generate verifications for BOTH the individual entry and
any aggregate values that may change:

  Verification 1 (Individual entry in report):
    description: "Verify the individual grade/score appears in the report module"
    execution_strategy: "after_only"
    before_action: ""
    after_action: ""

  Verification 2 (Aggregate/total updated):
    description: "Verify the course total or average is updated to reflect the new entry"
    execution_strategy: "before_after"
    before_action: "Record the current course total/average before the grading action"
    after_action: "Compare and confirm the total/average changed to include the new grade"

This pattern applies to ANY action that adds data which feeds into an aggregate report:
grading assignments, recording attendance, completing course activities, etc.

EXAMPLE 5: Multi-user action requiring session switch (LMS/collaborative pattern)
─────────────────────────────────────────────────────────
If a test is performed by one user but the result should be visible to a DIFFERENT user
(e.g., a student submits work and the teacher should see it, or one user sends a message
and the recipient should receive it), you MUST set requires_different_session:

  Verification 1 (Visible to different user):
    description: "Verify the action result is visible from the other user's perspective"
    execution_strategy: "after_only"
    before_action: ""
    after_action: ""
    requires_different_session: true
    session_note: "Login as the other user role (e.g., teacher, recipient, admin)"

This pattern applies to ANY cross-user scenario: student submissions visible to teachers,
messages between users, enrollment actions visible to enrolled users, shared content
visible to collaborators, etc.

═══════════════════════════════════════════════════════════

CRITICAL RULES FOR FINANCIAL/DATA-MOVEMENT ACTIONS:

1. NEVER generate a single vague verification like "Verify the action was successful"
   or "Verify the transfer status". Instead, break it down into CONCRETE observable
   data checks (balances, counts, records).

2. For ANY action that moves value/data between two entities, you MUST verify BOTH
   the source AND the destination separately. Each gets its own verification entry.

3. For ANY action that changes a numeric value (balance, count, quantity), ALWAYS use
   "before_after" strategy — record the number before, check it changed after.

4. For ANY action that creates a new record/entry, use "after_only" — check it exists.

5. Think about ALL side effects of an action. A payment doesn't just "succeed" — it
   reduces a balance, creates a transaction record, updates a payee history, etc.
   Generate verifications for each observable side effect.

6. For ANY action in an LMS/CMS that creates content (assignments, activities, courses,
   forum posts, resources), verify the content appears in ALL relevant listing/overview
   pages, not just the page where it was created. Also consider whether the action
   affects aggregates (gradebook totals, activity counts) and verify those too.

═══════════════════════════════════════════════════════════

Return JSON:
{{
    "test_verifications": [
        {{
            "test_id": "TEST-001",
            "ideal_verifications": [
                {{
                    "description": "Concrete description of what to verify",
                    "target_module": "Module name from the context above that can display this data",
                    "verification_action": "Specific action to take on that module",
                    "expected_change": "Exact expected outcome",
                    "state_to_verify": "state_name_from_module_summaries",
                    "execution_strategy": "before_after",
                    "before_action": "What to record before the action",
                    "after_action": "What to compare/check after the action",
                    "requires_different_session": false,
                    "session_note": ""
                }}
            ]
        }}
    ]
}}

IMPORTANT:
- target_module should be a module that CAN verify the state (from the context above)
- Be specific about what to check and what the expected outcome is
- Include ALL test cases in the output
- Only generate verifications that are actually achievable with the available modules
- If no verification is possible, return empty ideal_verifications array
- Use actual module names from the provided context, not placeholder names
- Use state names that match those in the module summaries
- ALWAYS set execution_strategy — default to "before_after" for any value/quantity change,
  "after_only" for new record/entry creation
- For before_action: describe what specific data to RECORD before the action
- For after_action: describe exactly what COMPARISON or CHECK to perform after"""

        try:
            result = self.call_llm_json(prompt, max_tokens=4000)

            verifications = {}
            for item in result.get("test_verifications", []):
                test_id = item.get("test_id")
                if test_id:
                    ideal_list = []
                    for v in item.get("ideal_verifications", []):
                        ideal_list.append(IdealVerification(
                            description=v.get("description", ""),
                            target_module=v.get("target_module", ""),
                            verification_action=v.get("verification_action", ""),
                            expected_change=v.get("expected_change", ""),
                            state_to_verify=v.get("state_to_verify", ""),
                            execution_strategy=v.get("execution_strategy", "after_only"),
                            before_action=v.get("before_action", ""),
                            after_action=v.get("after_action", ""),
                            requires_different_session=v.get("requires_different_session", False),
                            session_note=v.get("session_note", ""),
                        ))
                    verifications[test_id] = ideal_list

            return verifications

        except Exception as e:
            print(f"Warning: Ideal verification generation failed: {e}")
            return {}
