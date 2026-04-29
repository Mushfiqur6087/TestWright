from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ============================================================================
# Parser Agent Output
# ============================================================================


@dataclass
class ParsedModule:
    """Output from ParserAgent representing a parsed page/module."""

    id: int
    title: str
    raw_description: str
    mentioned_items: List[str] = field(default_factory=list)
    workflows: List[str] = field(default_factory=list)
    business_rules: List[str] = field(default_factory=list)
    expected_behaviors: List[str] = field(default_factory=list)


@dataclass
class ParsedFunctionalDescription:
    """Complete parsed functional description."""

    project_name: str
    base_url: str
    navigation_overview: str
    modules: List[ParsedModule] = field(default_factory=list)


# ============================================================================
# Chunker Agent Output
# ============================================================================


@dataclass
class ProjectContext:
    """Lightweight project context passed to downstream agents."""

    project_name: str = ""
    navigation_overview: str = ""


@dataclass
class WorkflowChunk:
    """A chunk representing a single workflow within a module."""

    chunk_id: str
    module_id: int
    module_title: str
    workflow_name: str
    workflow_description: str
    related_items: List[str] = field(default_factory=list)
    related_rules: List[str] = field(default_factory=list)
    related_behaviors: List[str] = field(default_factory=list)
    sibling_workflows: List[str] = field(default_factory=list)
    project_context: Optional["ProjectContext"] = None


# ============================================================================
# Summary Agent Output
# ============================================================================


@dataclass
class ModuleSummary:
    """Summary data for a module."""

    module_id: int
    module_title: str
    summary: str

    def to_dict(self) -> dict:
        return {
            "module_id": self.module_id,
            "module_title": self.module_title,
            "summary": self.summary,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ModuleSummary":
        return cls(
            module_id=data["module_id"],
            module_title=data["module_title"],
            summary=data.get("summary", ""),
        )


# ============================================================================
# Navigation Agent Output
# ============================================================================


@dataclass
class NavigationNode:
    """A node in the navigation graph representing a page/module."""

    module_id: int
    title: str
    url_path: Optional[str] = None
    connected_to: List[int] = field(default_factory=list)
    test_case_ids: List[str] = field(default_factory=list)


@dataclass
class NavigationGraph:
    """Navigation graph of the website."""

    nodes: Dict[int, NavigationNode] = field(default_factory=dict)
    graph_image_path: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "graph_image_path": self.graph_image_path,
            "nodes": [
                {
                    "module_id": node.module_id,
                    "title": node.title,
                    "url_path": node.url_path,
                    "connected_to": node.connected_to,
                    "test_case_ids": node.test_case_ids,
                }
                for node in self.nodes.values()
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "NavigationGraph":
        nodes: Dict[int, NavigationNode] = {}
        for node_data in data.get("nodes", []):
            node = NavigationNode(
                module_id=node_data["module_id"],
                title=node_data["title"],
                url_path=node_data.get("url_path"),
                connected_to=node_data.get("connected_to", []),
                test_case_ids=node_data.get("test_case_ids", []),
            )
            nodes[node.module_id] = node

        return cls(
            nodes=nodes,
            graph_image_path=data.get("graph_image_path"),
        )


# ============================================================================
# Test Case Output
# ============================================================================


@dataclass
class TestCase:
    """A single test case."""

    id: str
    title: str
    module_id: int
    module_title: str
    workflow: str
    test_type: str
    priority: str
    preconditions: str
    steps: List[str] = field(default_factory=list)
    expected_result: str = ""
    spec_evidence: str = ""

    def to_dict(self) -> dict:
        result = {
            "id": self.id,
            "title": self.title,
            "module_id": self.module_id,
            "module_title": self.module_title,
            "workflow": self.workflow,
            "test_type": self.test_type,
            "priority": self.priority,
            "preconditions": self.preconditions,
            "steps": self.steps,
            "expected_result": self.expected_result,
        }
        if self.spec_evidence:
            result["spec_evidence"] = self.spec_evidence
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "TestCase":
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            module_id=data.get("module_id", 0),
            module_title=data.get("module_title", ""),
            workflow=data.get("workflow", ""),
            test_type=data.get("test_type", "positive"),
            priority=data.get("priority", "Medium"),
            preconditions=data.get("preconditions", ""),
            steps=data.get("steps", []),
            expected_result=data.get("expected_result", ""),
            spec_evidence=data.get("spec_evidence", ""),
        )


# ============================================================================
# Final Output
# ============================================================================


@dataclass
class TestSuiteOutput:
    """Final output containing navigation graph and test cases."""

    project_name: str
    base_url: str
    generated_at: str
    navigation_graph: NavigationGraph
    test_cases: List[TestCase] = field(default_factory=list)
    module_summaries: Dict[int, ModuleSummary] = field(default_factory=dict)
    summary: Dict = field(default_factory=dict)
    navigation_overview: str = ""

    def to_dict(self) -> dict:
        return {
            "project_name": self.project_name,
            "base_url": self.base_url,
            "generated_at": self.generated_at,
            "navigation_overview": self.navigation_overview,
            "navigation_graph": self.navigation_graph.to_dict(),
            "module_summaries": [summary.to_dict() for summary in self.module_summaries.values()],
            "test_cases": [test_case.to_dict() for test_case in self.test_cases],
            "summary": self.summary,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TestSuiteOutput":
        nav_graph = NavigationGraph.from_dict(data.get("navigation_graph", {}))
        test_cases = [TestCase.from_dict(test_case) for test_case in data.get("test_cases", [])]
        module_summaries = {
            summary["module_id"]: ModuleSummary.from_dict(summary)
            for summary in data.get("module_summaries", [])
        }
        return cls(
            project_name=data.get("project_name", ""),
            base_url=data.get("base_url", ""),
            generated_at=data.get("generated_at", ""),
            navigation_graph=nav_graph,
            test_cases=test_cases,
            module_summaries=module_summaries,
            summary=data.get("summary", {}),
            navigation_overview=data.get("navigation_overview", ""),
        )


# ============================================================================
# Verification Pipeline Output
# ============================================================================


@dataclass
class VerificationRecord:
    """A single verification record per verification_structure_spec.md §2."""

    test_case_id: str
    verification_type: str
    coverage: str
    body: Dict[str, Any] = field(default_factory=dict)
    coverage_note: Optional[str] = None

    def to_dict(self) -> dict:
        result: Dict[str, Any] = {
            "test_case_id": self.test_case_id,
            "verification_type": self.verification_type,
            "coverage": self.coverage,
        }
        if self.coverage_note:
            result["coverage_note"] = self.coverage_note
        result["body"] = self.body
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "VerificationRecord":
        return cls(
            test_case_id=data.get("test_case_id", ""),
            verification_type=data.get("verification_type", ""),
            coverage=data.get("coverage", ""),
            coverage_note=data.get("coverage_note"),
            body=data.get("body", {}),
        )


@dataclass
class VerificationSuiteOutput:
    """Top-level payload written to verifications.json."""

    project_name: str
    base_url: str
    generated_at: str
    source_test_cases_file: str
    source_spec_files: List[str] = field(default_factory=list)
    verifications: List[VerificationRecord] = field(default_factory=list)
    coverage_summary: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "project_name": self.project_name,
            "base_url": self.base_url,
            "generated_at": self.generated_at,
            "source_test_cases_file": self.source_test_cases_file,
            "source_spec_files": self.source_spec_files,
            "coverage_summary": self.coverage_summary,
            "verifications": [v.to_dict() for v in self.verifications],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "VerificationSuiteOutput":
        return cls(
            project_name=data.get("project_name", ""),
            base_url=data.get("base_url", ""),
            generated_at=data.get("generated_at", ""),
            source_test_cases_file=data.get("source_test_cases_file", ""),
            source_spec_files=data.get("source_spec_files", []),
            verifications=[VerificationRecord.from_dict(v) for v in data.get("verifications", [])],
            coverage_summary=data.get("coverage_summary", {}),
        )