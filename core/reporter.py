"""
Stage 4 — Deterministic Reporter.

Walks paired (ideal_step, matched_step) lists and emits the final execution
sequences + populates exporter-compatible fields on each TestCase. No LLM.

Responsibilities:
  - Build ExecutionSequence per source test from the matched plan.
  - Defense-in-depth: demote a matched test whose module differs from the
    ideal step's target_module to a manual step.
  - Compute verification_coverage across non-procedural steps.
  - Populate TestCase.post_verifications, needs_new_verification_test,
    coverage_gaps, verification_coverage in a shape the existing exporter
    understands.
  - Derive aggregate plan-summary counters (labels are emergent from phase
    composition, not a fixed enum).
"""

from typing import Dict, List, Optional

from testwright.models.schemas import (
    ExecutionSequence,
    ExecutionStep,
    IdealExecutionPlan,
    IdealPlanStep,
    MatchedPlanStep,
    TestCase,
)


# ---------------------------------------------------------------------------
# Phase composition → reporter-friendly labels (for exporter compatibility).
# These are purely derived — there is no strategy enum anywhere in the plan.
# ---------------------------------------------------------------------------

def _derive_strategy_label(ideal_step: IdealPlanStep, plan: IdealExecutionPlan) -> str:
    """Pick a legacy-style strategy label for a post/pre_verify step, used
    only by the exporter for grouping. Composition-derived:
      - any session_switch in the plan → cross_user
      - any matching pre/post pair → before_after
      - otherwise → after_only
    """
    has_session = any(s.phase == "session_switch" for s in plan.steps)
    if has_session:
        return "cross_user"
    has_pre = any(s.phase == "pre_verify" for s in plan.steps)
    if has_pre:
        return "before_after"
    return "after_only"


def _observer_role_for_step(step_idx: int, plan: IdealExecutionPlan) -> str:
    """Return the observer_role of the nearest preceding session_switch, if any."""
    for i in range(step_idx, -1, -1):
        s = plan.steps[i]
        if s.phase == "session_switch" and s.observer_role:
            return s.observer_role
    return ""


# ---------------------------------------------------------------------------
# Core reporter
# ---------------------------------------------------------------------------

def run_reporter(
    ideal_plans: Dict[str, IdealExecutionPlan],
    matched_plans: Dict[str, List[MatchedPlanStep]],
    test_lookup: Dict[str, TestCase],
) -> Dict[str, ExecutionSequence]:
    """Walk every plan and produce an ExecutionSequence per source test.

    Also mutates the TestCase instances in ``test_lookup`` in place to
    populate exporter-compatible fields.
    """
    execution_plans: Dict[str, ExecutionSequence] = {}

    for source_id, plan in ideal_plans.items():
        source_test = test_lookup.get(source_id)
        if source_test is None:
            continue
        matched_steps = matched_plans.get(source_id) or []
        if len(matched_steps) != len(plan.steps):
            # Defensive: pad or trim so enumeration stays 1:1.
            matched_steps = _align_matches(plan.steps, matched_steps)

        execution_plans[source_id] = _build_sequence(
            plan=plan,
            matched_steps=matched_steps,
            source_test=source_test,
            test_lookup=test_lookup,
        )

    return execution_plans


def _align_matches(
    ideal_steps: List[IdealPlanStep],
    matched_steps: List[MatchedPlanStep],
) -> List[MatchedPlanStep]:
    aligned: List[MatchedPlanStep] = []
    for i, step in enumerate(ideal_steps):
        if i < len(matched_steps):
            aligned.append(matched_steps[i])
        else:
            aligned.append(MatchedPlanStep(
                ideal_step=step,
                status="procedural" if step.phase in ("navigate", "session_switch", "action") else "gap",
                grade_reason="Matcher produced no record for this step.",
            ))
    return aligned


def _build_sequence(
    plan: IdealExecutionPlan,
    matched_steps: List[MatchedPlanStep],
    source_test: TestCase,
    test_lookup: Dict[str, TestCase],
) -> ExecutionSequence:
    execution_order: List[ExecutionStep] = []
    manual_steps: List[Dict] = []
    post_verifications_out: List[Dict] = []
    needs_new_verification_test: List[Dict] = []
    coverage_gaps_reasons: List[str] = []

    found_count = 0
    partial_count = 0
    observation_count = 0

    step_counter = 0
    has_pre_verify = any(s.phase == "pre_verify" for s in plan.steps)
    has_session = any(s.phase == "session_switch" for s in plan.steps)

    for idx, (ideal, matched) in enumerate(zip(plan.steps, matched_steps)):
        phase = ideal.phase
        strategy_label = _derive_strategy_label(ideal, plan)

        if phase == "navigate":
            step_counter += 1
            execution_order.append(ExecutionStep(
                step=step_counter,
                phase="navigate",
                action="navigate",
                purpose=f"Navigate to {ideal.target_module}" if ideal.target_module else ideal.description,
                note=ideal.description or f"Navigate to {ideal.target_module}",
            ))
            continue

        if phase == "session_switch":
            step_counter += 1
            execution_order.append(ExecutionStep(
                step=step_counter,
                phase="session",
                action="session_switch",
                purpose=(
                    f"Switch to {ideal.observer_role}"
                    if ideal.observer_role else "Switch user session"
                ),
                note=ideal.description or (
                    f"Log out and log in as {ideal.observer_role}"
                    if ideal.observer_role else "Log out and log in as the required user"
                ),
            ))
            continue

        if phase == "action":
            step_counter += 1
            execution_order.append(ExecutionStep(
                step=step_counter,
                phase="action",
                action="execute_test",
                test_id=source_test.id,
                test_title=source_test.title,
                purpose=f"Execute the action: {source_test.title}",
                note=f"Run {source_test.id} — this is the state-changing action being verified",
                confidence=1.0,
            ))
            continue

        if phase not in ("pre_verify", "post_verify"):
            continue

        observation_count += 1
        observer_role = _observer_role_for_step(idx, plan)
        pv_entry = _build_post_verification_entry(
            ideal=ideal,
            matched=matched,
            strategy=strategy_label,
            observer_role=observer_role,
            has_session=has_session,
        )
        post_verifications_out.append(pv_entry)

        # Defense-in-depth: demote to manual if module mismatch slipped in.
        matched_test = (
            test_lookup.get(matched.matched_test_id) if matched.matched_test_id else None
        )
        module_mismatch = (
            matched_test is not None
            and ideal.target_module
            and matched_test.module_title != ideal.target_module
        )

        if matched.status == "gap" or matched.status not in ("found", "partial") or module_mismatch:
            reason = (
                matched.grade_reason
                if matched.status == "gap"
                else (
                    f"Module mismatch: matched test is in "
                    f"'{matched_test.module_title if matched_test else ''}', "
                    f"but verification should occur in '{ideal.target_module}'."
                )
                if module_mismatch
                else matched.grade_reason or "No matching test case found"
            )
            suggested_title = (
                matched.suggested_new_test_title
                or f"Verify {ideal.field_or_record} in {ideal.target_module}"
                if ideal.field_or_record and ideal.target_module
                else matched.suggested_new_test_title or f"Verify {ideal.description}"
            )
            manual_steps.append({
                "purpose": ideal.description,
                "suggested_step": (
                    f"In {ideal.target_module}, observe {ideal.field_or_record}: "
                    f"{ideal.expected_observation}"
                    if ideal.field_or_record else
                    f"Manual verification: {ideal.description}"
                ),
                "reason": reason,
                "execution_strategy": strategy_label,
                "verification_type": _verification_type_for_step(ideal, plan),
                "expected_change": ideal.expected_observation,
                "target_module": ideal.target_module,
                "observer_role": observer_role,
                "suggested_test_title": suggested_title,
            })
            needs_new_verification_test.append({
                "verification_type": _verification_type_for_step(ideal, plan),
                "execution_strategy": strategy_label,
                "target_module": ideal.target_module,
                "description": ideal.description,
                "expected_change": ideal.expected_observation,
                "observer_role": observer_role,
                "suggested_test_title": suggested_title,
            })
            coverage_gaps_reasons.append(reason)
            # Update pv_entry to reflect gap (not found) for the exporter.
            pv_entry["status"] = "not_found"
            pv_entry.pop("matched_test_id", None)
            pv_entry.pop("matched_test_title", None)
            pv_entry.pop("confidence", None)
            pv_entry.pop("execution_note", None)
            pv_entry["reason"] = reason
            if suggested_title:
                pv_entry["suggested_manual_step"] = suggested_title
            continue

        # Found or partial: emit execution step
        is_full = matched.status == "found"
        if is_full:
            found_count += 1
        else:
            partial_count += 1

        step_counter += 1
        note_prefix = "Record baseline" if phase == "pre_verify" else "Verify"
        note = (
            f"Run {matched.matched_test_id} and {note_prefix.lower()}: "
            f"{ideal.field_or_record} = {ideal.expected_observation}"
            if ideal.field_or_record else
            f"Run {matched.matched_test_id} to {note_prefix.lower()} {ideal.description}"
        )
        execution_order.append(ExecutionStep(
            step=step_counter,
            phase=phase,
            action="execute_test" if is_full else "execute_test_partial",
            test_id=matched.matched_test_id,
            test_title=matched.matched_test_title,
            purpose=ideal.description or f"{note_prefix}: {ideal.field_or_record}",
            note=note,
            confidence=matched.confidence,
            limitation=matched.grade_reason if not is_full else "",
        ))

    # Coverage across observation steps only.
    if observation_count == 0:
        coverage = "none"
    else:
        ratio = (found_count + 0.5 * partial_count) / observation_count
        if ratio >= 1.0:
            coverage = "full"
        elif ratio >= 0.5:
            coverage = "partial"
        elif ratio > 0:
            coverage = "minimal"
        else:
            coverage = "none"

    # Mutate the source TestCase for exporter compatibility.
    source_test.post_verifications = post_verifications_out
    source_test.needs_new_verification_test = needs_new_verification_test
    source_test.verification_coverage = coverage
    source_test.coverage_gaps = coverage_gaps_reasons

    notes = _generate_notes(
        source_test=source_test,
        execution_order=[s.to_dict() for s in execution_order],
        manual_steps=manual_steps,
        has_before_after=has_pre_verify,
        has_cross_user=has_session,
    )

    return ExecutionSequence(
        source_test_id=source_test.id,
        source_test_title=source_test.title,
        source_module=source_test.module_title,
        execution_order=[s.to_dict() for s in execution_order],
        manual_steps=manual_steps,
        verification_coverage=coverage,
        notes=notes,
        has_before_after=has_pre_verify,
        has_cross_user=has_session,
    )


def _verification_type_for_step(ideal: IdealPlanStep, plan: IdealExecutionPlan) -> str:
    """Best-effort: map a post/pre_verify step to one of the plan's declared
    verification_types. If the plan declared exactly one, use it. Otherwise
    leave blank — we can't tell which one corresponds to this step.
    """
    if len(plan.verification_types) == 1:
        return plan.verification_types[0]
    return ""


def _build_post_verification_entry(
    ideal: IdealPlanStep,
    matched: MatchedPlanStep,
    strategy: str,
    observer_role: str,
    has_session: bool,
) -> Dict:
    """Build an exporter-compatible post_verifications dict entry."""
    ideal_desc = ideal.description or (
        f"Observe {ideal.field_or_record} in {ideal.target_module}: {ideal.expected_observation}"
    )
    entry: Dict = {
        "ideal": ideal_desc,
        "status": "found" if matched.status == "found" else (
            "partial" if matched.status == "partial" else "not_found"
        ),
        "execution_strategy": strategy,
        "target_module": ideal.target_module,
    }
    if ideal.field_or_record:
        entry["field_or_record"] = ideal.field_or_record
    if ideal.expected_observation:
        entry["expected_change"] = ideal.expected_observation
    if ideal.spec_citation:
        entry["spec_citation"] = ideal.spec_citation
    if observer_role:
        entry["observer_role"] = observer_role
    if has_session:
        entry["requires_different_session"] = True
        if observer_role:
            entry["session_note"] = f"Log out and log in as {observer_role}"
    if matched.status in ("found", "partial") and matched.matched_test_id:
        entry["matched_test_id"] = matched.matched_test_id
        entry["matched_test_title"] = matched.matched_test_title
        entry["confidence"] = round(matched.confidence, 2)
        entry["execution_note"] = matched.grade_reason
    if matched.status in ("partial", "gap"):
        entry["reason"] = matched.grade_reason
    return entry


def _generate_notes(
    source_test: TestCase,
    execution_order: List[Dict],
    manual_steps: List[Dict],
    has_before_after: bool,
    has_cross_user: bool,
) -> str:
    if not execution_order and not manual_steps:
        return "No verification steps identified."

    parts: List[str] = []
    if has_before_after:
        pre_ids = [s.get("test_id") for s in execution_order if s.get("phase") == "pre_verify" and s.get("test_id")]
        post_ids = [s.get("test_id") for s in execution_order if s.get("phase") == "post_verify" and s.get("test_id")]
        if pre_ids:
            parts.append(f"PRE: Record baseline with {', '.join(pre_ids)}")
        parts.append(f"ACTION: Execute {source_test.id}")
        if post_ids:
            parts.append(f"POST: Verify with {', '.join(post_ids)} (compare against baseline)")
    else:
        post_ids = [s.get("test_id") for s in execution_order if s.get("phase") == "post_verify" and s.get("test_id")]
        parts.append(f"Execute {source_test.id}")
        if post_ids:
            parts.append(f"then verify with {', '.join(post_ids)}")

    if has_cross_user:
        parts.append("(cross-user: switch to observer role)")
    elif any(s.get("action") == "session_switch" for s in execution_order):
        parts.append("(requires user session switch)")

    if manual_steps:
        parts.append(f"Manual verification needed for {len(manual_steps)} item(s)")

    return " → ".join(parts)


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def generate_execution_plan_summary(
    execution_plans: Dict[str, ExecutionSequence]
) -> Dict:
    """Aggregate summary counters for the finalize node."""
    if not execution_plans:
        return {
            "total_plans": 0,
            "coverage_distribution": {},
            "total_automated_steps": 0,
            "total_manual_steps": 0,
            "automation_rate": 0,
            "before_after_plans": 0,
            "after_only_plans": 0,
            "cross_user_plans": 0,
        }

    coverage_dist = {"full": 0, "partial": 0, "minimal": 0, "none": 0}
    total_automated = 0
    total_manual = 0
    before_after_count = 0
    after_only_count = 0
    cross_user_count = 0

    for plan in execution_plans.values():
        coverage_dist[plan.verification_coverage] = (
            coverage_dist.get(plan.verification_coverage, 0) + 1
        )
        verify_steps = [
            s for s in plan.execution_order
            if s.get("phase") in ("pre_verify", "post_verify")
        ]
        total_automated += len(verify_steps)
        total_manual += len(plan.manual_steps)
        if plan.has_cross_user:
            cross_user_count += 1
        elif plan.has_before_after:
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
        "cross_user_plans": cross_user_count,
    }
