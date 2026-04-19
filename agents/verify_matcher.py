from typing import List, Dict, Optional, Set, Tuple

from testwright.agents.base import BaseAgent
from testwright.agents.rag_indexer import RAGIndexer
from testwright.models.schemas import (
    IdealVerification,
    ModuleSummary,
    ParsedModule,
    TestCase,
    VerificationMatch,
)


class VerificationMatcherAgent(BaseAgent):
    """Agent responsible for matching ideal verifications to actual test cases using RAG"""

    @property
    def name(self) -> str:
        return "Verification Matcher Agent"

    @property
    def system_prompt(self) -> str:
        return """You are an expert at matching verification requirements to test cases.

Given an ideal verification scenario and candidate test cases from RAG search,
determine if any of the candidates can serve as the verification test.

IMPORTANT — Execution Strategy Awareness:

When execution_strategy is "before_after":
  The verification test will be run TWICE — once BEFORE the action to record a baseline,
  and once AFTER to compare. Therefore, the test does NOT need to detect a "change" on its
  own. It only needs to OBSERVE/DISPLAY the relevant data. The comparison is handled by
  the execution plan.
  → Ask: "Does this test display or access the relevant data?"
  → A test that simply shows a value IS a full match for before_after verification.

When execution_strategy is "after_only":
  The test runs only after the action. It must be able to confirm the expected outcome
  by itself (e.g., a new record exists, a status changed to a specific value).
  → Ask: "Can this test confirm the expected result exists?"

When execution_strategy is "cross_user":
  The action is performed by one user; verification must be observed while logged in
  as a DIFFERENT role. The candidate qualifies if it operates on a module/view that
  the observer role can access AND it displays the relevant data.
  → Ask: "Can this test be run as the observer and reveal the change?"

Consider:
1. Does the test case operate on the right module/page?
2. Does it access/display the relevant data?
3. For before_after: can it observe the data? (sufficient for full match)
4. For after_only: can it confirm the expected outcome?
5. For cross_user: can it be run while logged in as the observer role?"""

    def run(
        self,
        flagged_tests: List[TestCase],
        ideal_verifications: Dict[str, List[IdealVerification]],
        all_test_cases: List[TestCase],
        module_summaries: Dict[int, ModuleSummary],
        use_embeddings: bool = True,
        module_descriptions: Optional[Dict[int, ParsedModule]] = None,
        system_constraints: Optional[List[str]] = None,
    ) -> List[TestCase]:
        """Match ideal verifications to actual test cases"""

        module_descriptions = module_descriptions or {}
        system_constraints = system_constraints or []

        # Build observer-only RAG index — excludes state-mutating tests and
        # NEGATIVE tests so similarity search returns only safe observers.
        observer_tests = [
            tc for tc in all_test_cases if self._is_observer_candidate(tc)
        ]
        print(f"  - Building observer RAG index ({len(observer_tests)} observers)...")
        observer_rag = RAGIndexer(use_embeddings=use_embeddings)
        observer_rag.build_index(observer_tests)

        # Full index is used only to surface "closest unsafe candidate" hints
        # in not_found reasons. Never promoted to an actual match.
        print(f"  - Building full RAG index ({len(all_test_cases)} tests)...")
        full_rag = RAGIndexer(use_embeddings=use_embeddings)
        full_rag.build_index(all_test_cases)

        # Lookups for module-level ranking and prompt grounding
        summaries_by_title = {
            ms.module_title: ms for ms in module_summaries.values()
        }
        modules_by_title = {
            m.title: m for m in module_descriptions.values()
        }

        for tc in flagged_tests:
            if not tc.needs_post_verification:
                continue

            test_id = tc.id
            if test_id not in ideal_verifications:
                continue

            ideals = ideal_verifications[test_id]
            if not ideals:
                tc.verification_coverage = "none"
                tc.coverage_gaps = ["No verification scenarios identified"]
                continue

            # Modules whose can_verify_states overlap with this test's
            # modifies_state — used for pass-3 targeted search.
            verifier_module_names = set()
            for ms in module_summaries.values():
                if any(s in ms.can_verify_states for s in tc.modifies_state):
                    verifier_module_names.add(ms.module_title)

            matches = []
            gap_records: List[Dict] = []
            for ideal in ideals:
                match = self._match_verification(
                    ideal=ideal,
                    observer_rag=observer_rag,
                    full_rag=full_rag,
                    source_test=tc,
                    verifier_module_names=verifier_module_names,
                    summaries_by_title=summaries_by_title,
                    modules_by_title=modules_by_title,
                    system_constraints=system_constraints,
                )
                matches.append(match.to_dict())

                if match.status == "not_found":
                    gap_records.append({
                        "verification_type": ideal.verification_type,
                        "execution_strategy": ideal.execution_strategy,
                        "target_module": ideal.target_module,
                        "description": ideal.description,
                        "expected_change": ideal.expected_change,
                        "observer_role": ideal.observer_role,
                        "suggested_test_title": (
                            match.suggested_manual_step
                            or f"Verify {ideal.expected_change}"
                        ),
                    })

            tc.post_verifications = matches
            tc.needs_new_verification_test = gap_records

            found_count = sum(1 for m in matches if m["status"] == "found")
            partial_count = sum(1 for m in matches if m["status"] == "partial")
            total = len(matches)

            if total == 0:
                tc.verification_coverage = "none"
            elif found_count == total:
                tc.verification_coverage = "full"
            elif found_count > 0 or partial_count > 0:
                tc.verification_coverage = "partial"
            else:
                tc.verification_coverage = "none"

            tc.coverage_gaps = [
                m.get("reason", "Unknown reason")
                for m in matches
                if m["status"] in ("not_found", "partial")
            ]

        return flagged_tests

    @staticmethod
    def _is_observer_candidate(tc: TestCase) -> bool:
        """A test is an observer-candidate (index-wide) if it does not mutate
        state and is not a NEGATIVE/error-path test. This is the universal
        filter for both the index and per-ideal matching."""
        if tc.needs_post_verification:
            return False
        if (tc.test_type or "").upper() == "NEGATIVE":
            return False
        return True

    def _is_observer_safe(self, candidate: TestCase, source: TestCase) -> bool:
        """Per-ideal observer-safety check. Also rejects the source test itself."""
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
        """Rank candidates using module-level observer/actor knowledge.

        Modules whose summary declares can_verify_states overlapping with
        the source's modifies_state get a boost. Modules whose action_states
        overlap get a penalty — they ACT on that state, they don't observe it.
        """
        summary = summaries_by_title.get(candidate.module_title)
        if not summary or not source_states:
            return similarity
        can_verify = set(summary.can_verify_states)
        acts_on = set(summary.action_states)
        boost = 0.3 if (can_verify & source_states) else 0.0
        penalty = 0.4 if (acts_on & source_states) else 0.0
        return similarity + boost - penalty

    def _match_verification(
        self,
        ideal: IdealVerification,
        observer_rag: RAGIndexer,
        full_rag: RAGIndexer,
        source_test: TestCase,
        verifier_module_names: Optional[Set[str]],
        summaries_by_title: Dict[str, ModuleSummary],
        modules_by_title: Dict[str, ParsedModule],
        system_constraints: List[str],
    ) -> VerificationMatch:
        """Match a single ideal verification to an observer-safe test case.

        Search runs against the observer-only index so unsafe candidates
        (state mutators, NEGATIVE tests) are excluded by construction.
        The full index is consulted only to craft a useful "closest unsafe
        candidate" hint when nothing observer-safe is found.
        """

        query = (
            f"{ideal.description} {ideal.verification_action} "
            f"{ideal.target_module} {ideal.expected_change}"
        )

        # --- Pass 1: module-filtered observer search ------------------------
        candidates: List[Tuple[TestCase, float]] = observer_rag.search(
            query=query,
            top_k=5,
            module_filter=ideal.target_module if ideal.target_module else None,
        )
        seen_ids = {tc.id for tc, _ in candidates}

        # --- Pass 2: cross-module observer search ---------------------------
        if len(candidates) < 3:
            for tc, score in observer_rag.search(query=query, top_k=5, module_filter=None):
                if tc.id not in seen_ids:
                    candidates.append((tc, score))
                    seen_ids.add(tc.id)

        # --- Pass 3: targeted search in verifier modules --------------------
        if verifier_module_names:
            for vmod in verifier_module_names:
                if ideal.target_module and vmod.lower() == ideal.target_module.lower():
                    continue
                for tc, score in observer_rag.search(query=query, top_k=3, module_filter=vmod):
                    if tc.id not in seen_ids:
                        candidates.append((tc, score))
                        seen_ids.add(tc.id)

        # Drop anything unsafe that somehow slipped through (self-match etc.)
        candidates = [
            (tc, s) for tc, s in candidates if self._is_observer_safe(tc, source_test)
        ]

        # Rank candidates using module-level observer/actor knowledge
        source_states = set(source_test.modifies_state)
        candidates.sort(
            key=lambda cs: -self._score_candidate(
                cs[0], cs[1], source_states, summaries_by_title
            )
        )

        if not candidates:
            # Craft a useful "not_found" reason by peeking at the full index
            # for the closest unsafe candidate — helps humans understand WHY.
            closest_hint = ""
            unsafe_hits = full_rag.search(
                query=query,
                top_k=3,
                module_filter=ideal.target_module if ideal.target_module else None,
            )
            for tc, _score in unsafe_hits:
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

            return VerificationMatch(
                ideal_description=ideal.description,
                status="not_found",
                reason=(
                    f"No observer-safe test cases found for module "
                    f"'{ideal.target_module}'.{closest_hint}"
                ),
                suggested_manual_step=(
                    f"Manual verification: {ideal.verification_action}. "
                    f"Expected: {ideal.expected_change}"
                ),
                execution_strategy=ideal.execution_strategy,
                verification_type=ideal.verification_type,
                before_action=ideal.before_action,
                after_action=ideal.after_action,
                observer_role=ideal.observer_role,
                requires_different_session=ideal.requires_different_session,
                session_note=ideal.session_note,
                target_module=ideal.target_module,
            )

        return self._validate_candidates(
            ideal=ideal,
            candidates=candidates[:3],
            source_test=source_test,
            summaries_by_title=summaries_by_title,
            modules_by_title=modules_by_title,
            system_constraints=system_constraints,
        )

    def _validate_candidates(
        self,
        ideal: IdealVerification,
        candidates: List[Tuple[TestCase, float]],
        source_test: TestCase,
        summaries_by_title: Dict[str, ModuleSummary],
        modules_by_title: Dict[str, ParsedModule],
        system_constraints: List[str],
    ) -> VerificationMatch:
        """Use LLM to validate whether candidates can verify the ideal."""

        # Full candidate context — no step/expected truncation so the LLM
        # can reason about what the test actually does.
        candidates_text = ""
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
            candidates_text += (
                f"\nTest ID: {tc.id}\n"
                f"Title: {tc.title}\n"
                f"Module: {tc.module_title}\n"
                f"Test Type: {tc.test_type}\n"
                f"Module can_verify_states: {can_verify}\n"
                f"Module action_states: {acts_on}\n"
                f"Steps:\n    {steps_text}\n"
                f"Expected: {tc.expected_result}\n"
                f"Similarity Score (after ranking): {score:.2f}\n"
                f"---\n"
            )

        # Source test context — matcher now knows what the source test does.
        source_mods = ", ".join(source_test.modifies_state) or "(none)"
        source_steps = "\n    ".join(f"- {s}" for s in source_test.steps) or "(none)"
        source_text = (
            f"Test ID: {source_test.id}\n"
            f"Title: {source_test.title}\n"
            f"Module: {source_test.module_title}\n"
            f"Modification kind: {source_test.modification_kind or 'unknown'}\n"
            f"Modifies state: {source_mods}\n"
            f"Steps:\n    {source_steps}\n"
            f"Expected: {source_test.expected_result}\n"
        )

        # Spec text for target and source modules
        target_mod = modules_by_title.get(ideal.target_module)
        source_mod = modules_by_title.get(source_test.module_title)

        def _module_spec_block(label: str, mod: Optional[ParsedModule]) -> str:
            if not mod:
                return ""
            behaviors = "\n    ".join(f"- {b}" for b in mod.expected_behaviors) or "(none)"
            rules = "\n    ".join(f"- {r}" for r in mod.business_rules) or "(none)"
            return (
                f"{label} ({mod.title}):\n"
                f"  Expected behaviors:\n    {behaviors}\n"
                f"  Business rules:\n    {rules}\n"
            )

        spec_blocks = []
        src_block = _module_spec_block("SOURCE MODULE", source_mod)
        if src_block:
            spec_blocks.append(src_block)
        if target_mod is not source_mod:
            tgt_block = _module_spec_block("TARGET MODULE", target_mod)
            if tgt_block:
                spec_blocks.append(tgt_block)
        spec_text = "\n".join(spec_blocks) if spec_blocks else ""

        constraints_block = ""
        if system_constraints:
            bullets = "\n".join(f"- {c}" for c in system_constraints)
            constraints_block = (
                "\nSYSTEM CONSTRAINTS (behaviors the system does NOT have):\n"
                f"{bullets}\n"
                "A candidate cannot verify a behavior listed here. If the\n"
                "verification itself contradicts a constraint, return not_found.\n"
            )

        # Strategy-aware instruction (same as before)
        if ideal.execution_strategy == "before_after":
            strategy_instruction = f"""EXECUTION STRATEGY: before_after
This verification test will be run TWICE:
  - BEFORE the action: {ideal.before_action or 'Record the relevant data'}
  - AFTER the action: {ideal.after_action or 'Compare and confirm the change'}

Therefore, the candidate test does NOT need to detect a "change" on its own.
It only needs to DISPLAY or ACCESS the relevant data so we can record it before
and compare it after. A test that shows the relevant value is a FULL MATCH ("found").

Do NOT mark a test as "partial" just because it "shows data but doesn't verify the change."
The before/after execution handles the change detection — the test just needs to observe the data."""
        elif ideal.execution_strategy == "cross_user":
            observer = ideal.observer_role or "a different user role"
            strategy_instruction = f"""EXECUTION STRATEGY: cross_user
The action is performed by one user; verification must be observed while logged
in as a DIFFERENT role: {observer}.

The candidate qualifies as a FULL match ("found") if it can plausibly be run
while logged in as {observer} AND it displays the relevant data. Prefer tests
in modules accessible to {observer}. Do NOT mark "partial" just because the
candidate doesn't itself perform a session switch — the execution plan handles
the logout/login as {observer}."""
        else:
            strategy_instruction = """EXECUTION STRATEGY: after_only
This verification test runs only AFTER the action. It must confirm the expected
outcome by itself (e.g., new record exists, status shows expected value)."""

        session_instruction = ""
        if ideal.requires_different_session:
            session_instruction = (
                f"\nSESSION NOTE: This verification requires a different user session.\n"
                f"{ideal.session_note}\n"
                f"Consider whether the candidate test can be run under a different user context."
            )

        prompt = f"""Determine if any of these test cases can verify the following requirement.

VERIFICATION NEEDED:
- Description: {ideal.description}
- Target Module: {ideal.target_module}
- Verification Action: {ideal.verification_action}
- Expected Change: {ideal.expected_change}
- State to Verify: {ideal.state_to_verify}

{strategy_instruction}
{session_instruction}

SOURCE TEST (the action whose effect we need to verify):
{source_text}

SPEC CONTEXT:
{spec_text}
{constraints_block}

CANDIDATE TEST CASES (pre-filtered to observer-safe tests only):
{candidates_text}

HARD MODULE RULE:
The required target module is "{ideal.target_module}". A candidate from a
different module can be marked "found" ONLY if that module's can_verify_states
overlaps with the source test's modifies_state. Otherwise mark "partial" (right
data, wrong module) or "not_found".

NEVER mark "found" for a candidate whose module action_states overlap with the
source's modifies_state — that candidate performs the same action under a
different name, it does not observe the result.

BEHAVIORAL VERIFICATION PREFERENCE:
A behavioral verification (testing the system's behavioral consequence of the
state change) is stronger than a UI-presence verification (a message or label).
Examples:
- A password change is best verified by attempting login with the old credentials
  (expect failure) and new credentials (expect success), NOT a "password updated" toast.
- A new account is best verified by reading the account listing or performing an
  action that requires the new account, NOT a "created successfully" message.
- A deletion is best verified by attempting to access the deleted record, NOT
  a "deleted" toast.
When multiple candidates qualify, PREFER the one that exercises a behavioral
consequence over one that checks a UI label.

Return JSON:
{{
    "best_match": {{
        "test_id": "TEST-ID or null if none match",
        "status": "found|partial|not_found",
        "confidence": 0.0 to 1.0,
        "execution_note": "How to use this test for verification",
        "reason": "Explanation if not_found or partial",
        "suggested_manual_step": "Manual step if no automated option exists"
    }}
}}

STATUS DEFINITIONS:
- found: Candidate can fully serve as the verification test.
- partial: Candidate is relevant but does not access the specific data required,
  or is in a module that does not clearly verify the target state.
- not_found: None of the candidates can verify this requirement, or the
  verification contradicts a system constraint."""

        try:
            result = self.call_llm_json(prompt, max_tokens=16000)
            match_data = result.get("best_match", {})

            status = match_data.get("status", "not_found")
            test_id = match_data.get("test_id")

            matched_title = ""
            matched_confidence = match_data.get("confidence", 0.0)
            if test_id and test_id != "null":
                for tc, score in candidates:
                    if tc.id == test_id:
                        matched_title = tc.title
                        if matched_confidence == 0:
                            matched_confidence = score
                        break

            return VerificationMatch(
                ideal_description=ideal.description,
                status=status,
                matched_test_id=test_id if test_id and test_id != "null" else "",
                matched_test_title=matched_title,
                confidence=matched_confidence,
                execution_note=match_data.get("execution_note", ""),
                reason=match_data.get("reason", ""),
                suggested_manual_step=match_data.get("suggested_manual_step", ""),
                execution_strategy=ideal.execution_strategy,
                verification_type=ideal.verification_type,
                before_action=ideal.before_action,
                after_action=ideal.after_action,
                observer_role=ideal.observer_role,
                requires_different_session=ideal.requires_different_session,
                session_note=ideal.session_note,
                target_module=ideal.target_module,
            )

        except Exception as e:
            print(f"Warning: Candidate validation failed: {e}")
            if candidates:
                best_tc, best_score = candidates[0]
                return VerificationMatch(
                    ideal_description=ideal.description,
                    status="partial" if best_score > 0.5 else "not_found",
                    matched_test_id=best_tc.id if best_score > 0.3 else "",
                    matched_test_title=best_tc.title if best_score > 0.3 else "",
                    confidence=best_score,
                    execution_note=f"Execute {best_tc.id} to verify",
                    reason="LLM validation failed, using similarity score",
                    execution_strategy=ideal.execution_strategy,
                    verification_type=ideal.verification_type,
                    before_action=ideal.before_action,
                    after_action=ideal.after_action,
                    observer_role=ideal.observer_role,
                    requires_different_session=ideal.requires_different_session,
                    session_note=ideal.session_note,
                    target_module=ideal.target_module,
                )

            return VerificationMatch(
                ideal_description=ideal.description,
                status="not_found",
                reason="No matching test cases found",
                execution_strategy=ideal.execution_strategy,
                verification_type=ideal.verification_type,
                before_action=ideal.before_action,
                after_action=ideal.after_action,
                observer_role=ideal.observer_role,
                requires_different_session=ideal.requires_different_session,
                session_note=ideal.session_note,
                target_module=ideal.target_module,
            )
