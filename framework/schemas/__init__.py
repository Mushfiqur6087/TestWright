"""Typed dataclasses, TypedDicts, and enums shared across the framework."""

from autospectest.framework.schemas.schemas import (
    ParsedModule,
    ParsedFunctionalDescription,
    WorkflowChunk,
    ModuleSummary,
    NavigationNode,
    NavigationGraph,
    TestCase,
    ProjectContext,
    TestSuiteOutput,
)
from autospectest.framework.schemas.enums import (
    TestType,
    Priority,
)

__all__ = [
    "ParsedModule",
    "ParsedFunctionalDescription",
    "WorkflowChunk",
    "ModuleSummary",
    "NavigationNode",
    "NavigationGraph",
    "TestCase",
    "ProjectContext",
    "TestSuiteOutput",
    "TestType",
    "Priority",
]
