"""
Stage 3 — Honest Matcher / Grader.

Grades ideal plan steps against the existing test catalog using RAG
to shortlist candidates. Prefers "gap" over rationalization. Operates
per-step — no plan redesign, no template-driven prompts.
"""

from typing import Dict, List, Optional, Set, Tuple

from testwright.agents.base import BaseAgent
from testwright.agents.rag_indexer import RAGIndexer
from testwright.models.schemas import (
    IdealExecutionPlan,
    IdealPlanStep,
    MatchedPlanStep,
    ModuleSummary,
    ParsedModule,
    TestCase,
)


_OBSERVATION_PHASES = {"pre_verify", "post_verify"}
_PROCEDURAL_PHASES = {"navigate", "session_switch", "action"}


class VerificationMatcherAgent(BaseAgent):
    """Stage 3 of the post-verification pipeline.

    For each ideal plan step:
      - procedural steps (navigate, session_switch, action) → status="procedural"
      - observation steps (pre_verify, post_verify) → RAG shortlist + LLM grader
    """

    @property
    def name(self) -> str:
        return "Verification Matcher Agent"

    @property
    def system_prompt(self) -> str:
        return """You are a QA verification grader. You are given ONE specific step from an ideal post-
verification plan and up to THREE candidate test cases. Your job is to grade honestly
whether any candidate can serve as that step.

YOUR ONLY JOB IS GRADING. Do not redesign the step. Do not suggest alternative ways to
verify that ignore the step's requirements. If no candidate fits the step as written,
return "gap".

BE HONEST. "gap" is an acceptable, often correct answer. Gaps identify real holes in the
test suite — they are useful signals. Do not rationalize a match because "we don't want
gaps". A weak match reported as "found" is worse than a gap reported as "gap".

WHAT THE STEP CONTAINS:
  - phase: "pre_verify" or "post_verify"
  - description: what the tester should do
  - target_module: where the observation happens
  - state_to_observe: the state name from the module's can_verify_states
  - field_or_record: the EXACT field or record to observe
  - expected_observation: what should be true after this step (a baseline value for
    pre_verify, a post-change value/delta/presence/absence for post_verify)

HOW TO THINK ABOUT pre_verify STEPS:
  A pre_verify step will be run BEFORE the action to record a baseline. Elsewhere in the
  plan there is typically a matching post_verify step that will be run AFTER the action to
  compare. The candidate does NOT need to detect a change on its own — it only needs to
  DISPLAY or ACCESS the exact field/record the step names. A test that shows the relevant
  value IS a full match. Do not downgrade to "partial" just because the candidate doesn't
  itself assert on a change.

HOW TO THINK ABOUT post_verify STEPS:
  A post_verify step runs AFTER the action. The candidate must be able to access or assert
  on the exact field/record named by the step, such that running it would reveal the
  expected_observation. If the step pairs with a pre_verify on the same field (baseline/
  compare pattern), displaying the value is sufficient. If the step is standalone (e.g.,
  existence/absence/status), the candidate must actually confirm the expected observation.

IF the plan includes a session_switch step immediately before this step, the candidate
will be run under the observer_role named in that session_switch step. The candidate does
NOT need to itself switch sessions — that is procedural and handled elsewhere. Grade the
candidate on whether it can plausibly be run under that role AND whether it accesses the
field/record.

HARD RULES:

  1. HARD MODULE RULE. If the candidate is in a different module than the step's
     target_module, it may only be "found" if that module's can_verify_states overlaps the
     source test's modifies_state. Otherwise at most "partial" (right data, wrong module)
     or "gap".

  2. NEVER mark "found" for a candidate whose module's action_states overlap the source's
     modifies_state. That candidate performs the same action — it is an actor, not an
     observer. Return "gap" and explain.

  3. The candidate must access the specific field_or_record named by the step. "Opens the
     account page" does NOT equal "observes the balance column". If the candidate only
     navigates and does not display/assert on the required field, it is at best "partial".

  4. BEHAVIORAL > UI-PRESENCE. A candidate that checks a success toast is not a match for
     a step that observes persistent data.

  5. A step whose observation would contradict a SYSTEM CONSTRAINT is a gap — report "gap"
     with a grade_reason citing the constraint.

STATUS DEFINITIONS:

  found        Candidate fully serves this step. Observer-safe, in the right module (or in
               a module whose can_verify_states overlap), and accesses the exact field/
               record the step names.

  partial      Candidate is in the right module and touches related data, but does not
               access the specific field_or_record the step requires. Use partial sparingly
               — when in doubt between partial and gap, choose gap.

  gap          No candidate fits this step as written. Include a concrete
               suggested_new_test_title describing what the missing observer test should do.
"""

    # ------------------------------------------------------------------ run

    def run(
        self,
        ideal_plans: Dict[str, IdealExecutionPlan],
        all_test_cases: List[TestCase],
        module_summaries: Dict[int, ModuleSummary],
        use_embeddings: bool = True,
        module_descriptions: Optional[Dict[int, ParsedModule]] = None,
        system_constraints: Optional[List[str]] = None,
    ) -> Dict[str, List[MatchedPlanStep]]:
        """Grade every ideal plan step against the test catalog.

        Returns a mapping ``source_test_id -> List[MatchedPlanStep]`` where
        the matched steps list is 1:1 aligned with ``ideal_plans[id].steps``.
        """
        module_descriptions = module_descriptions or {}
        system_constraints = system_constraints or []

        if not ideal_plans:
            return {}

        # Observer-safe index: excludes state mutators + NEGATIVE tests.
        observer_tests = [tc for tc in all_test_cases if self._is_observer_candidate(tc)]
        print(f"  - Building observer RAG index ({len(observer_tests)} observers)...")
        observer_rag = RAGIndexer(use_embeddings=use_embeddings)
        observer_rag.build_index(observer_tests)

        # Full index is only used to surface "closest unsafe candidate" hints.
        print(f"  - Building full RAG index ({len(all_test_cases)} tests)...")
        full_rag = RAGIndexer(use_embeddings=use_embeddings)
        full_rag.build_index(all_test_cases)

        summaries_by_title = {ms.module_title: ms for ms in module_summaries.values()}
        modules_by_title = {m.title: m for m in module_descriptions.values()}
        tests_by_id = {tc.id: tc for tc in all_test_cases}

        matched_plans: Dict[str, List[MatchedPlanStep]] = {}

        for source_id, plan in ideal_plans.items():
            source_test = tests_by_id.get(source_id)
            if source_test is None:
                # Shouldn't happen — but be defensive.
                matched_plans[source_id] = [
                    MatchedPlanStep(ideal_step=step, status="procedural")
                    if step.phase in _PROCEDURAL_PHASES
                    else MatchedPlanStep(ideal_step=step, status="gap",
                                         grade_reason="Source test not found in catalog")
                    for step in plan.steps
                ]
                continue

            # Modules whose can_verify_states overlap this test's modifies_state.
            verifier_module_names: Set[str] = set()
            for ms in module_summaries.values():
                if any(s in ms.can_verify_states for s in source_test.modifies_state):
                    verifier_module_names.add(ms.module_title)

            matched_steps: List[MatchedPlanStep] = []
            prev_steps: List[IdealPlanStep] = []
            for step in plan.steps:
                if step.phase in _PROCEDURAL_PHASES:
                    matched_steps.append(MatchedPlanStep(
                        ideal_step=step, status="procedural"
                    ))
                    prev_steps.append(step)
                    continue

                if step.phase not in _OBSERVATION_PHASES:
                    # Unknown phase — treat as gap.
                    matched_steps.append(MatchedPlanStep(
                        ideal_step=step, status="gap",
                        grade_reason=f"Unknown phase: {step.phase}",
                    ))
                    prev_steps.append(step)
                    continue

                matched_steps.append(self._grade_step(
                    step=step,
                    prev_step=prev_steps[-1] if prev_steps else None,
                    source_test=source_test,
                    observer_rag=observer_rag,
                    full_rag=full_rag,
                    verifier_module_names=verifier_module_names,
                    summaries_by_title=summaries_by_title,
                    modules_by_title=modules_by_title,
                    system_constraints=system_constraints,
                ))
                prev_steps.append(step)

            matched_plans[source_id] = matched_steps

        return matched_plans

    # ------------------------------------------------------------------ candidate safety

    @staticmethod
    def _is_observer_candidate(tc: TestCase) -> bool:
        """A test is an observer-candidate if it does not mutate state and is
        not a NEGATIVE/error-path test."""
        if tc.needs_post_verification:
            return False
        if (tc.test_type or "").upper() == "NEGATIVE":
            return False
        return True

    def _is_observer_safe(self, candidate: TestCase, source: TestCase) -> bool:
        if candidate.id == source.id:
            return False
        return self._is_observer_candidate(candidate)

    def _score_candidate(
        self,
        candidate: TestCase,
        similarity: float,
        source_states: Set[str],
        summaries_by_title: Dict[str, ModuleSummary],
    ) -> float:
        """Boost modules that can verify the source's modifies_state; penalize
        modules that act on it."""
        summary = summaries_by_title.get(candidate.module_title)
        if not summary or not source_states:
            return similarity
        can_verify = set(summary.can_verify_states)
        acts_on = set(summary.action_states)
        boost = 0.3 if (can_verify & source_states) else 0.0
        penalty = 0.4 if (acts_on & source_states) else 0.0
        return similarity + boost - penalty

    # ------------------------------------------------------------------ per-step grading

    def _grade_step(
        self,
        step: IdealPlanStep,
        prev_step: Optional[IdealPlanStep],
        source_test: TestCase,
        observer_rag: RAGIndexer,
        full_rag: RAGIndexer,
        verifier_module_names: Set[str],
        summaries_by_title: Dict[str, ModuleSummary],
        modules_by_title: Dict[str, ParsedModule],
        system_constraints: List[str],
    ) -> MatchedPlanStep:
        query = (
            f"{step.description} {step.target_module} "
            f"{step.field_or_record} {step.expected_observation}"
        ).strip()

        candidates = self._shortlist_candidates(
            query=query,
            target_module=step.target_module,
            observer_rag=observer_rag,
            verifier_module_names=verifier_module_names,
            source_test=source_test,
            summaries_by_title=summaries_by_title,
        )

        if not candidates:
            return self._gap_from_empty(
                step=step,
                source_test=source_test,
                full_rag=full_rag,
                query=query,
            )

        return self._llm_grade(
            step=step,
            prev_step=prev_step,
            candidates=candidates[:3],
            source_test=source_test,
            summaries_by_title=summaries_by_title,
            modules_by_title=modules_by_title,
            system_constraints=system_constraints,
        )

    # ------------------------------------------------------------------ shortlist

    def _shortlist_candidates(
        self,
        query: str,
        target_module: str,
        observer_rag: RAGIndexer,
        verifier_module_names: Set[str],
        source_test: TestCase,
        summaries_by_title: Dict[str, ModuleSummary],
    ) -> List[Tuple[TestCase, float]]:
        # Pass 1: module-filtered observer search
        candidates: List[Tuple[TestCase, float]] = observer_rag.search(
            query=query,
            top_k=5,
            module_filter=target_module if target_module else None,
        )
        seen_ids = {tc.id for tc, _ in candidates}

        # Pass 2: cross-module observer search (if pass 1 thin)
        if len(candidates) < 3:
            for tc, score in observer_rag.search(query=query, top_k=5, module_filter=None):
                if tc.id not in seen_ids:
                    candidates.append((tc, score))
                    seen_ids.add(tc.id)

        # Pass 3: targeted search in verifier modules
        if verifier_module_names:
            for vmod in verifier_module_names:
                if target_module and vmod.lower() == target_module.lower():
                    continue
                for tc, score in observer_rag.search(query=query, top_k=3, module_filter=vmod):
                    if tc.id not in seen_ids:
                        candidates.append((tc, score))
                        seen_ids.add(tc.id)

        # Drop self-matches and any unsafe candidates that slipped through.
        candidates = [
            (tc, s) for tc, s in candidates if self._is_observer_safe(tc, source_test)
        ]

        # Rank.
        source_states = set(source_test.modifies_state)
        candidates.sort(
            key=lambda cs: -self._score_candidate(
                cs[0], cs[1], source_states, summaries_by_title,
            )
        )
        return candidates

    # ------------------------------------------------------------------ empty-case gap

    def _gap_from_empty(
        self,
        step: IdealPlanStep,
        source_test: TestCase,
        full_rag: RAGIndexer,
        query: str,
    ) -> MatchedPlanStep:
        closest_hint = ""
        for tc, _score in full_rag.search(
            query=query,
            top_k=3,
            module_filter=step.target_module if step.target_module else None,
        ):
            if tc.id == source_test.id:
                continue
            if self._is_observer_candidate(tc):
                continue
            reason_bits = []
            if tc.needs_post_verification:
                reason_bits.append("mutates state")
            if (tc.test_type or "").upper() == "NEGATIVE":
                reason_bits.append("NEGATIVE test")
            if reason_bits:
                closest_hint = (
                    f" Closest candidate {tc.id} skipped ({', '.join(reason_bits)})."
                )
                break

        return MatchedPlanStep(
            ideal_step=step,
            status="gap",
            grade_reason=(
                f"No observer-safe test cases found for module "
                f"'{step.target_module}' that access '{step.field_or_record}'."
                f"{closest_hint}"
            ),
            suggested_new_test_title=(
                f"Verify {step.field_or_record} in {step.target_module}"
                if step.field_or_record and step.target_module
                else f"Verify {step.description}"
            ),
        )

    # ------------------------------------------------------------------ LLM grading

    def _llm_grade(
        self,
        step: IdealPlanStep,
        prev_step: Optional[IdealPlanStep],
        candidates: List[Tuple[TestCase, float]],
        source_test: TestCase,
        summaries_by_title: Dict[str, ModuleSummary],
        modules_by_title: Dict[str, ParsedModule],
        system_constraints: List[str],
    ) -> MatchedPlanStep:
        candidates_text = self._format_candidates(candidates, summaries_by_title)
        source_text = self._format_source(source_test)
        neighbor_text = self._format_neighbor(prev_step)
        spec_text = self._format_specs(step, source_test, modules_by_title)
        constraints_text = self._format_constraints(system_constraints)
        step_text = self._format_step(step)

        prompt = f"""Grade whether any candidate test case serves the following plan step.

THE STEP:
{step_text}

SOURCE TEST (the state-changing action being verified):
{source_text}

NEIGHBOR CONTEXT (the step immediately before this one):
{neighbor_text}

{spec_text}{constraints_text}
CANDIDATES (pre-filtered observer-safe tests, up to 3):
{candidates_text}

Return JSON:
{{
  "status": "found" | "partial" | "gap",
  "matched_test_id": "ID or empty string",
  "confidence": 0.0 to 1.0,
  "grade_reason": "HONEST explanation. If found: what the candidate does that matches the step. If partial: what it does and what it misses. If gap: why no candidate works, referencing specific candidate shortcomings.",
  "suggested_new_test_title": "Only for gap. Concrete title for the missing test."
}}"""

        try:
            result = self.call_llm_json(prompt, max_tokens=4000)
        except Exception as e:
            print(f"Warning: Per-step grading failed: {e}")
            best_tc, best_score = candidates[0]
            return MatchedPlanStep(
                ideal_step=step,
                status="partial" if best_score > 0.5 else "gap",
                matched_test_id=best_tc.id if best_score > 0.3 else "",
                matched_test_title=best_tc.title if best_score > 0.3 else "",
                confidence=best_score,
                grade_reason="LLM grading failed; fell back to similarity score.",
            )

        status = result.get("status", "gap")
        if status not in ("found", "partial", "gap"):
            status = "gap"

        raw_id = result.get("matched_test_id") or ""
        test_id = raw_id if raw_id and raw_id.lower() != "null" else ""

        matched_title = ""
        confidence = float(result.get("confidence") or 0.0)
        if test_id:
            for tc, score in candidates:
                if tc.id == test_id:
                    matched_title = tc.title
                    if confidence == 0:
                        confidence = score
                    break

        return MatchedPlanStep(
            ideal_step=step,
            status=status,
            matched_test_id=test_id if status in ("found", "partial") else "",
            matched_test_title=matched_title if status in ("found", "partial") else "",
            confidence=confidence if status in ("found", "partial") else 0.0,
            grade_reason=result.get("grade_reason", ""),
            suggested_new_test_title=(
                result.get("suggested_new_test_title", "") if status == "gap" else ""
            ),
        )

    # ------------------------------------------------------------------ prompt helpers

    @staticmethod
    def _format_step(step: IdealPlanStep) -> str:
        return (
            f"  phase: {step.phase}\n"
            f"  description: {step.description}\n"
            f"  target_module: {step.target_module}\n"
            f"  state_to_observe: {step.state_to_observe}\n"
            f"  field_or_record: {step.field_or_record}\n"
            f"  expected_observation: {step.expected_observation}\n"
            f"  spec_citation: {step.spec_citation}"
        )

    @staticmethod
    def _format_source(source_test: TestCase) -> str:
        mods = ", ".join(source_test.modifies_state) or "(none)"
        return (
            f"  id: {source_test.id}\n"
            f"  title: {source_test.title}\n"
            f"  module: {source_test.module_title}\n"
            f"  modifies_state: {mods}\n"
            f"  modification_kind: {source_test.modification_kind or 'unknown'}"
        )

    @staticmethod
    def _format_neighbor(prev_step: Optional[IdealPlanStep]) -> str:
        if prev_step is None:
            return "  (this is the first step)"
        parts = [f"  phase: {prev_step.phase}"]
        if prev_step.observer_role:
            parts.append(f"  observer_role: {prev_step.observer_role}")
        if prev_step.target_module:
            parts.append(f"  target_module: {prev_step.target_module}")
        return "\n".join(parts)

    @staticmethod
    def _format_candidates(
        candidates: List[Tuple[TestCase, float]],
        summaries_by_title: Dict[str, ModuleSummary],
    ) -> str:
        if not candidates:
            return "(none)"
        parts = []
        for tc, score in candidates:
            summary = summaries_by_title.get(tc.module_title)
            can_verify = (
                ", ".join(summary.can_verify_states)
                if summary and summary.can_verify_states else "(none)"
            )
            acts_on = (
                ", ".join(summary.action_states)
                if summary and summary.action_states else "(none)"
            )
            steps_text = "\n    ".join(f"- {s}" for s in tc.steps) or "(none)"
            parts.append(
                f"Test ID: {tc.id}\n"
                f"Title: {tc.title}\n"
                f"Module: {tc.module_title}\n"
                f"Test Type: {tc.test_type}\n"
                f"Module can_verify_states: {can_verify}\n"
                f"Module action_states: {acts_on}\n"
                f"Steps:\n    {steps_text}\n"
                f"Expected: {tc.expected_result}\n"
                f"Similarity (after ranking): {score:.2f}\n"
                f"---"
            )
        return "\n".join(parts)

    @staticmethod
    def _format_specs(
        step: IdealPlanStep,
        source_test: TestCase,
        modules_by_title: Dict[str, ParsedModule],
    ) -> str:
        source_mod = modules_by_title.get(source_test.module_title)
        target_mod = modules_by_title.get(step.target_module)

        def _block(label: str, mod: Optional[ParsedModule]) -> str:
            if not mod:
                return ""
            behaviors = "\n    ".join(f"- {b}" for b in mod.expected_behaviors) or "(none)"
            rules = "\n    ".join(f"- {r}" for r in mod.business_rules) or "(none)"
            return (
                f"{label} ({mod.title}):\n"
                f"  Expected behaviors:\n    {behaviors}\n"
                f"  Business rules:\n    {rules}\n"
            )

        parts = []
        src = _block("SOURCE MODULE", source_mod)
        if src:
            parts.append(src)
        if target_mod is not None and target_mod is not source_mod:
            tgt = _block("TARGET MODULE", target_mod)
            if tgt:
                parts.append(tgt)
        if not parts:
            return ""
        return "SPEC CONTEXT:\n" + "\n".join(parts) + "\n"

    @staticmethod
    def _format_constraints(system_constraints: List[str]) -> str:
        if not system_constraints:
            return ""
        bullets = "\n".join(f"- {c}" for c in system_constraints)
        return (
            "SYSTEM CONSTRAINTS (behaviors the system does NOT have):\n"
            f"{bullets}\n\n"
        )
