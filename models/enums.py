"""Enumerations for test case types, priorities, and verification statuses."""

from enum import Enum


class TestType(str, Enum):
    """Type of test case."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    EDGE_CASE = "edge_case"


class Priority(str, Enum):
    """Test case priority level."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class VerificationStatus(str, Enum):
    """Status of a verification match."""
    FOUND = "found"
    NOT_FOUND = "not_found"
    PARTIAL = "partial"


class VerificationCoverage(str, Enum):
    """Coverage level of post-verification."""
    FULL = "full"
    PARTIAL = "partial"
    MINIMAL = "minimal"
    NONE = "none"


class ExecutionStrategy(str, Enum):
    """Execution strategy for verification."""
    BEFORE_AFTER = "before_after"
    AFTER_ONLY = "after_only"
