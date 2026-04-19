from dataclasses import dataclass, field
from typing import List, Dict, Optional

from testwright.models.enums import VerificationStatus


# ============================================================================
# Parser Agent Output
# ============================================================================

@dataclass
class ParsedModule:
    """Output from ParserAgent - represents a parsed module/page"""
    id: int
    title: str
    raw_description: str
    mentioned_items: List[str] = field(default_factory=list)
    workflows: List[str] = field(default_factory=list)
    business_rules: List[str] = field(default_factory=list)
    expected_behaviors: List[str] = field(default_factory=list)
    requires_auth: bool = True


@dataclass
class ParsedFunctionalDescription:
    """Complete parsed functional description"""
    project_name: str
    base_url: str
    navigation_overview: str
    modules: List[ParsedModule] = field(default_factory=list)
    # Sentences describing behaviors the system does NOT have, or
    # sandbox/mock limitations. Used by plan_generator and verify_matcher
    # to prevent emitting / matching verifications the system cannot satisfy.
    system_constraints: List[str] = field(default_factory=list)


# ============================================================================
# Chunker Agent Output
# ============================================================================

@dataclass
class ProjectContext:
    """Lightweight domain/context info passed to downstream agents so they
    can produce domain-appropriate tests and verifications."""
    project_name: str = ""
    navigation_overview: str = ""


@dataclass
class WorkflowChunk:
    """A chunk representing a single workflow within a module"""
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
    """Summary of a module for verification matching"""
    module_id: int
    module_title: str
    summary: str
    verification_keywords: List[str] = field(default_factory=list)
    can_verify_states: List[str] = field(default_factory=list)
    action_states: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "module_id": self.module_id,
            "module_title": self.module_title,
            "summary": self.summary,
            "verification_keywords": self.verification_keywords,
            "can_verify_states": self.can_verify_states,
            "action_states": self.action_states
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ModuleSummary":
        return cls(
            module_id=d["module_id"],
            module_title=d["module_title"],
            summary=d.get("summary", ""),
            verification_keywords=d.get("verification_keywords", []),
            can_verify_states=d.get("can_verify_states", []),
            action_states=d.get("action_states", []),
        )


# ============================================================================
# Navigation Agent Output
# ============================================================================

@dataclass
class NavigationNode:
    """A node in the navigation graph representing a page/module"""
    module_id: int
    title: str
    requires_auth: bool
    url_path: Optional[str] = None
    connected_to: List[int] = field(default_factory=list)
    test_case_ids: List[str] = field(default_factory=list)


@dataclass
class NavigationGraph:
    """Navigation graph of the website"""
    nodes: Dict[int, NavigationNode] = field(default_factory=dict)
    login_module_id: Optional[int] = None
    graph_image_path: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to JSON-serializable dictionary"""
        return {
            "login_module_id": self.login_module_id,
            "graph_image_path": self.graph_image_path,
            "nodes": [
                {
                    "module_id": node.module_id,
                    "title": node.title,
                    "requires_auth": node.requires_auth,
                    "url_path": node.url_path,
                    "connected_to": node.connected_to,
                    "test_case_ids": node.test_case_ids
                }
                for node in self.nodes.values()
            ]
        }

    @classmethod
    def from_dict(cls, d: dict) -> "NavigationGraph":
        nodes = {}
        for n in d.get("nodes", []):
            node = NavigationNode(
                module_id=n["module_id"],
                title=n["title"],
                requires_auth=n.get("requires_auth", True),
                url_path=n.get("url_path"),
                connected_to=n.get("connected_to", []),
                test_case_ids=n.get("test_case_ids", []),
            )
            nodes[node.module_id] = node
        return cls(
            nodes=nodes,
            login_module_id=d.get("login_module_id"),
            graph_image_path=d.get("graph_image_path"),
        )


# ============================================================================
# Test Case Output
# ============================================================================

@dataclass
class TestCase:
    """A single test case"""
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

    # Post-verification fields (populated by verification pipeline)
    needs_post_verification: bool = False
    modifies_state: List[str] = field(default_factory=list)
    modification_kind: str = ""  # create | update | delete | status_transition | credential_change | none
    post_verifications: List[Dict] = field(default_factory=list)
    verification_coverage: str = ""
    coverage_gaps: List[str] = field(default_factory=list)
    # Structured records for ideal verifications with no found/partial match.
    # Each entry: {verification_type, execution_strategy, target_module,
    # description, expected_change, observer_role, suggested_test_title}
    needs_new_verification_test: List[Dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to JSON-serializable dictionary"""
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
            "expected_result": self.expected_result
        }

        if self.spec_evidence:
            result["spec_evidence"] = self.spec_evidence

        if self.needs_post_verification:
            result["needs_post_verification"] = self.needs_post_verification
            result["modifies_state"] = self.modifies_state
            if self.modification_kind:
                result["modification_kind"] = self.modification_kind
            result["post_verifications"] = self.post_verifications
            result["verification_coverage"] = self.verification_coverage
            if self.coverage_gaps:
                result["coverage_gaps"] = self.coverage_gaps
            if self.needs_new_verification_test:
                result["needs_new_verification_test"] = self.needs_new_verification_test

        return result

    @classmethod
    def from_dict(cls, d: dict) -> "TestCase":
        return cls(
            id=d.get("id", ""),
            title=d.get("title", ""),
            module_id=d.get("module_id", 0),
            module_title=d.get("module_title", ""),
            workflow=d.get("workflow", ""),
            test_type=d.get("test_type", "positive"),
            priority=d.get("priority", "Medium"),
            preconditions=d.get("preconditions", ""),
            steps=d.get("steps", []),
            expected_result=d.get("expected_result", ""),
            spec_evidence=d.get("spec_evidence", ""),
            needs_post_verification=d.get("needs_post_verification", False),
            modifies_state=d.get("modifies_state", []),
            modification_kind=d.get("modification_kind", ""),
            post_verifications=d.get("post_verifications", []),
            verification_coverage=d.get("verification_coverage", ""),
            coverage_gaps=d.get("coverage_gaps", []),
            needs_new_verification_test=d.get("needs_new_verification_test", []),
        )


# ============================================================================
# Ideal Execution Plan (Generated by PlanGeneratorAgent — Stage 2)
# ============================================================================

@dataclass
class IdealPlanStep:
    """A single step in an ideal post-verification plan.

    phase is one of:
      "pre_verify"     — observe a baseline BEFORE the action
      "navigate"       — move to a different module
      "session_switch" — log out and log in as a different role
      "action"         — execute the source state-changing test (exactly one per plan)
      "post_verify"    — observe the system AFTER the action to confirm the change
    """
    phase: str
    description: str = ""
    target_module: str = ""
    state_to_observe: str = ""
    field_or_record: str = ""
    expected_observation: str = ""
    observer_role: str = ""
    spec_citation: str = ""

    def to_dict(self) -> dict:
        result = {"phase": self.phase, "description": self.description}
        if self.target_module:
            result["target_module"] = self.target_module
        if self.state_to_observe:
            result["state_to_observe"] = self.state_to_observe
        if self.field_or_record:
            result["field_or_record"] = self.field_or_record
        if self.expected_observation:
            result["expected_observation"] = self.expected_observation
        if self.observer_role:
            result["observer_role"] = self.observer_role
        if self.spec_citation:
            result["spec_citation"] = self.spec_citation
        return result


@dataclass
class IdealExecutionPlan:
    """An ideal free-form plan that proves the source test's state change."""
    source_test_id: str
    verification_types: List[str] = field(default_factory=list)
    steps: List[IdealPlanStep] = field(default_factory=list)
    rationale: str = ""

    def to_dict(self) -> dict:
        return {
            "source_test_id": self.source_test_id,
            "verification_types": self.verification_types,
            "rationale": self.rationale,
            "steps": [s.to_dict() for s in self.steps],
        }


# ============================================================================
# Matched Plan Step (Output from VerificationMatcherAgent — Stage 3)
# ============================================================================

@dataclass
class MatchedPlanStep:
    """Stage 3's parallel grading record for one ideal step.

    status:
      "found"      — candidate fully serves this step
      "partial"    — candidate touches related data but not the exact field
      "gap"        — no candidate fits this step
      "procedural" — step is navigate/session_switch/action (no match needed)
    """
    ideal_step: IdealPlanStep
    status: str = "gap"
    matched_test_id: str = ""
    matched_test_title: str = ""
    confidence: float = 0.0
    grade_reason: str = ""
    suggested_new_test_title: str = ""


# ============================================================================
# Execution Sequence (Output from core/reporter.py — Stage 4)
# ============================================================================

@dataclass
class ExecutionStep:
    """A single step in an execution sequence produced by the reporter."""
    step: int
    phase: str                      # "pre_verify" | "navigate" | "session" | "action" | "post_verify"
    action: str                     # "execute_test" | "execute_test_partial" | "navigate" | "session_switch"
    test_id: str = ""
    test_title: str = ""
    purpose: str = ""
    note: str = ""
    confidence: float = 0.0
    limitation: str = ""

    def to_dict(self) -> dict:
        result = {"step": self.step, "phase": self.phase, "action": self.action}
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
    """Execution sequence for verifying a test case (Stage 4 output)."""
    source_test_id: str
    source_test_title: str
    source_module: str = ""
    execution_order: List[Dict] = field(default_factory=list)
    manual_steps: List[Dict] = field(default_factory=list)
    verification_coverage: str = ""
    notes: str = ""
    has_before_after: bool = False
    has_cross_user: bool = False

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
            "has_cross_user": self.has_cross_user,
        }


# ============================================================================
# Verification Match (Exporter-compatibility serialization shim)
# ============================================================================

@dataclass
class VerificationMatch:
    """Result of matching an ideal verification to actual test cases"""
    ideal_description: str
    status: str
    matched_test_id: str = ""
    matched_test_title: str = ""
    confidence: float = 0.0
    execution_note: str = ""
    reason: str = ""
    suggested_manual_step: str = ""
    execution_strategy: str = "after_only"
    verification_type: str = ""
    before_action: str = ""
    after_action: str = ""
    observer_role: str = ""
    requires_different_session: bool = False
    session_note: str = ""
    target_module: str = ""

    def to_dict(self) -> dict:
        result = {
            "ideal": self.ideal_description,
            "status": self.status,
            "execution_strategy": self.execution_strategy
        }
        if self.verification_type:
            result["verification_type"] = self.verification_type
        if self.target_module:
            result["target_module"] = self.target_module
        if self.status == "found" or self.status == "partial":
            result["matched_test_id"] = self.matched_test_id
            result["matched_test_title"] = self.matched_test_title
            result["confidence"] = round(self.confidence, 2)
            result["execution_note"] = self.execution_note
        if self.execution_strategy == "before_after":
            result["before_action"] = self.before_action
            result["after_action"] = self.after_action
        if self.execution_strategy == "cross_user" or self.observer_role:
            result["observer_role"] = self.observer_role
        if self.requires_different_session:
            result["requires_different_session"] = True
            result["session_note"] = self.session_note
        if self.status == "not_found" or self.status == "partial":
            result["reason"] = self.reason
            if self.suggested_manual_step:
                result["suggested_manual_step"] = self.suggested_manual_step
        return result


# ============================================================================
# Final Output
# ============================================================================

@dataclass
class TestSuiteOutput:
    """Final output containing navigation graph and test cases"""
    project_name: str
    base_url: str
    generated_at: str
    navigation_graph: NavigationGraph
    test_cases: List[TestCase] = field(default_factory=list)
    module_summaries: Dict[int, ModuleSummary] = field(default_factory=dict)
    execution_plans: Dict = field(default_factory=dict)
    summary: Dict = field(default_factory=dict)
    navigation_overview: str = ""

    def to_dict(self) -> dict:
        """Convert to JSON-serializable dictionary"""
        result = {
            "project_name": self.project_name,
            "base_url": self.base_url,
            "generated_at": self.generated_at,
            "navigation_overview": self.navigation_overview,
            "navigation_graph": self.navigation_graph.to_dict(),
            "module_summaries": [s.to_dict() for s in self.module_summaries.values()],
            "test_cases": [tc.to_dict() for tc in self.test_cases],
            "summary": self.summary
        }

        if self.execution_plans:
            result["execution_plans"] = {
                test_id: plan.to_dict() if hasattr(plan, 'to_dict') else plan
                for test_id, plan in self.execution_plans.items()
            }

        return result

    @classmethod
    def from_dict(cls, d: dict) -> "TestSuiteOutput":
        nav_graph = NavigationGraph.from_dict(d.get("navigation_graph", {}))
        test_cases = [TestCase.from_dict(tc) for tc in d.get("test_cases", [])]
        module_summaries = {
            s["module_id"]: ModuleSummary.from_dict(s)
            for s in d.get("module_summaries", [])
        }
        return cls(
            project_name=d.get("project_name", ""),
            base_url=d.get("base_url", ""),
            generated_at=d.get("generated_at", ""),
            navigation_graph=nav_graph,
            test_cases=test_cases,
            module_summaries=module_summaries,
            summary=d.get("summary", {}),
            navigation_overview=d.get("navigation_overview", ""),
        )
