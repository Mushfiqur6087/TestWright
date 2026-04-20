"""Verification planner agent.

Given a positive test case, decide whether it needs verification and, if so,
produce a verification record per verification_structure_spec.md.

Credential-mutation scenarios are explicitly excluded and skipped.
"""

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional

from testwright.agents.base import BaseAgent
from testwright.models.schemas import NavigationGraph, TestCase, VerificationRecord


ALLOWED_TYPES = {
    "same_actor_navigation",
    "cross_actor",
    "out_of_band",
    "unobservable_by_design",
}
ALLOWED_COVERAGE = {"verifiable", "manual_only", "not_coverable"}


def _load_verification_spec() -> str:
    """Read verification_structure_spec.md from the repo root."""
    here = Path(__file__).resolve().parent
    # agents/ -> repo root
    spec_path = here.parent / "verification_structure_spec.md"
    if not spec_path.exists():
        raise FileNotFoundError(
            f"verification_structure_spec.md not found at {spec_path}. "
            "The verification planner requires this spec to drive type selection."
        )
    return spec_path.read_text(encoding="utf-8")


_VERIFICATION_SPEC = _load_verification_spec()


_EXCLUSION_AND_OUTPUT_DIRECTIVE = """

--------------------------------------------------------------------------------
PIPELINE-SPECIFIC DIRECTIVES (OVERRIDE SPEC WHERE THEY CONFLICT)
--------------------------------------------------------------------------------

DEFAULT IS SKIP. Only emit a verification record when the test case has a
PERSISTENT, OUT-OF-VIEW side effect that the test case itself CANNOT already
prove on its own screen. If the test case's own `expected_result` already
fully asserts the outcome on the same page, respond with `{"skip": true}`.
Be strict — err on the side of skipping.

Skip rules (respond with EXACTLY `{"skip": true}`):

1. Credential mutations (password change/reset, username change, any auth
   credential update). We do not verify these.

2. In-page dynamic effects (filter updates, sorts, same-page success
   banners, client-side validation, toggles, modals opening/closing). The
   test case already asserts these on-screen — no verification record is
   needed. Do NOT emit a verification type for these. Just skip.

3. Static page-load assertions (reading values on the page as rendered,
   confirming a table exists, verifying a field is present with no user
   action triggering a state change). These are observations, not
   verifications. Skip.

4. Pure navigation, read-only views, and anything with no persistent state
   change (no DB write, no cross-screen effect, no external side channel).
   Skip.

5. Negative / edge / standard tests. We only verify positive tests where a
   meaningful persistent effect exists. Skip otherwise.

Emit a record ONLY for one of these four types:

    - same_actor_navigation   — persistent effect visible on a DIFFERENT
                                page or after a full navigation (e.g.,
                                account balance change visible on
                                Accounts Overview after a transfer).
                                Prefer pre_check + post_check with a
                                concrete `expected_change`.
    - cross_actor             — effect is only observable to a DIFFERENT
                                user role (e.g., teacher creates an
                                assignment; student sees it on login).
    - out_of_band             — effect leaves the app (email, SMS, webhook,
                                external system).
    - unobservable_by_design  — spec explicitly states the effect cannot
                                be verified in this environment (e.g.,
                                mock system notes, disabled subsystem).
                                Provide an alternative_assertion.

Do NOT include `login_required` anywhere in the output.
For `same_actor_navigation`, `post_check` should include only:
`navigate_to`, `observe`, and `expected_change`.

For state-mutating financial / data flows (transfer, bill payment,
purchase, booking, order placement, etc.), ALWAYS prefer
`same_actor_navigation` with a pre/post observation on the page that
shows the persistent effect (balance, list of accounts, list of orders,
etc.) — even if an in-page success banner is also shown. The banner is
NOT a verification; the persistent state change IS. If only part of the
effect is observable in-app (e.g., external transfer where the remote
account is unreachable), still verify the observable side (source
balance decrease) and add a `coverage_note` explaining what is
unobservable.

Choose `navigate_to` values ONLY from the provided "Valid navigation
targets" list in the user message. Do not invent page names.

Response format: a SINGLE JSON object, nothing else. No prose. No
markdown fence. Either `{"skip": true}` or a full verification record
matching §2 of the spec: test_case_id, verification_type, coverage,
coverage_note (omit when coverage is "verifiable"), body (shape depends
on verification_type).
"""


_WORKED_EXAMPLES = """

--------------------------------------------------------------------------------
WORKED EXAMPLES (one per allowed type)
--------------------------------------------------------------------------------

Example A — same_actor_navigation (Parabank transfer):
{
  "test_case_id": "5.TRAFUN-001",
  "verification_type": "same_actor_navigation",
  "coverage": "verifiable",
  "body": {
    "pre_check": {
      "navigate_to": "Accounts Overview",
      "observe": ["balance of source account", "balance of destination account"]
    },
    "post_check": {
      "navigate_to": "Accounts Overview",
      "observe": ["balance of source account", "balance of destination account"],
      "expected_change": "Source account balance decreased by transfer amount; destination account balance increased by the same amount; combined total unchanged."
    }
  }
}

Example B — same_actor_navigation with partially observable effect
(Parabank external transfer — destination account is on another bank
and is not observable in-app, but the source balance decrease is):
{
  "test_case_id": "5.TRAFUN-002",
  "verification_type": "same_actor_navigation",
  "coverage": "verifiable",
  "coverage_note": "Destination account is external to Parabank and cannot be observed in-app; only the source-side effect is verified.",
  "body": {
    "pre_check": {
      "navigate_to": "Accounts Overview",
      "observe": ["balance of source account"]
    },
    "post_check": {
      "navigate_to": "Accounts Overview",
      "observe": ["balance of source account"],
      "expected_change": "Source account balance decreased by the transfer amount."
    }
  }
}

Example C — cross_actor (Moodle teacher -> student):
{
  "test_case_id": "MOODLE-ASSIGN-TC001",
  "verification_type": "cross_actor",
  "coverage": "verifiable",
  "body": {
    "actor_a": {
      "role": "teacher",
      "action": "Create assignment 'Week 1 Essay' in Course X with due date, online text submission enabled"
    },
    "actor_b": {
      "role": "student",
      "session": "new_session",
      "navigate_to": "Course X -> Activities tab -> Assignments section",
      "observe": ["assignment name", "due date", "submission status column"],
      "expected_change": "Assignment 'Week 1 Essay' appears in the Assignments section with correct due date and submission status 'No submission'."
    }
  }
}

Example D — out_of_band (PHPTravels booking email):
{
  "test_case_id": "PHPTRV-BOOK-003",
  "verification_type": "out_of_band",
  "coverage": "manual_only",
  "coverage_note": "Booking confirmation email is sent to an external inbox and cannot be observed within the PHPTravels application UI.",
  "body": {
    "trigger_action": "Complete hotel booking payment with valid credit card",
    "channel": "email",
    "recipient": "email address entered in the booking lead passenger form",
    "expected_content": [
      "Unique booking reference number",
      "Hotel name",
      "Check-in date",
      "Check-out date",
      "Room type",
      "Total amount paid",
      "Cancellation policy"
    ],
    "in_app_partial_check": {
      "navigate_to": "Booking Confirmation page (immediate post-payment screen)",
      "observe": "Reference number displayed on page matches reference number in email"
    },
    "verification_method": "Access test inbox (Mailtrap or equivalent). Confirm email arrives within 2 minutes. Verify all expected_content fields are present."
  }
}

Example E — unobservable_by_design (Parabank mock collateral debit):
{
  "test_case_id": "7.LOAFUN-002",
  "verification_type": "unobservable_by_design",
  "coverage": "not_coverable",
  "coverage_note": "Parabank mock system does not debit collateral accounts. Balance assertions on collateral account will always show no change regardless of test outcome.",
  "body": {
    "reason": "Functional spec states: 'In this mock system, no actual balance debits occur.'",
    "suppressed_assertion": "Collateral account balance should decrease by down payment amount on loan approval.",
    "alternative_assertion": "Verify a new loan account appears in Accounts Overview with correct principal, type 'Loan', status 'Active', and open date matching today.",
    "environment_condition": "Mock environment - balance mutation globally disabled"
  }
}

Example F — skip (credential mutation, in-page-only effect, static
page-load observation, or any case already fully asserted on-screen):
{"skip": true}
"""


_SYSTEM_PROMPT = (
    _VERIFICATION_SPEC
    + _EXCLUSION_AND_OUTPUT_DIRECTIVE
    + _WORKED_EXAMPLES
)


def _body_is_valid_for_type(verification_type: str, body: dict) -> bool:
    """Soft structural check so obviously broken outputs are retried."""
    if not isinstance(body, dict):
        return False
    if verification_type == "same_actor_navigation":
        return isinstance(body.get("pre_check"), dict) and isinstance(body.get("post_check"), dict)
    if verification_type == "cross_actor":
        return isinstance(body.get("actor_a"), dict) and isinstance(body.get("actor_b"), dict)
    if verification_type == "out_of_band":
        return all(k in body for k in ("trigger_action", "channel", "expected_content"))
    if verification_type == "unobservable_by_design":
        return all(k in body for k in ("reason", "suppressed_assertion", "alternative_assertion"))
    return False


class VerificationPlannerAgent(BaseAgent):
    """Per-test-case verification planner; fans out over tests in parallel."""

    @property
    def name(self) -> str:
        return "Verification Planner Agent"

    @property
    def system_prompt(self) -> str:
        return _SYSTEM_PROMPT

    def _build_user_prompt(
        self,
        test_case: TestCase,
        spec_text: str,
        peer_specs: List[str],
        nav_node_titles: List[str],
    ) -> str:
        peer_block = ""
        if peer_specs:
            peer_block = "\n\n## Peer / Cross-role specs\n\n"
            for i, text in enumerate(peer_specs, start=1):
                peer_block += f"### Peer spec #{i}\n\n{text}\n\n"

        steps_str = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(test_case.steps))

        return f"""Decide verification for a single test case.

## Test case
- id: {test_case.id}
- title: {test_case.title}
- module_id: {test_case.module_id}
- module_title: {test_case.module_title}
- workflow: {test_case.workflow}
- test_type: {test_case.test_type}
- priority: {test_case.priority}
- preconditions: {test_case.preconditions}
- steps:
{steps_str}
- expected_result: {test_case.expected_result}
- spec_evidence: {test_case.spec_evidence}

## Valid navigation targets (use ONLY these for navigate_to)
{json.dumps(nav_node_titles, indent=2)}

## Primary functional specification

{spec_text}
{peer_block}

Respond with EXACTLY one JSON object: either `{{"skip": true}}` or a full
verification record per the spec. The record's `test_case_id` must equal
"{test_case.id}"."""

    def plan_one(
        self,
        test_case: TestCase,
        spec_text: str,
        peer_specs: List[str],
        nav_node_titles: List[str],
    ) -> Optional[VerificationRecord]:
        user_prompt = self._build_user_prompt(
            test_case=test_case,
            spec_text=spec_text,
            peer_specs=peer_specs,
            nav_node_titles=nav_node_titles,
        )

        try:
            parsed = self.call_llm_json(
                user_prompt=user_prompt,
                temperature=0.2,
                max_tokens=8000,
            )
        except Exception as e:
            print(f"    !! {self.name} | test {test_case.id} | LLM call failed: {e}")
            return None

        # Skip sentinel
        if isinstance(parsed, dict) and parsed.get("skip") is True:
            return None

        if not isinstance(parsed, dict):
            return None

        vtype = parsed.get("verification_type")
        coverage = parsed.get("coverage")
        body = parsed.get("body")
        note = parsed.get("coverage_note")

        if vtype in ("credential_mutation", "in_page_dynamic"):
            # Dropped per pipeline policy even if the model emits them.
            return None

        if vtype not in ALLOWED_TYPES:
            return None
        if coverage not in ALLOWED_COVERAGE:
            return None
        if coverage != "verifiable" and not note:
            return None
        if not _body_is_valid_for_type(vtype, body or {}):
            return None

        return VerificationRecord(
            test_case_id=parsed.get("test_case_id") or test_case.id,
            verification_type=vtype,
            coverage=coverage,
            coverage_note=note,
            body=body,
        )

    def run(
        self,
        test_cases: List[TestCase],
        spec_text: str,
        peer_specs: List[str],
        nav_graph: NavigationGraph,
        max_workers: int = 8,
    ) -> List[VerificationRecord]:
        nav_node_titles = [node.title for node in nav_graph.nodes.values()]

        records: List[VerificationRecord] = []
        if not test_cases:
            return records

        workers = max(1, int(max_workers))
        print(f"  - Planning verifications for {len(test_cases)} positive test cases "
              f"using {workers} parallel worker(s)")

        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {
                pool.submit(
                    self.plan_one, tc, spec_text, peer_specs, nav_node_titles
                ): tc.id
                for tc in test_cases
            }
            done = 0
            for fut in as_completed(futures):
                tc_id = futures[fut]
                done += 1
                try:
                    result = fut.result()
                except Exception as e:
                    print(f"    !! {self.name} | test {tc_id} | unexpected error: {e}")
                    result = None
                if result is not None:
                    records.append(result)
                if done % 10 == 0 or done == len(futures):
                    print(f"    .. progress {done}/{len(futures)} "
                          f"(kept {len(records)} so far)")

        records.sort(key=lambda r: r.test_case_id)
        return records


def compute_coverage_summary(records: List[VerificationRecord]) -> Dict[str, object]:
    """Aggregate counts per coverage level and verification type."""
    coverage_counts = {"verifiable": 0, "manual_only": 0, "not_coverable": 0}
    type_counts: Dict[str, int] = {t: 0 for t in ALLOWED_TYPES}

    for r in records:
        if r.coverage in coverage_counts:
            coverage_counts[r.coverage] += 1
        if r.verification_type in type_counts:
            type_counts[r.verification_type] += 1

    return {
        "total_records": len(records),
        "verifiable": coverage_counts["verifiable"],
        "manual_only": coverage_counts["manual_only"],
        "not_coverable": coverage_counts["not_coverable"],
        "by_type": type_counts,
    }
