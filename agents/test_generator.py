from typing import List

from testwright.agents.base import BaseAgent
from testwright.models.schemas import WorkflowChunk, TestCase


class TestGenerationAgent(BaseAgent):
    """Agent responsible for generating test cases from workflow chunks"""

    @property
    def name(self) -> str:
        return "Test Generation Agent"

    @property
    def system_prompt(self) -> str:
        return """You are an expert QA engineer specializing in test case design for web automation.

Your task is to generate comprehensive test cases that cover the functionality described.
The application domain may be anything — consumer banking, LMS, travel booking, enterprise
microfinance, CMS, SaaS admin, etc. The rules below are DOMAIN-AGNOSTIC; apply them using
vocabulary appropriate to the specific project you are testing.

GUIDING PRINCIPLES:
1. Cover all scenarios mentioned in the functional description
2. Tests must be executable by a browser automation tool
3. Test steps should describe actions on the current page - NOT navigation to the page
4. Generate granular TEST CASES (one scenario per test), but CONCISE STEPS inside each test

STEP CONCISENESS — critical for readability:
A well-formed test case is typically 2–6 steps, NOT one step per field interaction.
- GROUP form-filling into a single step naming all fields:
    "Fill all required fields (First Name, Last Name, Email, Password)"
  NOT 4 separate "Fill X" steps.
- Keep distinct user actions (clicks, selections, dropdown picks, file uploads,
  multi-step wizard transitions) as separate steps.
- Split field-filling into separate steps ONLY when:
    (a) field order matters (e.g., selecting country unlocks the state dropdown),
    (b) one field triggers dynamic UI that affects later fields, or
    (c) the test specifically verifies single-field behavior (e.g., a "<field> empty"
        negative test only touches that one field).
- For multi-step wizards, use one step PER WIZARD PAGE, not per field:
    "Fill all required fields in Step 1 (Details)" → "Click Next" →
    "Fill all required fields in Step 2 (Terms)" → "Click Submit"
- For per-field negative tests, use: "Fill all other required fields, leave <field> empty"

TEST TYPES:
1. POSITIVE TESTS: Verify success scenarios work as described
2. NEGATIVE TESTS: Test error conditions and validation rules mentioned
3. EDGE CASE TESTS: Boundary values, special characters, format variations if relevant

NEGATIVE TESTS — Required field validation (HYBRID policy):

DEFAULT: Generate ONE consolidated "all required fields empty" test per workflow:
    title: "Submit with all required fields empty"
    steps: ["Leave all required fields empty", "Click \"<Submit button>\""]
    expected_result: "Validation errors shown for all required fields."

GENERATE PER-FIELD EMPTY TESTS (one test per field) ONLY WHEN the spec explicitly describes:
  (a) Different error messages per field (e.g., "First Name is required" vs
      "Invalid SSN format" vs "Password must contain a number"),
  (b) Different validation rules per field (e.g., one field has a length/format
      rule that others don't), or
  (c) A field-specific behavior the spec calls out (e.g., "SSN must match an
      existing customer record").

Do NOT generate N empty-field tests by default just because there are N required
fields. The spec must justify the split.

Other negative-test rules (always apply):
- One test per invalid-format field (one "Invalid email format" — NOT sub-variants
  like "missing @", "multiple @", "missing domain")
- Separate tests for mismatch scenarios (password mismatch, confirm-password mismatch,
  account number mismatch, etc.)
- Separate tests for constraint violations (insufficient balance, unmet prerequisite,
  ineligible date, quota exceeded, duplicate unique value, …)

POSITIVE TESTS:
1. If multiple valid input types are mentioned (e.g., "username OR email"), create
   separate tests for EACH.
2. If multiple entity categories exist (e.g., distinct account types, distinct
   service tabs), create ONE positive test for the primary path, PLUS a test for
   an alternative ONLY if the spec describes different behavior/fields for it.
3. Include state verification tests — verify changes are reflected after actions
   (e.g., "newly created entity appears in its listing", "numeric value updated
   after a modification action").
4. Include pre-populated/display tests (e.g., "fields pre-filled with user data")
   when the spec mentions them.

BOUNDARY/EDGE TESTS:
1. For numeric/monetary values: test exactly at a stated boundary value, and just
   below/above if boundary semantics are described.
2. For text fields: test maximum length ONLY if the spec explicitly states a
   character limit. DO NOT invent length constraints.
3. For date fields: test same start/end date, future dates if the spec allows.

DO NOT generate tests for:
- Device-specific interactions (touch gestures, mobile-only features)
- Browser-specific features (right-click menus, opening in new tabs)
- Network conditions (offline, slow connection, server errors)
- Stress scenarios (rapid clicking, load testing)
- Invented display-absence checks ("table not displayed", "logo missing") —
  only test error conditions explicitly described in the spec.

CRUD / LIFECYCLE COMPLETENESS — mandatory:
When the spec describes operations beyond Create, you MUST generate tests for them.
Scan the workflow description, business rules, and expected behaviors for these signals:
  - Any mention of Edit, "edit the", modify, update, change a field → Edit test
  - Any mention of Delete, remove, discard, "no longer needed" → Delete test
  - Close, Deactivate, Disable, Inactivate, "Is Active" toggle, active/inactive
    status → lifecycle test (Disable + Re-enable when both are implied)
  - Creation form / multi-step wizard described → creation happy-path test AND
    an Edit test (wizard-backed detail pages admit Edit via the same form)
  - Status transitions described (e.g., Pending → Active → Closed) → one test
    per transition

Short-spec modules are especially prone to missing these. A spec that says "detail view
with Edit and Delete options" requires BOTH an Edit test AND a Delete test — not just a
test that verifies the buttons exist.

Do NOT confuse "verify button exists" with "test the operation". Verifying that an Edit
button is visible is a display test. Actually clicking Edit, modifying fields, saving,
and verifying the update — THAT is the Edit test. Generate both when applicable.

TAB / SECTION COVERAGE — when spec lists tabs by name:
If the spec names tabs on a detail page (e.g., "Tabs show Notes, Documents,
Family Members, Dividends, Calendar/Meeting"), generate ONE test per named tab
that exercises its primary purpose:
  - Notes → "Add note" (enter text, submit, verify appears in list)
  - Documents → "Upload document" (attach file, submit, verify listed)
  - Family Members / Members → "Add member to <entity>"
  - Dividends / posted distributions → "View dividend distributions" (columns)
  - Calendar / Meeting → "Schedule meeting for <entity>"
  - Repayment Schedule / Summary / tabs described via TABLE columns →
    ONE test verifying the listed columns or fields are displayed

A bare "Tabs show A, B, C" statement IS an implicit functional requirement for
each tab. Do not skip a tab because its action verb is not spelled out — the tab
name itself signals the action (Notes → add note, Documents → upload document).

WITHIN-WORKFLOW DEDUPLICATION — critical:
Before emitting your test list, scan it for pairs that share the SAME (action verb,
target object, expected outcome) modulo UI entry point. Collapse such pairs into ONE
test. If a feature is reachable from multiple buttons/cards/banners on the same page,
test the function ONCE and append the entry variants to the title.
  Example: instead of 5 separate "Book Now applies promo" tests (one for featured card,
  one for banner, one for search result, one for sidebar, one for footer), emit ONE test
  titled: "Book Now applies promotional code (triggerable from: featured card, banner,
  search result)". Do NOT emit N tests for N entry points.

Similarly, if a workflow has actions that only differ by a document type or category
(e.g., "Download Invoice", "Download Voucher", "Download Confirmation"), emit ONE test
per distinct document type — but if the download mechanism is identical, a single
consolidated test is preferred.

MENU / CONTROL COMPOSITION TESTS:
If you emit a test that asserts a menu, dropdown, or toolbar lists a specific
set of options (e.g., "Three-dot menu lists edit, duplicate, hide, delete,
move"), emit that test AT MOST ONCE per control — not once per action the menu
contains. Do NOT re-verify the menu composition inside each action-specific
test. Action-specific tests (e.g., "Edit section via three-dot menu") assume
the menu composition is already covered by the single composition test.

CROSS-WORKFLOW PRECONDITION RULE:
Do NOT emit standalone tests that only verify a precondition of the workflow
under test. If the workflow is "Rename section" and the spec says editing
requires Edit mode to be enabled, the precondition "Enable Edit mode shows
inline controls" belongs in the test's `preconditions` field, NOT as its own
separate test case. Preconditions are stated, not retested. The one exception
is when enabling/toggling that precondition IS the workflow itself (e.g., a
dedicated "Toggle edit mode" workflow).

FIELD / COLUMN VISIBILITY DEDUPLICATION:
Do NOT generate multiple tests that verify the same page fields or table columns are
displayed. If a detail page shows the same core fields (e.g., amount, date, status,
interest rate) regardless of entity status, generate ONE field-visibility test — do NOT
repeat the same field-presence check under different status contexts. Similarly, do NOT
generate separate tests for each tab's presence if the tabs are the same across statuses.
One canonical "detail page displays expected fields" test per entity page is sufficient.

UI-FEASIBILITY — do NOT generate these test patterns:
- Invalid-value tests for <select>/dropdown, radio, checkbox, or date-picker widgets
  (they only offer allowed values — test the allowed values, never "invalid selection")
- "Required empty" / validation-error tests for widgets with no required state
  (sort dropdowns, view toggles, pagination, currency/language switchers)
- "Required empty" / validation-error tests for single-click actions (Approve,
  Reject, Activate, Undo, Enable, Disable, Delete, Close) — these are button-clicks
  with at most a confirmation prompt, NOT data-entry forms
- Format-validity tests on numeric steppers, sliders, or constrained numeric widgets
EXCEPTION: if the spec describes a dialog WITH input fields (e.g., "Approve dialog
with Approved On Date and Note"), that dialog IS a form and its fields CAN be tested
for empty/invalid values.
Only text/textarea inputs admit format negatives. File uploads DO admit type/size
tests when the spec describes file restrictions.

EVIDENCE-BASED NEGATIVE AND EDGE TESTS — enforced:
For EVERY test where test_type is "negative" or "edge_case", you MUST provide a
"spec_evidence" field containing a VERBATIM 3-to-15-word substring copied from the
business rules or expected behaviors above that justifies the failure mode you are
testing. The phrase must appear literally in the spec text — paraphrased or invented
quotes will be rejected and the test dropped.

  Example of valid evidence for a "SSN empty" negative test:
      "spec_evidence": "SSN must match an existing customer record"
      (this phrase must appear verbatim in the Business Rules or Expected Behaviors)

  Example of invalid evidence (fabricated):
      "spec_evidence": "the cancellation dialog requires additional input"
      (fails if "cancellation dialog requires additional input" is not in the spec)

If you cannot find a verbatim phrase in the spec that justifies a particular negative
or edge test, DO NOT emit that test. The spec must ground every failure case you
generate. Positive tests do NOT require spec_evidence.

For each test case, provide:
- Clear, concise title (no hardcoded values in the title)
- Single precondition statement (or "None")
- CONCISE test steps (see STEP CONCISENESS above) — actions on THIS page only
- Single expected result
- Priority (High for core functionality, Medium for validations, Low for edge cases)"""

    def run(self, chunk: WorkflowChunk) -> List[TestCase]:
        """Generate test cases for a workflow chunk"""

        # Build context from chunk
        items_str = ", ".join(chunk.related_items) if chunk.related_items else "Not specified"
        rules_str = "\n".join([f"  - {r}" for r in chunk.related_rules]) if chunk.related_rules else "None"
        behaviors_str = "\n".join([f"  - {b}" for b in chunk.related_behaviors]) if chunk.related_behaviors else "None"

        # Project context block (domain awareness for downstream LLM calls)
        project_str = ""
        if chunk.project_context and (chunk.project_context.project_name or chunk.project_context.navigation_overview):
            project_str = f"""PROJECT CONTEXT:
You are generating tests for: {chunk.project_context.project_name or 'Unknown project'}
Application overview: {chunk.project_context.navigation_overview or 'Not provided'}

Use this context to choose domain-appropriate terminology. Do NOT force banking or
LMS idioms onto projects where they don't fit.

"""

        # Build cross-workflow dedup context if sibling workflows exist
        sibling_str = ""
        if chunk.sibling_workflows:
            sibling_str = f"""
CROSS-WORKFLOW DEDUP RULE:
This module has sibling workflows: {', '.join(chunk.sibling_workflows)}.
For fields shared across workflows, generate field-empty and field-invalid tests ONLY ONCE — do not repeat them for each workflow.
Only generate validation tests for fields UNIQUE to this workflow: '{chunk.workflow_name}'.
"""

        prompt = f"""{project_str}Generate test cases for this workflow.

Module: {chunk.module_title}
Workflow: {chunk.workflow_name}
Description: {chunk.workflow_description}

Available Items/Elements: {items_str}

Business Rules:
{rules_str}

Expected Behaviors:
{behaviors_str}
{sibling_str}
Generate test cases in this JSON format:
{{
    "test_cases": [
        {{
            "title": "Short descriptive title",
            "test_type": "positive|negative|edge_case",
            "priority": "High|Medium|Low",
            "preconditions": "Single precondition statement or None",
            "steps": ["Step 1", "Step 2", "Step 3"],
            "expected_result": "Single expected outcome",
            "spec_evidence": "VERBATIM 3-15 word phrase from the Business Rules or Expected Behaviors above (REQUIRED for negative/edge_case, OMIT for positive)"
        }}
    ]
}}

REQUIREMENTS:
1. Steps describe actions on THIS page only — no navigation steps
2. DO NOT hardcode values — use generic descriptive text
3. Every NEGATIVE and EDGE_CASE test MUST include "spec_evidence" — a VERBATIM substring from Business Rules or Expected Behaviors above (paraphrasing = rejection)

═══════════════════════════════════════════════════════════
FEW-SHOT EXAMPLES — Study the STEP FORMAT, not the domain
═══════════════════════════════════════════════════════════

EXAMPLE A — Authentication / form recovery (short form, all-at-once fill):
{{
  "title": "Retrieve forgotten credentials with valid identity details",
  "test_type": "positive",
  "priority": "High",
  "preconditions": "None",
  "steps": [
    "Click \\"Forgot login info?\\"",
    "Fill all required fields (First Name, Last Name, Address, City, State, Zip Code, SSN)",
    "Click \\"Find My Login Info\\""
  ],
  "expected_result": "Credentials retrieved and displayed."
}}

EXAMPLE B — Consolidated required-field validation (default negative case):
{{
  "title": "Submit with all required fields empty",
  "test_type": "negative",
  "priority": "Medium",
  "preconditions": "None",
  "steps": [
    "Leave all required fields empty",
    "Click \\"Submit\\""
  ],
  "expected_result": "Validation errors shown for all required fields.",
  "spec_evidence": "all required fields must be filled"
}}

EXAMPLE C — Per-field negative test (ONLY when spec describes per-field behavior):
{{
  "title": "Submit with SSN field empty",
  "test_type": "negative",
  "priority": "Medium",
  "preconditions": "None",
  "steps": [
    "Fill all other required fields, leave SSN empty",
    "Click \\"Find My Login Info\\""
  ],
  "expected_result": "Validation error indicating SSN is required.",
  "spec_evidence": "SSN must match an existing customer record"
}}

EXAMPLE C2 — Entry-point deduplication (feature reachable from multiple buttons):
{{
  "title": "Apply promotional code via Book Now (triggerable from: featured card, banner, search result)",
  "test_type": "positive",
  "priority": "High",
  "preconditions": "At least one active promotional offer exists.",
  "steps": [
    "Click any \\"Book Now\\" entry point for an active offer",
    "Fill all required booking fields",
    "Click \\"Confirm Booking\\""
  ],
  "expected_result": "The promotional code is applied and the discounted rate is reflected in the booking total."
}}

EXAMPLE D — Multi-step wizard (one step per wizard page, not per field):
{{
  "title": "Create entity via multi-step wizard with valid data",
  "test_type": "positive",
  "priority": "High",
  "preconditions": "None",
  "steps": [
    "Click \\"New\\"",
    "Fill all required fields in Step 1 (Details)",
    "Click \\"Next\\"",
    "Fill all required fields in Step 2 (Terms)",
    "Click \\"Next\\"",
    "Click \\"Submit\\""
  ],
  "expected_result": "Entity created and listed with the expected initial status."
}}

EXAMPLE E — Search → filter → book/select funnel:
{{
  "title": "Complete a booking after searching and selecting an item",
  "test_type": "positive",
  "priority": "High",
  "preconditions": "None",
  "steps": [
    "Fill search form with valid criteria",
    "Click \\"Search\\"",
    "Select a result from the list",
    "Fill all required booking fields",
    "Click \\"Confirm Booking\\""
  ],
  "expected_result": "Booking confirmation with reference number is displayed."
}}

EXAMPLE F — State-transition action (single button on a status-driven page):
{{
  "title": "Approve a pending entity",
  "test_type": "positive",
  "priority": "High",
  "preconditions": "An entity exists in \\"Pending Approval\\" status.",
  "steps": [
    "Click \\"Approve\\"",
    "Confirm in the approval dialog"
  ],
  "expected_result": "Entity status changes to \\"Approved\\" and the available action buttons update accordingly."
}}

EXAMPLE G — Value-modification action (quantity/amount/number):
{{
  "title": "Modify a numeric value with a valid amount",
  "test_type": "positive",
  "priority": "High",
  "preconditions": "None",
  "steps": [
    "Fill all required fields (including the new amount)",
    "Click \\"Submit\\""
  ],
  "expected_result": "The numeric value updates and the confirmation is displayed."
}}

EXAMPLE H — Edit entity (click Edit, modify, save, verify update):
{{
  "title": "Edit an existing entity's details",
  "test_type": "positive",
  "priority": "High",
  "preconditions": "An entity exists and its detail page is open.",
  "steps": [
    "Click \\"Edit\\"",
    "Modify one or more editable fields",
    "Click \\"Save\\""
  ],
  "expected_result": "Detail page reflects the updated values."
}}

EXAMPLE I — Delete entity (click Delete, confirm, verify removal):
{{
  "title": "Delete an existing entity",
  "test_type": "positive",
  "priority": "High",
  "preconditions": "An entity exists and its detail page or listing row is visible.",
  "steps": [
    "Click \\"Delete\\"",
    "Confirm deletion in the confirmation dialog"
  ],
  "expected_result": "Entity is removed and no longer appears in the listing."
}}

EXAMPLE J — Tab-action (exercise primary action of a named tab):
{{
  "title": "Add a note to an entity via the Notes tab",
  "test_type": "positive",
  "priority": "Medium",
  "preconditions": "Entity exists and its detail page is open.",
  "steps": [
    "Click the \\"Notes\\" tab",
    "Click \\"Add Note\\"",
    "Fill the note text",
    "Click \\"Submit\\""
  ],
  "expected_result": "Note is saved and appears in the notes list."
}}

═══════════════════════════════════════════════════════════

GRANULARITY vs. CONCISENESS:

- Test CASE granularity: one SCENARIO per test (do not combine multiple independent scenarios).
- Step CONCISENESS inside each test: group form-filling, keep clicks distinct.
These two rules work together — many test cases, few steps per test.

IMPORTANT VALUE HANDLING:
- Do not hardcode specific values in steps.
  CORRECT: "Fill all required fields (First Name, Last Name, Email, Password)"
  WRONG:   "Fill First Name with 'John', Last Name with 'Doe', Email with 'john@example.com'..."
- Describe the INTENT of the value, not the value itself (e.g., "Fill a valid email address").

COVERAGE CHECKLIST (verify all applicable items are covered):
[ ] Primary creation / submission scenario (always emit when a creation form is described)
[ ] All CRUD/lifecycle operations described in the spec (see CRUD rule above —
    Edit, Delete, Close, Disable/Enable, status transitions)
[ ] Primary action for each named tab (Notes → add, Documents → upload,
    Family Members → add, Dividends → view, Calendar → schedule)
[ ] All valid input variations (separate tests only when behavior differs)
[ ] Required field validation (ONE consolidated test; per-field only if spec differentiates)
[ ] Each validation rule explicitly stated in the spec
[ ] Mismatch scenarios (password, confirm, account number, …)
[ ] Constraint-violation scenarios explicitly described (insufficient balance,
    unmet prerequisite, ineligible date, quota exceeded, duplicate unique value, …)
[ ] Boundary values ONLY for explicitly specified limits
[ ] State-change verification (when the action modifies persistent data)
"""

        try:
            result = self.call_llm_json(prompt, max_tokens=16000)
            return self._parse_test_results(result, chunk)
        except Exception as e:
            print(f"Warning: Test generation failed for {chunk.workflow_name}: {e}")
            return []

    def _parse_test_results(self, result: dict, chunk: WorkflowChunk) -> List[TestCase]:
        """Parse LLM response into TestCase objects.

        Enforces the evidence rule: every negative / edge_case test must carry a
        ``spec_evidence`` field whose value is a verbatim substring of the chunk's
        workflow text (description + related rules + related behaviors). Tests
        without evidence are dropped as hallucinated requirements.
        """

        tests = []
        raw_tests = result.get("test_cases", [])

        # Pre-build the evidence haystack once per chunk
        haystack = (
            chunk.workflow_description + " " +
            " ".join(chunk.related_rules) + " " +
            " ".join(chunk.related_behaviors)
        ).lower()

        dropped_hallucinations = 0

        for i, raw_test in enumerate(raw_tests):
            # Validate and normalize test_type
            test_type = raw_test.get("test_type", "positive").lower()
            if test_type not in ["positive", "negative", "edge_case"]:
                test_type = "positive"

            # Validate and normalize priority
            priority = raw_test.get("priority", "Medium")
            if priority not in ["High", "Medium", "Low"]:
                priority = "Medium"

            # Normalize preconditions
            preconditions = raw_test.get("preconditions", "None")
            if not preconditions or preconditions.lower() in ["none", "n/a", ""]:
                preconditions = "None"

            # Normalize expected_result
            expected = raw_test.get("expected_result", "")
            if isinstance(expected, list):
                expected = "; ".join(expected)

            # Evidence enforcement for negative / edge_case tests
            spec_evidence = ""
            if test_type in ("negative", "edge_case"):
                evidence_raw = (raw_test.get("spec_evidence") or "").strip()
                evidence_lower = evidence_raw.lower()
                word_count = len(evidence_raw.split())
                if (
                    not evidence_lower
                    or word_count < 3
                    or word_count > 15
                    or evidence_lower not in haystack
                ):
                    dropped_hallucinations += 1
                    continue
                spec_evidence = evidence_raw

            test_case = TestCase(
                id="",  # Will be assigned by AssemblerAgent
                title=raw_test.get("title", f"Test Case {i+1}"),
                module_id=chunk.module_id,
                module_title=chunk.module_title,
                workflow=chunk.workflow_name,
                test_type=test_type,
                priority=priority,
                preconditions=preconditions,
                steps=raw_test.get("steps", []),
                expected_result=expected,
                spec_evidence=spec_evidence,
            )
            tests.append(test_case)

        if dropped_hallucinations:
            print(
                f"    [{self._ts()}] ~~ {self.name} | dropped {dropped_hallucinations} "
                f"hallucinated negative/edge test(s) in '{chunk.workflow_name}'"
            )

        return tests
