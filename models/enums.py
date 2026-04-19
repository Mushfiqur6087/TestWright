"""Enumerations for test case type and priority."""

from enum import Enum


class TestType(str, Enum):
    """Type of test case."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    EDGE_CASE = "edge_case"
    STANDARD = "standard"


class Priority(str, Enum):
    """Test case priority level."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
