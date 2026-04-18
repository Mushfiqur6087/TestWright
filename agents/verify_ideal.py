from typing import List, Dict, Optional

from testwright.agents.base import BaseAgent
from testwright.models.schemas import (
    IdealVerification,
    ModuleSummary,
    ProjectContext,
    TestCase,
)


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
        verification_context: str,
        project_context: Optional[ProjectContext] = None,
    ) -> Dict[str, List[IdealVerification]]:
        """Generate ideal verifications for a batch of test cases"""

        # Project context block (domain awareness)
        project_str = ""
        if project_context and (project_context.project_name or project_context.navigation_overview):
            project_str = f"""PROJECT CONTEXT:
You are generating verifications for: {project_context.project_name or 'Unknown project'}
Application overview: {project_context.navigation_overview or 'Not provided'}

Use this context to phrase verifications in terms appropriate to the application domain.
The patterns below are DOMAIN-AGNOSTIC; apply them using the project's own vocabulary.

"""

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

        prompt = f"""{project_str}Generate IDEAL verification scenarios for each test case below.

{verification_context}

TEST CASES NEEDING VERIFICATION:
{tests_text}

For each test case, generate 1-3 ideal verifications that would confirm the test truly succeeded.

CRITICAL — CROSS-MODULE VERIFICATION RULE:
When choosing target_module, consider ALL modules in the list above — not just the module
where the action takes place. Many actions are best verified from a DIFFERENT module.

Cross-module verification applies across every domain. A few illustrations:
  - A transfer/payment in an operational module → verified on the source AND destination
    detail pages where current balances are displayed.
  - A submission/content creation → verified on the listing/index page where the new
    entity appears, AND on any aggregated report that includes it.
  - A status transition (Approve/Disburse/Publish) → verified on the detail page where the
    status badge is displayed AND in any audit/history module that logs the transition.
  - A booking/reservation → verified on the user's "My Bookings" listing AND in the
    confirmation/receipt section.

If MULTIPLE modules can verify the same state, generate SEPARATE ideal verifications
for each target module. This maximises the chance of finding a matching test case later.

For EACH verification, you MUST choose an execution_strategy:
- "before_after": When the action MODIFIES existing data. The same verification test runs
  BEFORE the action (to record the baseline) and AFTER (to compare and confirm the change).
  You must fill in before_action and after_action.
- "after_only": When the action CREATES new data or a result that didn't previously exist.
  The verification test only needs to run after the action to confirm the new data appeared.

Also determine if verification requires a DIFFERENT user session:
- requires_different_session: true if a different user must log in to verify
- session_note: description of who needs to be logged in (e.g., "Login as the recipient user")

═══════════════════════════════════════════════════════════
FEW-SHOT EXAMPLES — Each example states the PATTERN first,
then shows a domain-specific instance. Apply the PATTERN using
whatever domain vocabulary matches the current project.
═══════════════════════════════════════════════════════════

EXAMPLE 1 — Value movement between two entities
─────────────────────────────────────────────────────────
Pattern: A test moves a quantitative value from entity A to entity B. Verify BOTH
the source decrease AND the destination increase as separate verifications.
Applies to: fund transfers between accounts, payments to payees, inventory
moves between warehouses, point/credit transfers between users, allocations
between GL accounts, stock transfers between portfolios.

Domain-specific instance:
  Verification 1 (SOURCE side):
    description: "Verify the source value decreased by the exact amount"
    execution_strategy: "before_after"
    before_action: "Record the source value before the action"
    after_action: "Compare and confirm the source value decreased by the exact amount"

  Verification 2 (DESTINATION side):
    description: "Verify the destination value increased by the exact amount"
    execution_strategy: "before_after"
    before_action: "Record the destination value before the action"
    after_action: "Compare and confirm the destination value increased by the exact amount"

EXAMPLE 2 — Entity creation that also affects an existing value
─────────────────────────────────────────────────────────
Pattern: A test creates a new entity AND affects an existing numeric value.
Generate verifications for BOTH sides: the new entity's appearance AND the
before/after on the affected value.
Applies to: opening a new account that draws an initial deposit, creating a
loan that decrements available product quota, booking a seat that decrements
remaining inventory, enrolling a student that decrements class capacity.

Domain-specific instance:
  Verification 1 (NEW entity):
    description: "Verify the newly created entity appears in its listing/overview"
    execution_strategy: "after_only"
    before_action: ""
    after_action: ""

  Verification 2 (EXISTING value affected):
    description: "Verify the existing value reflects the deduction from creation"
    execution_strategy: "before_after"
    before_action: "Record the current value before the action"
    after_action: "Compare and confirm the value decreased by the expected amount"

EXAMPLE 3 — Content creation verified on other pages
─────────────────────────────────────────────────────────
Pattern: A test creates content/child entity in a configuration/editing UI.
Verify the content appears on ALL relevant listing/index pages AND in any
aggregate that should reflect the new entity.
Applies to: adding activities to a course, creating forum posts, uploading
resources, adding loan accounts under a client, adding rooms under a hotel,
creating support tickets, adding portfolio items, adding catalog products.

Domain-specific instance:
  Verification 1 (Primary listing page):
    description: "Verify the new content appears on the primary listing/overview"
    execution_strategy: "after_only"
    before_action: ""
    after_action: ""

  Verification 2 (Secondary navigation/index):
    description: "Verify the new content appears in a secondary index or sidebar"
    execution_strategy: "after_only"
    before_action: ""
    after_action: ""

EXAMPLE 4 — Entry that updates an aggregate report
─────────────────────────────────────────────────────────
Pattern: A test enters individual data that feeds into a summary/report/aggregate.
Generate verifications for BOTH the individual entry AND the aggregate change.
Applies to: grading assignments → gradebook totals, recording attendance →
attendance rate, approving expenses → departmental spend, closing a journal
entry → trial balance, completing a task → progress indicator.

Domain-specific instance:
  Verification 1 (Individual entry in report):
    description: "Verify the individual entry appears in the report module"
    execution_strategy: "after_only"
    before_action: ""
    after_action: ""

  Verification 2 (Aggregate/total updated):
    description: "Verify the aggregate total is updated to reflect the new entry"
    execution_strategy: "before_after"
    before_action: "Record the aggregate total before the action"
    after_action: "Compare and confirm the total changed to include the new entry"

EXAMPLE 5 — Cross-user visibility requiring session switch
─────────────────────────────────────────────────────────
Pattern: A test is performed by user A but the result should be visible to user B.
Set requires_different_session=true.
Applies to: student submission visible to teacher, customer message visible to
support agent, shared document visible to collaborator, loan application visible
to approver, booking visible to vendor, escalation visible to manager.

Domain-specific instance:
  Verification 1 (Visible to different user):
    description: "Verify the action result is visible from the other user's perspective"
    execution_strategy: "after_only"
    before_action: ""
    after_action: ""
    requires_different_session: true
    session_note: "Login as the other user role (e.g., approver, recipient, admin)"

EXAMPLE 6 — Booking / reservation funnel verification
─────────────────────────────────────────────────────────
Pattern: A test completes a booking or reservation funnel. Verify it appears in
the user's booking history/listing AND that a confirmation reference is visible,
and (if the spec describes it) that any linked wallet/credit/inventory updated.
Applies to: hotel/flight/tour/car bookings, tickets, appointments, reservations,
class enrolments, event registrations.

Domain-specific instance:
  Verification 1 (My Bookings listing):
    description: "Verify the new booking appears in the user's bookings listing"
    execution_strategy: "after_only"
    before_action: ""
    after_action: ""

  Verification 2 (Confirmation reference / receipt):
    description: "Verify a confirmation reference or receipt is displayed for the booking"
    execution_strategy: "after_only"
    before_action: ""
    after_action: ""

  Verification 3 (Wallet/inventory if applicable):
    description: "Verify the linked wallet/credit/inventory decreased by the booking amount"
    execution_strategy: "before_after"
    before_action: "Record the wallet/credit/inventory value before the booking"
    after_action: "Compare and confirm the value decreased appropriately"

EXAMPLE 7 — Status-machine transition with audit trail
─────────────────────────────────────────────────────────
Pattern: A test transitions an entity from one status to another (Approve, Reject,
Disburse, Publish, Activate, Close). Verify (a) the status badge on the detail page
changed, (b) the set of available action buttons changed, (c) an audit/history
entry was created, (d) if accounting is affected, a corresponding journal/ledger
entry appears.
Applies to: loan approval/disbursement/closure, client activation, account close,
article publish/unpublish, ticket resolution, workflow approvals, document signing.

Domain-specific instance:
  Verification 1 (Status badge changed):
    description: "Verify the entity's status badge on the detail page reflects the new status"
    execution_strategy: "after_only"
    before_action: ""
    after_action: ""

  Verification 2 (Action button set updated):
    description: "Verify the action buttons available on the detail page match the new status"
    execution_strategy: "after_only"
    before_action: ""
    after_action: ""

  Verification 3 (Audit/history entry):
    description: "Verify a new audit/history entry exists for this transition"
    execution_strategy: "after_only"
    before_action: ""
    after_action: ""

  Verification 4 (Accounting side effect, if applicable):
    description: "Verify a corresponding journal/ledger entry appears in the accounting module"
    execution_strategy: "after_only"
    before_action: ""
    after_action: ""

═══════════════════════════════════════════════════════════

CRITICAL RULES FOR STATEFUL ACTIONS:

1. NEVER generate a single vague verification like "Verify the action was successful"
   or "Verify the transfer status". Instead, break it down into CONCRETE observable
   data checks (values, counts, records, badges, log entries).

2. For ANY action that moves value/data between two entities, you MUST verify BOTH
   the source AND the destination separately. Each gets its own verification entry.

3. For ANY action that changes a numeric value (balance, count, quantity, progress),
   ALWAYS use "before_after" strategy — record the number before, check it changed
   after.

4. For ANY action that creates a new record/entry, use "after_only" — check it exists.

5. Think about ALL side effects of an action. An action rarely just "succeeds" in one
   place — it may update a record, change an aggregate, create an audit/history entry,
   update a status badge, or change the set of actions available on the page. Generate
   verifications for each observable side effect.

6. For ANY action that creates content or child entities (assignments, forum posts,
   loan accounts under a client, rooms under a hotel, items under a portfolio), verify
   the content appears on ALL relevant listing/index pages AND verify any aggregates
   that should reflect the new entity (counts, totals, progress indicators).

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
            result = self.call_llm_json(prompt, max_tokens=16000)

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
