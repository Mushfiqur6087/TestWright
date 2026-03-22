from typing import Dict, Any

from testwright.agents.base import BaseAgent
from testwright.models.schemas import (
    ParsedModule,
    ParsedFunctionalDescription
)


class ParserAgent(BaseAgent):
    """Agent responsible for parsing functional description JSON"""

    @property
    def name(self) -> str:
        return "Parser Agent"

    @property
    def system_prompt(self) -> str:
        return """You are an expert software test analyst specializing in parsing functional descriptions for test case generation.

CRITICAL RULES:
1. Extract ONLY what is explicitly mentioned in the functional description
2. DO NOT infer, assume, or add information not present in the text
3. DO NOT specify UI element types (button/input/dropdown) - just extract names as written
4. Use the EXACT wording from the description whenever possible

Your task is to analyze functional descriptions and extract:

1. Mentioned Items: Fields, buttons, links, and interactive elements mentioned
2. Workflows: User actions that involve form submission or data processing on THIS page
   - A workflow is an action that COMPLETES on this page (e.g., "Login with credentials")
   - Navigation links to OTHER pages are NOT workflows for this page
3. Business Rules: Validation rules, constraints, and business logic stated
4. Expected Behaviors: What happens on success or failure
5. Authentication: Whether the page requires user to be logged in

WORKFLOW GUIDANCE:
- Focus on actions that complete on THIS page with a testable outcome
- Links to other pages (Register, Forgot Password) are navigation elements, not workflows
- If a page has multiple forms, each form's submission is a separate workflow"""

    def run(self, functional_desc: Dict[str, Any]) -> ParsedFunctionalDescription:
        """Parse the functional description JSON and extract structured data"""

        # Validate basic structure
        if not isinstance(functional_desc, dict):
            raise ValueError("Functional description must be a dictionary")

        project_name = functional_desc.get("project_name", "Unknown Project")
        base_url = functional_desc.get("website_url", "")
        navigation_overview = functional_desc.get("navigation_overview", "")
        raw_modules = functional_desc.get("modules", [])

        parsed_modules = []
        for module in raw_modules:
            parsed_module = self._parse_module(module)
            parsed_modules.append(parsed_module)

        return ParsedFunctionalDescription(
            project_name=project_name,
            base_url=base_url,
            navigation_overview=navigation_overview,
            modules=parsed_modules
        )

    def _parse_module(self, module: Dict[str, Any]) -> ParsedModule:
        """Parse a single module using LLM to extract details"""

        module_id = module.get("id", 0)
        title = module.get("title", "Unknown Module")
        description = module.get("description", "")

        # Use LLM to extract structured information from description
        extraction_prompt = f"""Analyze this functional description and extract information for test case generation.

Module Title: {title}
Description: {description}

IMPORTANT: Extract ONLY what is explicitly mentioned. Do NOT add assumptions or infer details not present.

Return a JSON object with these fields:
{{
    "mentioned_items": ["Item1", "Item2", ...],
    "workflows": ["Workflow1", ...],
    "business_rules": ["Rule1", "Rule2", ...],
    "expected_behaviors": ["Behavior1", "Behavior2", ...],
    "requires_auth": true/false
}}

Field Descriptions:

- mentioned_items: Extract ALL individual form fields, buttons, and interactive elements as SEPARATE items.
  * List EACH field separately (not grouped as "form fields")
  * Mark required fields with "(required)" suffix
  * Include buttons, links, dropdowns, and other interactive elements
  * Example: ["First Name (required)", "Last Name (required)", "Email (required)", "Phone", "Submit button", "Cancel link"]

- workflows: PRIMARY actions that COMPLETE on this page with a testable outcome.
  * A workflow involves form submission or data processing
  * Navigation links to other pages are NOT workflows
  * Most pages have only 1-2 primary workflows
  * Example for login page: ["Login with credentials"] (NOT "Navigate to register")

- business_rules: Extract ALL validation rules and constraints.
  * Include required field rules (e.g., "First Name is required")
  * Include format validations (e.g., "Email must be valid format")
  * Include matching field rules (e.g., "Password and Confirm Password must match")
  * Include business constraints (e.g., "Minimum balance $100 required")
  * Include uniqueness rules (e.g., "Username must be unique")

- expected_behaviors: Success/failure outcomes explicitly mentioned
  * Include success messages/redirects
  * Include error message behaviors
  * Include state changes (e.g., "Balance is deducted", "New account appears in list")

- requires_auth: false for login/register/forgot password/public pages, otherwise true

Example for a Registration page:
{{
    "mentioned_items": ["First Name (required)", "Last Name (required)", "Address (required)", "City (required)", "State (required)", "Zip Code (required)", "Phone (required)", "SSN (required)", "Username (required)", "Password (required)", "Confirm Password (required)", "Register button"],
    "workflows": ["Register new account"],
    "business_rules": ["First Name is required", "Last Name is required", "Address is required", "City is required", "State is required", "Zip Code is required", "Phone is required", "SSN is required", "Username is required", "Password is required", "Confirm Password is required", "Password and Confirm Password must match", "Username must be unique"],
    "expected_behaviors": ["Successful registration creates account and logs user in", "Validation errors shown for empty required fields", "Error shown if passwords do not match", "Error shown if username already exists"],
    "requires_auth": false
}}
"""

        try:
            result = self.call_llm_json(extraction_prompt, max_tokens=4000)
        except Exception as e:
            print(f"Warning: LLM extraction failed for module {title}: {e}")
            # Return module with empty extracted data
            return ParsedModule(
                id=module_id,
                title=title,
                raw_description=description,
                mentioned_items=[],
                workflows=[],
                business_rules=[],
                expected_behaviors=[],
                requires_auth=True
            )

        return ParsedModule(
            id=module_id,
            title=title,
            raw_description=description,
            mentioned_items=result.get("mentioned_items", []),
            workflows=result.get("workflows", []),
            business_rules=result.get("business_rules", []),
            expected_behaviors=result.get("expected_behaviors", []),
            requires_auth=result.get("requires_auth", True)
        )
