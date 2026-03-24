from typing import List

from testwright.agents.base import BaseAgent
from testwright.models.schemas import WorkflowChunk, TestCase


class TestGenerationAgent(BaseAgent):
    """Agent responsible for generating test cases from workflow chunks"""

    @property
    def name(self) -> str:
        return "Test Generation Agent"

    @property
    def system_prompt(self) -> str:
        return """You are an expert QA engineer specializing in test case design for web automation.

Your task is to generate comprehensive test cases that cover the functionality described.

GUIDING PRINCIPLES:
1. Cover all scenarios mentioned in the functional description
2. Tests must be executable by a browser automation tool
3. Test steps should describe actions on the current page - NOT navigation to the page
4. Generate GRANULAR tests - one test per scenario, not combined tests

TEST TYPES:
1. POSITIVE TESTS: Verify success scenarios work as described
2. NEGATIVE TESTS: Test error conditions and validation rules mentioned
3. EDGE CASE TESTS: Boundary values, special characters, format variations if relevant

CRITICAL - NEGATIVE TEST GENERATION RULES:
1. For forms with multiple required fields, generate SEPARATE test cases for EACH field being empty
   - Example: If form has 5 required fields, generate 5 separate "X field empty" test cases
   - Do NOT combine into single "all fields empty" or "some fields empty" tests
2. For invalid format, generate ONE test per field (e.g., one "Invalid email format" test) — do NOT split into sub-variants like missing @, missing domain, multiple @ signs, etc.
3. For each validation rule mentioned in the spec, create a dedicated test case
4. Test each mismatch scenario separately (e.g., password mismatch, account number mismatch)
5. Test insufficient funds/resources scenarios if applicable

CRITICAL - POSITIVE TEST GENERATION RULES:
1. If multiple valid input types are mentioned (e.g., "username OR email"), create separate tests for EACH
2. If multiple account types or categories exist, create ONE positive test using any valid type, PLUS one test for a different type ONLY if the spec describes different behavior for it
3. Include state verification tests - verify changes are reflected after actions
4. Test pre-populated/display scenarios (e.g., "fields pre-filled with user data")

CRITICAL - BOUNDARY TEST RULES:
1. For monetary values: test exact boundary (e.g., exactly $100), just below boundary ($99.99)
2. For text fields: test maximum length ONLY if the spec explicitly states a character limit — do NOT invent length constraints
3. For date fields: test same start/end date, future dates if applicable

DO NOT generate tests for:
- Device-specific interactions (touch gestures, mobile-only features)
- Browser-specific features (right-click context menus, opening in new tabs)
- Network conditions (offline, slow connection, server errors)
- Stress scenarios (rapid clicking, load testing)
- Invented negative display tests (e.g., "table not displayed", "logo missing") — only test error conditions explicitly described in the spec

For each test case, provide:
- Clear, concise title
- Single precondition statement (or "None")
- Specific test steps (actions on the page, NOT navigation to the page)
- Single expected result
- Priority (High for core functionality, Medium for validations, Low for edge cases)"""

    def run(self, chunk: WorkflowChunk) -> List[TestCase]:
        """Generate test cases for a workflow chunk"""

        # Build context from chunk
        items_str = ", ".join(chunk.related_items) if chunk.related_items else "Not specified"
        rules_str = "\n".join([f"  - {r}" for r in chunk.related_rules]) if chunk.related_rules else "None"
        behaviors_str = "\n".join([f"  - {b}" for b in chunk.related_behaviors]) if chunk.related_behaviors else "None"

        # Build cross-workflow dedup context if sibling workflows exist
        sibling_str = ""
        if chunk.sibling_workflows:
            sibling_str = f"""
CROSS-WORKFLOW DEDUP RULE:
This module has sibling workflows: {', '.join(chunk.sibling_workflows)}.
For fields shared across workflows, generate field-empty and field-invalid tests ONLY ONCE — do not repeat them for each workflow.
Only generate validation tests for fields UNIQUE to this workflow: '{chunk.workflow_name}'.
"""

        prompt = f"""Generate test cases for this workflow.

Module: {chunk.module_title}
Workflow: {chunk.workflow_name}
Description: {chunk.workflow_description}

Available Items/Elements: {items_str}

Business Rules:
{rules_str}

Expected Behaviors:
{behaviors_str}
{sibling_str}
Generate test cases in this JSON format:
{{
    "test_cases": [
        {{
            "title": "Short descriptive title",
            "test_type": "positive|negative|edge_case",
            "priority": "High|Medium|Low",
            "preconditions": "Single precondition statement or None",
            "steps": ["Step 1", "Step 2", "Step 3"],
            "expected_result": "Single expected outcome"
        }}
    ]
}}

REQUIREMENTS:
1. Steps should describe actions on THIS page only - do NOT include navigation steps like "Navigate to login page"
2. Tests must be executable by browser automation
3. DO NOT use specific values - use generic descriptive text instead

CRITICAL - GRANULARITY RULES:

1. POSITIVE TESTS - Cover all input variations:
   - If description mentions "username OR email", generate SEPARATE tests for each
   - If multiple valid paths exist (e.g., Checking vs Savings account), test the PRIMARY path. Add a separate test for an alternative ONLY if the spec describes different behavior or different fields for that path
   - Include a test for form/page elements displayed correctly (if form fields are mentioned)
   - Include state verification tests (e.g., "Balance updated after transfer", "New account visible in overview")

2. NEGATIVE TESTS - Per-field validation (MANDATORY):
   - If the workflow has N required fields, generate N SEPARATE test cases (one for each field empty)
   - Example for a form with First Name, Last Name, Email, Password:
     * Test 1: "First Name field empty"
     * Test 2: "Last Name field empty"
     * Test 3: "Email field empty"
     * Test 4: "Password field empty"
   - Do NOT generate combined tests like: "Some fields empty" or "Required fields validation"
   - For invalid format, generate ONE test per field type (e.g., one "Invalid email format") — NOT multiple sub-variants
   - Test mismatch scenarios separately (password mismatch, account number mismatch)
   - Test insufficient funds/invalid credentials as separate cases
   - Test duplicate/existing data scenarios (e.g., "duplicate username")

3. EDGE CASE/BOUNDARY TESTS (generate when applicable):
   - Exact boundary values (e.g., exactly $100 minimum balance)
   - Just below boundary (e.g., $99.99)
   - Maximum/minimum field lengths ONLY if a specific limit is stated in the spec
   - Same start and end date for date ranges
   - Future dates if date input exists

IMPORTANT:
- Do not generate tests for touch gestures, right-click menus, network failures, or rapid clicking
- Use generic descriptive text for values, NOT specific data:
  CORRECT: "Enter a valid username", "Enter valid first name", "Enter valid email address"
  WRONG: "Enter 'John'", "Enter 'john@example.com'", "Enter '123 Main St'"
- Keep test steps natural and descriptive without hardcoded values

COVERAGE CHECKLIST (ensure all applicable items are covered):
Primary success scenario
All valid input variations (separate tests)
Each required field empty (separate tests)
Each validation rule violation
Mismatch scenarios (password, account numbers)
Boundary values ONLY for explicitly specified limits
State change verification (if action modifies data)
"""

        try:
            result = self.call_llm_json(prompt, max_tokens=16000)
            return self._parse_test_results(result, chunk)
        except Exception as e:
            print(f"Warning: Test generation failed for {chunk.workflow_name}: {e}")
            return []

    def _parse_test_results(self, result: dict, chunk: WorkflowChunk) -> List[TestCase]:
        """Parse LLM response into TestCase objects"""

        tests = []
        raw_tests = result.get("test_cases", [])

        for i, raw_test in enumerate(raw_tests):
            # Validate and normalize test_type
            test_type = raw_test.get("test_type", "positive").lower()
            if test_type not in ["positive", "negative", "edge_case"]:
                test_type = "positive"

            # Validate and normalize priority
            priority = raw_test.get("priority", "Medium")
            if priority not in ["High", "Medium", "Low"]:
                priority = "Medium"

            # Normalize preconditions
            preconditions = raw_test.get("preconditions", "None")
            if not preconditions or preconditions.lower() in ["none", "n/a", ""]:
                preconditions = "None"

            # Normalize expected_result
            expected = raw_test.get("expected_result", "")
            if isinstance(expected, list):
                expected = "; ".join(expected)

            test_case = TestCase(
                id="",  # Will be assigned by AssemblerAgent
                title=raw_test.get("title", f"Test Case {i+1}"),
                module_id=chunk.module_id,
                module_title=chunk.module_title,
                workflow=chunk.workflow_name,
                test_type=test_type,
                priority=priority,
                preconditions=preconditions,
                steps=raw_test.get("steps", []),
                expected_result=expected
            )
            tests.append(test_case)

        return tests

    def generate_for_type(
        self,
        chunk: WorkflowChunk,
        test_type: str
    ) -> List[TestCase]:
        """Generate only a specific type of test cases"""

        type_prompts = {
            "positive": "Generate positive (happy path) test cases. Cover all success scenarios mentioned in the description.",
            "negative": "Generate negative test cases for error conditions and validations mentioned in the description.",
            "edge_case": "Generate edge case tests for boundary values, special characters, or format variations if relevant."
        }

        items_str = ", ".join(chunk.related_items) if chunk.related_items else "Not specified"
        rules_str = "\n".join([f"  - {r}" for r in chunk.related_rules]) if chunk.related_rules else "None"

        prompt = f"""{type_prompts.get(test_type, type_prompts["positive"])}

Module: {chunk.module_title}
Workflow: {chunk.workflow_name}
Description: {chunk.workflow_description}

Available Items: {items_str}

Business Rules:
{rules_str}

Return JSON with test_cases array.
Steps should NOT include navigation - only actions on the current page.
Tests must be executable by browser automation (no touch gestures, right-click menus, network tests).
"""

        try:
            result = self.call_llm_json(prompt, max_tokens=16000)
            tests = self._parse_test_results(result, chunk)
            # Ensure all tests have correct type
            for test in tests:
                test.test_type = test_type
            return tests
        except Exception as e:
            print(f"Warning: {test_type} test generation failed: {e}")
            return []
