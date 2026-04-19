"""
Stage 2 — Ideal Plan Generator.

Designs the ideal POST-VERIFICATION plan for a flagged source test.
ZERO knowledge of the test catalog — the signature itself enforces the
isolation contract (no ``all_test_cases`` / ``test_cases`` parameter).
"""

from typing import Dict, List

from testwright.agents.base import BaseAgent
from testwright.models.schemas import (
    IdealExecutionPlan,
    IdealPlanStep,
    ModuleSummary,
    ParsedFunctionalDescription,
    TestCase,
)


_VALID_PHASES = {"pre_verify", "navigate", "session_switch", "action", "post_verify"}
_VALID_VERIFICATION_TYPES = {
    "existence", "absence", "field_persistence", "status_transition",
    "cascading_update", "credential_change", "session_persistence",
    "financial_delta",
}


class PlanGeneratorAgent(BaseAgent):
    """Stage 2 of the post-verification pipeline.

    Produces a free-form ordered list of plan steps for each flagged test,
    grounded only in the functional spec. Has NO access to the test catalog
    so it cannot rationalize its ideal toward what happens to exist.
    """

    @property
    def name(self) -> str:
        return "Plan Generator Agent"

    @property
    def system_prompt(self) -> str:
        return """You are a QA test architect. Your job is to design the IDEAL POST-VERIFICATION PLAN for a
test that modifies persistent state. You describe exactly what a tester should do to prove
the state change really happened — not just that a success message appeared.

YOU DO NOT KNOW WHAT TESTS ALREADY EXIST. Design the ideal plan as if you could write any
observation test you wanted. Do not compromise the ideal to make it easier to match later.

A plan is an ORDERED SEQUENCE OF STEPS. Each step has exactly one PHASE. You may use any
phase, in any order, as many times as the spec demands. The only structural rules are:
  - Exactly ONE action step per plan.
  - pre_verify steps come before action; post_verify steps come after.
  - navigate and session_switch are setup steps — they only make sense immediately before
    a pre_verify or post_verify step, or chained with another navigate/session_switch.

PHASE DEFINITIONS:

  pre_verify      Observe a baseline value BEFORE the action. Use when a later post_verify
                  will need to compare against a starting value (e.g., balance before vs.
                  after). A pre_verify step MUST name:
                    - target_module: where the observation happens
                    - state_to_observe: the state name from that module's can_verify_states
                    - field_or_record: the EXACT field or record to observe (e.g.,
                      "source_account.balance", "profile.email_address")
                    - expected_observation: the expected current value (e.g., "current
                      balance X, to be recorded")
                    - spec_citation: the behavior/rule that says this field is observable here

  navigate        Move from the current module to another module. Insert immediately before
                  a pre_verify or post_verify step whose target_module differs from the
                  previous step's module. Only field needed: target_module.

  session_switch  Log out the current user and log in as a different role. Insert immediately
                  before any step that must be performed by a different role than the
                  previous step. Name the observer_role explicitly (e.g., "checker", "admin",
                  "teacher", "recipient", "auditor"). Use this whenever verification requires
                  a role change — it is NOT limited to any one scenario type.

  action          Execute the source test — the state-changing operation. Exactly one per
                  plan. You do not need to describe it; the source test is known. Just place
                  it at the correct position (after any pre_verify steps, before any
                  post_verify steps).

  post_verify     Observe the system AFTER the action to confirm the change persisted. A
                  post_verify step MUST name:
                    - target_module: where the observation happens
                    - state_to_observe: the state name from that module's can_verify_states
                    - field_or_record: the EXACT field or record to observe
                    - expected_observation: the expected value, delta, presence, or absence
                      (e.g., "Balance decreased by transfer_amount", "New row with
                      status=Executed exists", "Old record no longer visible")
                    - spec_citation: the behavior/rule that says this observation should be
                      true after the action

COMPOSITION IS FREE-FORM. You may, for example:
  - Emit several pre_verify steps across different modules (each preceded by a navigate).
  - Emit several post_verify steps in different modules (each preceded by a navigate).
  - Emit pre_verify as one role, then session_switch + post_verify as another role.
  - Chain session_switch + navigate + post_verify more than once (observe as role A, then
    switch to role B, then observe again).
  - Emit only post_verify steps (no pre_verify) when the action is a creation and there's
    nothing to baseline.
  - Emit the same field's pre_verify and post_verify pair when a value is being modified.
The shape is whatever the spec demands. Do not shoehorn the plan into a template.

VERIFICATION TYPES — label every post_verify step with one (metadata):
  existence            A new record appears in a listing with correct field values.
  absence              A deleted/hidden record is provably gone from the observer's view.
  field_persistence    An updated value survives page refresh AND re-login.
  status_transition    A status badge changed AND the available action buttons changed.
  cascading_update     Related data in another module reflects the change.
  credential_change    Old credential fails; new credential succeeds.
  session_persistence  A change persists after logout then login.
  financial_delta      Both sides of a value transfer balance (source -, destination +).
These labels are for reporting only — they do not dictate plan shape.

HARD RULES:

  1. A success toast is NEVER proof. Do not design a post_verify step that only checks a
     toast. Observe the underlying data.

  2. Every pre_verify and post_verify step must be grounded in the spec. Cite the behavior
     or rule that says this data should be visible at this point. If no spec text supports
     it, do not emit the step. If a step would contradict a SYSTEM CONSTRAINT, do not emit
     it.

  3. Behavioral > UI-presence. Prefer "attempt login with old password fails" over
     "password updated banner appears". Prefer "record visible in listing" over "record
     created message".

  4. Value transfers always need two post_verify steps — one per side (source and
     destination) — even if they happen to be in the same module.

  5. Credential changes always need BOTH: a post_verify that old credential fails + new
     credential succeeds, AND a post_verify that the change survives logout/login.

  6. Use module names exactly as written in the spec. Use state names from
     module_summaries.can_verify_states. Use roles the spec actually mentions.

  7. Name the EXACT field or record in every pre_verify and post_verify step. "Verify the
     balance updated" is not good enough. "In Accounts Overview, source account row,
     Balance column, expected to be previous balance minus transfer amount" is good.

  8. When a pre_verify and a matching post_verify observe the same field, they are the
     baseline/comparison pair — use the SAME target_module, state_to_observe, and
     field_or_record on both."""

    def run(
        self,
        flagged_tests: List[TestCase],
        parsed_desc: ParsedFunctionalDescription,
        module_summaries: Dict[int, ModuleSummary],
    ) -> Dict[str, IdealExecutionPlan]:
        """Generate ideal plans. NOTE: no ``test_cases`` parameter — the
        absence is the isolation contract with Stage 3.
        """

        tests_needing = [tc for tc in flagged_tests if tc.needs_post_verification]
        if not tests_needing:
            return {}

        capabilities_block = self._build_capabilities_block(module_summaries)
        spec_block = self._build_spec_block(parsed_desc)
        constraints_block = self._build_constraints_block(parsed_desc.system_constraints or [])
        project_block = self._build_project_block(parsed_desc)

        plans: Dict[str, IdealExecutionPlan] = {}
        batch_size = 8
        for i in range(0, len(tests_needing), batch_size):
            batch = tests_needing[i:i + batch_size]
            plans.update(
                self._generate_batch(
                    batch=batch,
                    capabilities_block=capabilities_block,
                    spec_block=spec_block,
                    constraints_block=constraints_block,
                    project_block=project_block,
                )
            )
        return plans

    # ------------------------------------------------------------------ blocks

    def _build_project_block(self, parsed_desc: ParsedFunctionalDescription) -> str:
        if not (parsed_desc.project_name or parsed_desc.navigation_overview):
            return ""
        return (
            f"PROJECT: {parsed_desc.project_name or 'Unknown'}\n"
            f"OVERVIEW: {parsed_desc.navigation_overview or 'Not provided'}\n\n"
        )

    def _build_capabilities_block(self, module_summaries: Dict[int, ModuleSummary]) -> str:
        lines = ["MODULE CAPABILITIES (\u2713 = can verify states):"]
        for summary in module_summaries.values():
            marker = "\u2713" if summary.can_verify_states else " "
            lines.append(f"- [{marker}] {summary.module_title}:")
            lines.append(f"    Summary: {summary.summary}")
            if summary.can_verify_states:
                lines.append(f"    can_verify_states: {', '.join(summary.can_verify_states)}")
            if summary.action_states:
                lines.append(f"    action_states: {', '.join(summary.action_states)}")
        return "\n".join(lines)

    def _build_spec_block(self, parsed_desc: ParsedFunctionalDescription) -> str:
        blocks: List[str] = []
        for m in parsed_desc.modules:
            if not (m.expected_behaviors or m.business_rules):
                continue
            behaviors = "\n".join(f"    - {b}" for b in m.expected_behaviors) or "    (none)"
            rules = "\n".join(f"    - {r}" for r in m.business_rules) or "    (none)"
            blocks.append(
                f"[{m.title}]\n"
                f"  Expected behaviors:\n{behaviors}\n"
                f"  Business rules:\n{rules}"
            )
        if not blocks:
            return ""
        return "FULL SPEC (every module's expected_behaviors and business_rules):\n" + "\n\n".join(blocks)

    def _build_constraints_block(self, system_constraints: List[str]) -> str:
        if not system_constraints:
            return ""
        bullets = "\n".join(f"- {c}" for c in system_constraints)
        return (
            "SYSTEM CONSTRAINTS (the system explicitly does NOT do these):\n"
            f"{bullets}\n"
            "Do NOT emit a post_verify whose expected_observation contradicts a constraint.\n"
        )

    # ------------------------------------------------------------------ batch

    def _generate_batch(
        self,
        batch: List[TestCase],
        capabilities_block: str,
        spec_block: str,
        constraints_block: str,
        project_block: str,
    ) -> Dict[str, IdealExecutionPlan]:
        tests_text = ""
        for tc in batch:
            mods = ", ".join(tc.modifies_state) if tc.modifies_state else "unknown"
            kind = tc.modification_kind or "unknown"
            tests_text += (
                f"\nTest ID: {tc.id}\n"
                f"Title: {tc.title}\n"
                f"Module: {tc.module_title}\n"
                f"Workflow: {tc.workflow}\n"
                f"Modification kind: {kind}\n"
                f"Modifies state: {mods}\n"
                f"Steps: {'; '.join(tc.steps[:5])}\n"
                f"Expected: {tc.expected_result}\n"
                f"---\n"
            )

        prompt = f"""{project_block}{constraints_block}
{spec_block}

{capabilities_block}

SOURCE TESTS (design a plan for each):
{tests_text}

OUTPUT JSON:
{{
  "plans": [
    {{
      "source_test_id": "TEST-001",
      "verification_types": ["existence", "financial_delta"],
      "rationale": "Brief — why this coverage.",
      "steps": [
        {{"phase": "pre_verify" | "navigate" | "session_switch" | "action" | "post_verify",
         "description": "...",
         "target_module": "...",
         "state_to_observe": "...",
         "field_or_record": "...",
         "expected_observation": "...",
         "observer_role": "...",
         "spec_citation": "..."}}
      ]
    }}
  ]
}}

Include EVERY source_test_id in the output. If a test cannot be verified for some reason,
return an empty steps array for it."""

        try:
            result = self.call_llm_json(prompt, max_tokens=16000)
        except Exception as e:
            print(f"Warning: Plan generation failed for batch: {e}")
            return {}

        plans: Dict[str, IdealExecutionPlan] = {}
        for item in result.get("plans", []):
            source_test_id = item.get("source_test_id", "")
            if not source_test_id:
                continue

            raw_types = item.get("verification_types") or []
            verification_types = [t for t in raw_types if t in _VALID_VERIFICATION_TYPES]

            steps: List[IdealPlanStep] = []
            for raw_step in item.get("steps", []) or []:
                phase = raw_step.get("phase", "")
                if phase not in _VALID_PHASES:
                    continue
                steps.append(IdealPlanStep(
                    phase=phase,
                    description=raw_step.get("description", ""),
                    target_module=raw_step.get("target_module", ""),
                    state_to_observe=raw_step.get("state_to_observe", ""),
                    field_or_record=raw_step.get("field_or_record", ""),
                    expected_observation=raw_step.get("expected_observation", ""),
                    observer_role=raw_step.get("observer_role", ""),
                    spec_citation=raw_step.get("spec_citation", ""),
                ))

            steps = self._enforce_invariants(steps)

            plans[source_test_id] = IdealExecutionPlan(
                source_test_id=source_test_id,
                verification_types=verification_types,
                steps=steps,
                rationale=item.get("rationale", ""),
            )
        return plans

    # ------------------------------------------------------------------ invariants

    @staticmethod
    def _enforce_invariants(steps: List[IdealPlanStep]) -> List[IdealPlanStep]:
        """Enforce the only structural rules we care about:
        - Exactly one action step (keep first occurrence; drop extras).
        - pre_verify steps only before the action; post_verify only after.
        - Trailing navigate/session_switch with no observation after is useless → drop.
        """
        if not steps:
            return steps

        # Find first action index; if none, let it be (reporter will synthesize one).
        action_idx = next((i for i, s in enumerate(steps) if s.phase == "action"), -1)

        cleaned: List[IdealPlanStep] = []
        seen_action = False
        for i, s in enumerate(steps):
            if s.phase == "action":
                if seen_action:
                    continue  # drop duplicate action
                seen_action = True
                cleaned.append(s)
                continue
            if s.phase == "pre_verify" and action_idx >= 0 and i > action_idx:
                continue  # pre_verify after action → ignore
            if s.phase == "post_verify" and action_idx >= 0 and i < action_idx:
                continue  # post_verify before action → ignore
            cleaned.append(s)

        # Trim trailing navigate/session_switch that don't lead to anything observable.
        while cleaned and cleaned[-1].phase in ("navigate", "session_switch"):
            cleaned.pop()

        return cleaned
