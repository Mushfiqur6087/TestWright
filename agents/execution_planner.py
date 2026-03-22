from typing import List, Dict
from dataclasses import dataclass, field

from testwright.agents.base import BaseAgent
from testwright.models.schemas import TestCase


@dataclass
class ExecutionStep:
    """A single step in an execution sequence"""
    step: int                       # Step number
    phase: str                      # "pre_verify" | "navigate" | "session" | "action" | "post_verify"
    action: str                     # "execute_test" | "execute_test_partial" | "navigate" | "session_switch" | "manual"
    test_id: str = ""               # Test ID to execute (if action is execute_test*)
    test_title: str = ""            # Human-readable title
    purpose: str = ""               # Why this step exists
    note: str = ""                  # Execution instructions
    confidence: float = 0.0        # Match confidence (for test execution steps)
    limitation: str = ""            # If partial match, what's missing

    def to_dict(self) -> dict:
        result = {
            "step": self.step,
            "phase": self.phase,
            "action": self.action,
        }
        if self.test_id:
            result["test_id"] = self.test_id
        if self.test_title:
            result["test_title"] = self.test_title
        if self.purpose:
            result["purpose"] = self.purpose
        if self.note:
            result["note"] = self.note
        if self.confidence:
            result["confidence"] = round(self.confidence, 2)
        if self.limitation:
            result["limitation"] = self.limitation
        return result


@dataclass
class ExecutionSequence:
    """Represents an execution sequence for verifying a test case"""
    source_test_id: str                     # The test that needs verification
    source_test_title: str                  # Title of the source test
    source_module: str = ""                 # Module of the source test
    execution_order: List[Dict] = field(default_factory=list)  # Ordered list of steps
    manual_steps: List[Dict] = field(default_factory=list)      # Manual steps if no automated test
    verification_coverage: str = ""         # "full" | "partial" | "none"
    notes: str = ""                          # Additional execution notes
    has_before_after: bool = False           # Whether this plan uses before/after strategy

    def to_dict(self) -> dict:
        return {
            "source_test_id": self.source_test_id,
            "source_test_title": self.source_test_title,
            "source_module": self.source_module,
            "execution_order": self.execution_order,
            "manual_steps": self.manual_steps,
            "verification_coverage": self.verification_coverage,
            "notes": self.notes,
            "has_before_after": self.has_before_after,
        }


class ExecutionPlanAgent(BaseAgent):
    """
    Agent responsible for compiling final execution plans.

    Builds PRE-VERIFY → ACTION → POST-VERIFY execution sequences:

    For "before_after" verifications:
      1. [PRE-VERIFY]  Run verification test → record baseline data
      2. [ACTION]       Run the source test → perform the state-changing action
      3. [POST-VERIFY]  Run verification test AGAIN → compare with baseline

    For "after_only" verifications:
      1. [ACTION]       Run the source test → perform the action
      2. [POST-VERIFY]  Run verification test → confirm expected outcome

    Navigation and session steps are inserted automatically when:
      - The verification test is on a DIFFERENT module/page than the action
      - The verification requires a DIFFERENT user session (logout + login)
    """

    @property
    def name(self) -> str:
        return "Execution Plan Agent"

    @property
    def system_prompt(self) -> str:
        return """You are a QA execution planner. Your job is to create clear, actionable
execution plans that tell testers exactly what steps to follow to verify test results.

You build execution sequences with these phases:
- PRE-VERIFY: Steps to record baseline data BEFORE the action
- NAVIGATE: Steps to move between pages/modules
- SESSION: Steps to switch user sessions (logout + login as different user)
- ACTION: The main test case being verified
- POST-VERIFY: Steps to check data AFTER the action

Keep execution notes concise and actionable."""

    def run(self, test_cases: List[TestCase]) -> Dict[str, ExecutionSequence]:
        """
        Generate execution plans for all tests needing post-verification.

        Args:
            test_cases: All test cases (flagged ones have post_verifications populated)

        Returns:
            Dictionary mapping test_id -> ExecutionSequence
        """

        # Filter to only tests that need post-verification AND have verifications
        tests_needing_plans = [
            tc for tc in test_cases
            if tc.needs_post_verification and tc.post_verifications
        ]

        if not tests_needing_plans:
            return {}

        execution_plans: Dict[str, ExecutionSequence] = {}

        # Build lookup for test details
        test_lookup = {tc.id: tc for tc in test_cases}

        for tc in tests_needing_plans:
            plan = self._build_execution_plan(tc, test_lookup)
            execution_plans[tc.id] = plan

        return execution_plans

    def _build_execution_plan(
        self,
        source_test: TestCase,
        test_lookup: Dict[str, TestCase]
    ) -> ExecutionSequence:
        """Build execution plan for a single test case with PRE → ACTION → POST ordering"""

        pre_verify_steps: List[ExecutionStep] = []
        post_verify_steps: List[ExecutionStep] = []
        manual_steps: List[Dict] = []
        found_count = 0
        total_verifications = len(source_test.post_verifications)
        has_before_after = False

        for pv in source_test.post_verifications:
            status = pv.get('status', 'not_found')
            strategy = pv.get('execution_strategy', 'after_only')
            matched_id = pv.get('matched_test_id', '')
            matched_test = test_lookup.get(matched_id) if matched_id else None
            matched_title = matched_test.title if matched_test else pv.get('matched_test_title', '')
            matched_module = matched_test.module_title if matched_test else ''
            ideal_desc = pv.get('ideal', '')
            before_action_desc = pv.get('before_action', '')
            after_action_desc = pv.get('after_action', '')
            needs_session_switch = pv.get('requires_different_session', False)
            session_note = pv.get('session_note', '')

            if status == 'not_found':
                manual_steps.append({
                    "purpose": ideal_desc,
                    "suggested_step": pv.get('suggested_manual_step', ''),
                    "reason": pv.get('reason', 'No matching test case found'),
                    "execution_strategy": strategy,
                })
                continue

            confidence = pv.get('confidence', 0.0)
            is_full = (status == 'found')
            limitation = pv.get('reason', '') if not is_full else ''

            if is_full:
                found_count += 1
            else:
                found_count += 0.5

            if strategy == 'before_after' and matched_id:
                has_before_after = True

                # --- PRE-VERIFY phase ---
                # Add navigation to verification module if different from source
                if matched_module and matched_module != source_test.module_title:
                    pre_verify_steps.append(ExecutionStep(
                        step=0,  # Will be renumbered later
                        phase="navigate",
                        action="navigate",
                        purpose=f"Navigate to {matched_module}",
                        note=f"Navigate from {source_test.module_title} to {matched_module} to record baseline data",
                    ))

                # Add session switch if needed for pre-verify
                if needs_session_switch:
                    pre_verify_steps.append(ExecutionStep(
                        step=0,
                        phase="session",
                        action="session_switch",
                        purpose=f"Switch user session for baseline recording",
                        note=session_note or "Log out and log in as the required user",
                    ))

                pre_verify_steps.append(ExecutionStep(
                    step=0,
                    phase="pre_verify",
                    action="execute_test" if is_full else "execute_test_partial",
                    test_id=matched_id,
                    test_title=matched_title,
                    purpose=before_action_desc or f"Record baseline: {ideal_desc}",
                    note=f"Run {matched_id} and RECORD the current values before the action",
                    confidence=confidence,
                    limitation=limitation,
                ))

                # --- POST-VERIFY phase ---
                # Add navigation back to verification module after the action
                if matched_module and matched_module != source_test.module_title:
                    post_verify_steps.append(ExecutionStep(
                        step=0,
                        phase="navigate",
                        action="navigate",
                        purpose=f"Navigate to {matched_module}",
                        note=f"Navigate from {source_test.module_title} to {matched_module} to verify the change",
                    ))

                # Add session switch if needed for post-verify
                if needs_session_switch:
                    post_verify_steps.append(ExecutionStep(
                        step=0,
                        phase="session",
                        action="session_switch",
                        purpose=f"Switch user session for verification",
                        note=session_note or "Log out and log in as the required user",
                    ))

                post_verify_steps.append(ExecutionStep(
                    step=0,
                    phase="post_verify",
                    action="execute_test" if is_full else "execute_test_partial",
                    test_id=matched_id,
                    test_title=matched_title,
                    purpose=after_action_desc or f"Verify change: {ideal_desc}",
                    note=f"Run {matched_id} AGAIN and COMPARE with baseline values recorded in pre-verify",
                    confidence=confidence,
                    limitation=limitation,
                ))

            elif matched_id:
                # --- after_only: POST-VERIFY only ---
                if matched_module and matched_module != source_test.module_title:
                    post_verify_steps.append(ExecutionStep(
                        step=0,
                        phase="navigate",
                        action="navigate",
                        purpose=f"Navigate to {matched_module}",
                        note=f"Navigate from {source_test.module_title} to {matched_module}",
                    ))

                if needs_session_switch:
                    post_verify_steps.append(ExecutionStep(
                        step=0,
                        phase="session",
                        action="session_switch",
                        purpose=f"Switch user session for verification",
                        note=session_note or "Log out and log in as the required user",
                    ))

                post_verify_steps.append(ExecutionStep(
                    step=0,
                    phase="post_verify",
                    action="execute_test" if is_full else "execute_test_partial",
                    test_id=matched_id,
                    test_title=matched_title,
                    purpose=ideal_desc,
                    note=pv.get('execution_note', f"Run {matched_id} to verify the outcome"),
                    confidence=confidence,
                    limitation=limitation,
                ))

        # --- Build final ordered execution sequence ---
        # Need to navigate back to source module before action if we navigated away for pre-verify
        action_nav_steps: List[ExecutionStep] = []
        if pre_verify_steps:
            # Check if last pre-verify was on a different module
            last_pre = pre_verify_steps[-1]
            if last_pre.phase == "pre_verify":
                last_pre_test = test_lookup.get(last_pre.test_id)
                if last_pre_test and last_pre_test.module_title != source_test.module_title:
                    action_nav_steps.append(ExecutionStep(
                        step=0,
                        phase="navigate",
                        action="navigate",
                        purpose=f"Navigate to {source_test.module_title}",
                        note=f"Return to {source_test.module_title} to execute the action",
                    ))

        # The ACTION step itself
        action_step = ExecutionStep(
            step=0,
            phase="action",
            action="execute_test",
            test_id=source_test.id,
            test_title=source_test.title,
            purpose=f"Execute the action: {source_test.title}",
            note=f"Run {source_test.id} — this is the state-changing action being verified",
            confidence=1.0,
        )

        # Assemble everything in order: PRE → NAV-BACK → ACTION → POST
        all_steps = pre_verify_steps + action_nav_steps + [action_step] + post_verify_steps

        # Renumber steps
        execution_order = []
        for i, step in enumerate(all_steps, 1):
            step.step = i
            execution_order.append(step.to_dict())

        # Determine coverage level
        if total_verifications > 0:
            coverage_ratio = found_count / total_verifications
            if coverage_ratio >= 1.0:
                coverage = "full"
            elif coverage_ratio >= 0.5:
                coverage = "partial"
            else:
                coverage = "minimal" if coverage_ratio > 0 else "none"
        else:
            coverage = "none"

        # Generate execution notes
        notes = self._generate_execution_notes(
            source_test, execution_order, manual_steps, has_before_after
        )

        return ExecutionSequence(
            source_test_id=source_test.id,
            source_test_title=source_test.title,
            source_module=source_test.module_title,
            execution_order=execution_order,
            manual_steps=manual_steps,
            verification_coverage=coverage,
            notes=notes,
            has_before_after=has_before_after,
        )

    def _generate_execution_notes(
        self,
        source_test: TestCase,
        execution_order: List[Dict],
        manual_steps: List[Dict],
        has_before_after: bool,
    ) -> str:
        """Generate human-readable execution notes"""

        if not execution_order and not manual_steps:
            return "No verification steps identified."

        notes_parts = []

        if has_before_after:
            pre_ids = [s['test_id'] for s in execution_order if s.get('phase') == 'pre_verify' and s.get('test_id')]
            post_ids = [s['test_id'] for s in execution_order if s.get('phase') == 'post_verify' and s.get('test_id')]

            if pre_ids:
                notes_parts.append(f"PRE: Record baseline with {', '.join(pre_ids)}")
            notes_parts.append(f"ACTION: Execute {source_test.id}")
            if post_ids:
                notes_parts.append(f"POST: Verify with {', '.join(post_ids)} (compare against baseline)")
        else:
            post_ids = [s['test_id'] for s in execution_order if s.get('phase') == 'post_verify' and s.get('test_id')]
            notes_parts.append(f"Execute {source_test.id}")
            if post_ids:
                notes_parts.append(f"then verify with {', '.join(post_ids)}")

        has_session = any(s.get('action') == 'session_switch' for s in execution_order)
        if has_session:
            notes_parts.append("(requires user session switch)")

        if manual_steps:
            notes_parts.append(f"Manual verification needed for {len(manual_steps)} item(s)")

        return " → ".join(notes_parts)

    def generate_execution_plan_summary(
        self,
        execution_plans: Dict[str, ExecutionSequence]
    ) -> Dict:
        """Generate a summary of all execution plans"""

        if not execution_plans:
            return {
                "total_plans": 0,
                "coverage_distribution": {},
                "total_automated_steps": 0,
                "total_manual_steps": 0,
                "automation_rate": 0,
                "before_after_plans": 0,
                "after_only_plans": 0,
            }

        coverage_dist = {"full": 0, "partial": 0, "minimal": 0, "none": 0}
        total_automated = 0
        total_manual = 0
        before_after_count = 0
        after_only_count = 0

        for plan in execution_plans.values():
            coverage_dist[plan.verification_coverage] = coverage_dist.get(plan.verification_coverage, 0) + 1
            # Count only pre_verify and post_verify steps as automated verification steps
            verify_steps = [s for s in plan.execution_order if s.get('phase') in ('pre_verify', 'post_verify')]
            total_automated += len(verify_steps)
            total_manual += len(plan.manual_steps)
            if plan.has_before_after:
                before_after_count += 1
            else:
                after_only_count += 1

        return {
            "total_plans": len(execution_plans),
            "coverage_distribution": coverage_dist,
            "total_automated_steps": total_automated,
            "total_manual_steps": total_manual,
            "automation_rate": round(
                total_automated / (total_automated + total_manual) * 100, 1
            ) if (total_automated + total_manual) > 0 else 0,
            "before_after_plans": before_after_count,
            "after_only_plans": after_only_count,
        }
