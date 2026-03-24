import json
import re
from typing import List, Dict, Optional
from datetime import datetime

from testwright.agents.base import BaseAgent
from testwright.models.schemas import (
    TestCase,
    TestSuiteOutput,
    NavigationGraph
)


class AssemblerAgent(BaseAgent):
    """Agent responsible for assembling and organizing all test cases into final output"""

    @property
    def name(self) -> str:
        return "Assembler Agent"

    @property
    def system_prompt(self) -> str:
        return """You are an expert at organizing and reviewing test suites.
Your task is to:
1. Remove duplicate test cases
2. Ensure proper ordering by module and priority
3. Validate test case completeness
4. Generate proper test case IDs"""

    def run(
        self,
        test_cases: List[TestCase],
        nav_graph: NavigationGraph,
        project_name: str,
        base_url: str
    ) -> TestSuiteOutput:
        """Assemble all test cases into final output with navigation graph"""

        # Remove duplicates
        unique_tests = self._remove_duplicates(test_cases)

        # Sort by module and priority
        sorted_tests = self._sort_tests(unique_tests)

        # Assign proper IDs (MODULE-001 format)
        sorted_tests = self._assign_ids(sorted_tests)

        # Link test cases to navigation nodes
        nav_graph = self._link_tests_to_nav(nav_graph, sorted_tests)

        # Generate summary
        summary = self._generate_summary(sorted_tests)

        # Create final output
        return TestSuiteOutput(
            project_name=project_name,
            base_url=base_url,
            generated_at=datetime.now().isoformat(),
            navigation_graph=nav_graph,
            test_cases=sorted_tests,
            summary=summary
        )

    def _remove_duplicates(self, test_cases: List[TestCase]) -> List[TestCase]:
        """Remove duplicate test cases based on title and steps"""

        # Pass 1: Exact dedup (title + first 3 steps)
        seen_exact = set()
        after_exact = []

        for tc in test_cases:
            steps_sig = tuple(s.lower().strip() for s in tc.steps[:3]) if tc.steps else ()
            signature = (
                tc.module_id,
                tc.title.lower().strip(),
                steps_sig
            )

            if signature not in seen_exact:
                seen_exact.add(signature)
                after_exact.append(tc)

        # Pass 2: Semantic dedup for negative/edge_case tests within same module.
        # Catches cross-workflow duplicates like "Amount empty (internal)" vs "Amount empty (external)".
        seen_normalized = set()
        unique = []

        for tc in after_exact:
            if tc.test_type in ("negative", "edge_case"):
                norm_title = self._normalize_title(tc.title)
                norm_sig = (tc.module_id, tc.test_type, norm_title)
                if norm_sig in seen_normalized:
                    continue
                seen_normalized.add(norm_sig)
            unique.append(tc)

        return unique

    def _normalize_title(self, title: str) -> str:
        """Normalize a test title for semantic dedup by stripping workflow qualifiers."""
        t = title.lower().strip()
        # Remove parenthetical suffixes: "(Internal Transfer)"
        t = re.sub(r'\s*\(.*?\)\s*', ' ', t)
        # Remove "- Workflow Name" suffixes
        t = re.sub(r'\s*-\s*\w[\w\s]*$', '', t)
        # Remove "for <workflow>" suffixes
        t = re.sub(r'\s+for\s+\w[\w\s]*$', '', t)
        # Remove "via <workflow>" suffixes
        t = re.sub(r'\s+via\s+\w[\w\s]*$', '', t)
        # Collapse whitespace
        t = re.sub(r'\s+', ' ', t).strip()
        return t

    def _sort_tests(self, test_cases: List[TestCase]) -> List[TestCase]:
        """Sort tests by module ID, priority, and test type"""

        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        type_order = {"positive": 0, "negative": 1, "edge_case": 2}

        return sorted(
            test_cases,
            key=lambda tc: (
                tc.module_id,
                priority_order.get(tc.priority, 1),
                type_order.get(tc.test_type, 0)
            )
        )

    def _assign_ids(self, test_cases: List[TestCase]) -> List[TestCase]:
        """Assign proper IDs in MODULE_ID.PREFIX-XXX format.

        Prepends the numeric module_id to guarantee uniqueness even when
        two modules produce the same text prefix.

        Example outputs:
            Module 10 "Assignment (Student View)"  → 10.ASV-001, 10.ASV-002
            Module 14 "Activities (Student View)"  → 14.ASV-001, 14.ASV-002
        """

        module_counters: Dict[int, int] = {}
        module_prefixes: Dict[int, str] = {}

        # --- Phase 1: generate raw prefixes for every module ----------------
        for tc in test_cases:
            if tc.module_id not in module_prefixes:
                module_prefixes[tc.module_id] = self._generate_prefix(tc.module_title)
                module_counters[tc.module_id] = 1

        # --- Phase 2: detect collisions and prepend module_id ---------------
        # Always prepend module_id so IDs are deterministic and collision-free.
        # Format: "{module_id}.{PREFIX}"  e.g. "10.ASV", "14.ASV"
        resolved_prefixes: Dict[int, str] = {}
        for mid, prefix in module_prefixes.items():
            resolved_prefixes[mid] = f"{mid}.{prefix}"

        # --- Phase 3: assign final IDs -------------------------------------
        for tc in test_cases:
            prefix = resolved_prefixes[tc.module_id]
            counter = module_counters[tc.module_id]
            tc.id = f"{prefix}-{counter:03d}"
            module_counters[tc.module_id] += 1

        return test_cases

    def _generate_prefix(self, module_title: str) -> str:
        """Generate a short prefix from module title dynamically.

        Examples:
            "Login"                             → "LOGIN"
            "My Courses"                        → "MYCOUR"
            "Assignment (Student View)"          → "ASV"
            "Activities (Student View)"          → "ASV"
            "Adding Activities (Teacher Only)"   → "AATO"
        """
        # Clean the title
        title = module_title.strip()
        if not title:
            return "TEST"

        # Remove common filler words for cleaner prefixes
        filler_words = {"the", "a", "an", "to", "for", "of", "and", "or", "with"}
        words = [w for w in title.split() if w.lower() not in filler_words]

        # If all words were filler, use original
        if not words:
            words = title.split()

        # Single word: use first 6 characters uppercase
        if len(words) == 1:
            return words[0].upper()[:6]

        # Two words: use first 3 chars of each word
        if len(words) == 2:
            prefix = words[0][:3].upper() + words[1][:3].upper()
            return prefix[:6]

        # Three or more words: use first letter of each (up to 6)
        prefix = "".join(w[0].upper() for w in words[:6])
        return prefix

    def _link_tests_to_nav(
        self,
        nav_graph: NavigationGraph,
        test_cases: List[TestCase]
    ) -> NavigationGraph:
        """Link test case IDs to their navigation nodes"""

        for tc in test_cases:
            if tc.module_id in nav_graph.nodes:
                if tc.id not in nav_graph.nodes[tc.module_id].test_case_ids:
                    nav_graph.nodes[tc.module_id].test_case_ids.append(tc.id)

        return nav_graph

    def _generate_summary(
        self,
        test_cases: List[TestCase]
    ) -> Dict:
        """Generate summary statistics"""

        summary = {
            "total_tests": len(test_cases),
            "by_type": {
                "positive": 0,
                "negative": 0,
                "edge_case": 0
            },
            "by_priority": {
                "High": 0,
                "Medium": 0,
                "Low": 0
            },
            "by_module": {}
        }

        for tc in test_cases:
            # Count by type
            if tc.test_type in summary["by_type"]:
                summary["by_type"][tc.test_type] += 1

            # Count by priority
            if tc.priority in summary["by_priority"]:
                summary["by_priority"][tc.priority] += 1

            # Count by module
            if tc.module_title not in summary["by_module"]:
                summary["by_module"][tc.module_title] = 0
            summary["by_module"][tc.module_title] += 1

        return summary

    def export_json(self, output: TestSuiteOutput, file_path: str) -> str:
        """Export final output to JSON file"""

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(output.to_dict(), f, indent=2, ensure_ascii=False)

        return file_path

    def validate(self, test_cases: List[TestCase]) -> List[str]:
        """Validate test cases for completeness"""

        issues = []

        for tc in test_cases:
            if not tc.title or tc.title.strip() == "":
                issues.append(f"{tc.id or 'Unknown'}: Missing title")

            if not tc.steps:
                issues.append(f"{tc.id or tc.title}: Missing test steps")

            if not tc.expected_result:
                issues.append(f"{tc.id or tc.title}: Missing expected result")

        return issues
