"""
AutoSpecTest - Automated test case generation from functional specifications
using multi-agent orchestration.
"""

__version__ = "3.0.0"

from autospectest.framework.orchestrator.generator import TestCaseGenerator
from autospectest.framework.schemas.schemas import TestSuiteOutput, TestCase, NavigationGraph

__all__ = ["TestCaseGenerator", "TestSuiteOutput", "TestCase", "NavigationGraph"]
