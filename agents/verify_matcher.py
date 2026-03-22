from typing import List, Dict

from testwright.agents.base import BaseAgent
from testwright.agents.rag_indexer import RAGIndexer
from testwright.models.schemas import TestCase, ModuleSummary, IdealVerification, VerificationMatch


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

Consider:
1. Does the test case operate on the right module/page?
2. Does it access/display the relevant data?
3. For before_after: can it observe the data? (sufficient for full match)
4. For after_only: can it confirm the expected outcome?"""

    def run(
        self,
        flagged_tests: List[TestCase],
        ideal_verifications: Dict[str, List[IdealVerification]],
        all_test_cases: List[TestCase],
        module_summaries: Dict[int, ModuleSummary],
        use_embeddings: bool = True
    ) -> List[TestCase]:
        """Match ideal verifications to actual test cases

        Args:
            flagged_tests: Test cases that need verification
            ideal_verifications: Dict mapping test_id to list of IdealVerification
            all_test_cases: All generated test cases to search through
            module_summaries: Module summaries for context
            use_embeddings: Whether to use embedding-based RAG

        Returns:
            Updated test cases with post_verifications populated
        """

        # Build RAG index
        print("  - Building RAG index...")
        rag = RAGIndexer(use_embeddings=use_embeddings)
        rag.build_index(all_test_cases)

        # Process each flagged test
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

            # Build set of modules whose can_verify_states overlap with this
            # test's modifies_state — used for cross-module RAG boosting.
            verifier_module_names = set()
            for ms in module_summaries.values():
                if any(s in ms.can_verify_states for s in tc.modifies_state):
                    verifier_module_names.add(ms.module_title)

            # Match each ideal verification
            matches = []
            for ideal in ideals:
                match = self._match_verification(
                    ideal, rag, all_test_cases, tc.id, verifier_module_names,
                )
                matches.append(match.to_dict())

            # Store matches in test case
            tc.post_verifications = matches

            # Calculate coverage
            found_count = sum(1 for m in matches if m["status"] == "found")
            partial_count = sum(1 for m in matches if m["status"] == "partial")
            total = len(matches)

            if found_count == total:
                tc.verification_coverage = "full"
            elif found_count > 0 or partial_count > 0:
                tc.verification_coverage = "partial"
            else:
                tc.verification_coverage = "none"

            # Collect gaps
            tc.coverage_gaps = [
                m.get("reason", "Unknown reason")
                for m in matches
                if m["status"] in ("not_found", "partial")
            ]

        return flagged_tests

    def _match_verification(
        self,
        ideal: IdealVerification,
        rag: RAGIndexer,
        all_tests: List[TestCase],
        source_test_id: str,
        verifier_module_names: set = None,
    ) -> VerificationMatch:
        """Match a single ideal verification to test cases.

        Uses a TWO-PASS search strategy:
          Pass 1 — Module-filtered search (preferred, same-module matches).
          Pass 2 — Unfiltered search across ALL modules to catch cross-module
                   verifiers (e.g., grading in Submissions verified by Student
                   Grades view). Results from pass 2 are de-duped against pass 1.

        Additionally, if ``verifier_module_names`` is provided (modules whose
        ``can_verify_states`` overlap with the source test's ``modifies_state``),
        a targeted third pass searches those modules specifically.

        Example: Grading a submission (module "Assignment Submissions") can be
        verified by "Assignment (Student View)" which can_verify grade_display.
        Pass 1 finds only Submissions tests; Pass 2 / Pass 3 finds the Student
        View test that actually displays the grade.
        """

        # Build search query from ideal verification
        query = f"{ideal.description} {ideal.verification_action} {ideal.target_module} {ideal.expected_change}"

        # --- Pass 1: Module-filtered search (preferred) ---------------------
        candidates = rag.search(
            query=query,
            top_k=5,
            module_filter=ideal.target_module if ideal.target_module else None
        )

        # --- Pass 2: Unfiltered cross-module search -------------------------
        # Only triggered when pass 1 didn't find enough candidates.
        seen_ids = {tc.id for tc, _ in candidates}
        if len(candidates) < 3:
            all_candidates = rag.search(query=query, top_k=5, module_filter=None)
            for tc, score in all_candidates:
                if tc.id not in seen_ids:
                    candidates.append((tc, score))
                    seen_ids.add(tc.id)

        # --- Pass 3: Targeted search in verifier modules --------------------
        # If module_summaries told us specific modules can verify the relevant
        # state, search those modules explicitly so we don't miss them.
        if verifier_module_names:
            for vmod in verifier_module_names:
                if ideal.target_module and vmod.lower() == ideal.target_module.lower():
                    continue  # Already covered by pass 1
                vmod_candidates = rag.search(query=query, top_k=3, module_filter=vmod)
                for tc, score in vmod_candidates:
                    if tc.id not in seen_ids:
                        candidates.append((tc, score))
                        seen_ids.add(tc.id)

        # Filter out the source test case itself
        candidates = [(tc, score) for tc, score in candidates if tc.id != source_test_id]

        if not candidates:
            return VerificationMatch(
                ideal_description=ideal.description,
                status="not_found",
                reason=f"No test cases found for module '{ideal.target_module}'",
                suggested_manual_step=f"Manual verification: {ideal.verification_action}. Expected: {ideal.expected_change}",
                execution_strategy=ideal.execution_strategy,
                before_action=ideal.before_action,
                after_action=ideal.after_action,
                requires_different_session=ideal.requires_different_session,
                session_note=ideal.session_note,
            )

        # Use LLM to validate the best candidates
        return self._validate_candidates(ideal, candidates[:3])

    def _validate_candidates(
        self,
        ideal: IdealVerification,
        candidates: List[tuple]
    ) -> VerificationMatch:
        """Use LLM to validate if candidates can verify the ideal scenario"""

        candidates_text = ""
        for tc, score in candidates:
            candidates_text += f"""
Test ID: {tc.id}
Title: {tc.title}
Module: {tc.module_title}
Steps: {'; '.join(tc.steps[:4])}
Expected: {tc.expected_result[:150]}
Similarity Score: {score:.2f}
---
"""

        # Build strategy-aware prompt
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
        else:
            strategy_instruction = """EXECUTION STRATEGY: after_only
This verification test runs only AFTER the action. It must confirm the expected
outcome by itself (e.g., new record exists, status shows expected value)."""

        session_instruction = ""
        if ideal.requires_different_session:
            session_instruction = f"""
SESSION NOTE: This verification requires a different user session.
{ideal.session_note}
Consider whether the candidate test can be run under a different user context."""

        prompt = f"""Determine if any of these test cases can verify the following requirement:

VERIFICATION NEEDED:
- Description: {ideal.description}
- Target Module: {ideal.target_module}
- Verification Action: {ideal.verification_action}
- Expected Change: {ideal.expected_change}
- State to Verify: {ideal.state_to_verify}

{strategy_instruction}
{session_instruction}

CANDIDATE TEST CASES:
{candidates_text}

Analyze each candidate and determine:
1. Does it operate on the correct module/page?
2. Does it access or display the relevant data?
3. For before_after strategy: Can it OBSERVE the data? (If yes → status should be "found")
4. For after_only strategy: Can it CONFIRM the expected outcome?

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
- found: Test case can fully serve as the verification test
  (for before_after: it can observe/display the relevant data)
  (for after_only: it can confirm the expected outcome)
- partial: Test case is on the right module but doesn't access the specific data needed
- not_found: None of the candidates can verify this requirement"""

        try:
            result = self.call_llm_json(prompt, max_tokens=1000)
            match_data = result.get("best_match", {})

            status = match_data.get("status", "not_found")
            test_id = match_data.get("test_id")

            # Find the matched test case for its title
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
                before_action=ideal.before_action,
                after_action=ideal.after_action,
                requires_different_session=ideal.requires_different_session,
                session_note=ideal.session_note,
            )

        except Exception as e:
            print(f"Warning: Candidate validation failed: {e}")
            # Fallback: use best candidate by score
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
                    before_action=ideal.before_action,
                    after_action=ideal.after_action,
                    requires_different_session=ideal.requires_different_session,
                    session_note=ideal.session_note,
                )

            return VerificationMatch(
                ideal_description=ideal.description,
                status="not_found",
                reason="No matching test cases found",
                execution_strategy=ideal.execution_strategy,
                before_action=ideal.before_action,
                after_action=ideal.after_action,
                requires_different_session=ideal.requires_different_session,
                session_note=ideal.session_note,
            )
