import asyncio
from typing import Dict, Any

from autospectest.framework.agents.base import BaseAgent
from autospectest.framework.schemas.schemas import (
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
1. Extract ONLY what is explicitly mentioned in the functional description.
2. DO NOT infer, assume, or add information not present in the text.
3. DO NOT specify UI element types (button/input/dropdown) - just extract names as written.
4. Use the EXACT wording from the description whenever possible.
5. EXPLICIT LINGUISTIC LINKING: Because you are outputting flat arrays, every business rule and behavior MUST explicitly include the exact name of the item it governs so downstream systems can map them together.

Your task is to analyze functional descriptions and extract:

1. Mentioned Items: Fields, buttons, links, and interactive elements mentioned.
2. Workflows: User actions that involve form submission or data processing on THIS page.
3. Business Rules: Validation rules, constraints, and business logic stated.
4. Expected Behaviors: What happens on success or failure.

WORKFLOW GUIDANCE:
- Focus on actions that complete on THIS page with a testable outcome.
- Links to other pages (Register, Forgot Password) are navigation elements, not workflows.
- If a page has multiple forms, each form's submission is a separate workflow."""

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
            modules=parsed_modules,
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
    "expected_behaviors": ["Behavior1", "Behavior2", ...]
}}

Field Descriptions:

- mentioned_items: Extract ALL individual form fields, buttons, and interactive elements as SEPARATE items.
  * List EACH field separately (not grouped as "form fields").
  * Mark required fields with "(required)" suffix.
  * Include buttons, links, dropdowns, and other interactive elements.
  * Example: ["First Name (required)", "Last Name (required)", "Submit button", "Cancel link"]

- workflows: PRIMARY actions that COMPLETE on this page with a testable outcome.
  * A workflow involves form submission or data processing.
  * Navigation links to other pages are NOT workflows.
  * MENU / DROPDOWN / TOOLBAR CONSOLIDATION: If a single control
    (three-dot menu, action dropdown, bulk-actions toolbar, context menu, kebab
    menu) exposes multiple actions on the same entity kind, list it as ONE
    workflow (e.g., "Section-level three-dot menu actions"), NOT one workflow
    per action. The individual actions (edit, duplicate, hide, delete, move)
    become items in `expected_behaviors` of that single workflow.
  * HARD CEILING: Emit AT MOST 5 workflows per module. If you identify more
    than 5, consolidate related ones by their UI surface (same menu / same
    form / same toolbar / same modal) until you are at <= 5.

  Worked example — Course Edit Mode page with three-dot menus on sections and activities:
    WRONG (over-segmented, 10+ workflows):
      ["Section menu: edit", "Section menu: duplicate", "Section menu: hide",
       "Section menu: delete", "Section menu: move",
       "Activity menu: edit settings", "Activity menu: move",
       "Activity menu: hide", "Activity menu: delete", "Enable edit mode"]
    CORRECT (consolidated, 3 workflows):
      ["Toggle edit mode",
       "Section-level three-dot menu actions",
       "Activity-level three-dot menu actions"]
    The individual menu actions live in expected_behaviors, e.g.:
      "Section menu lists edit, duplicate, hide, delete, move",
      "Clicking Edit on a section opens an inline rename field".

- business_rules: Extract ALL validation rules and constraints with STRICT PREFIXING.
  * You MUST prefix every rule with the exact name of the item, action, or workflow it governs.
  * Format: "<Prefix>: <rule text extracted from description>"
  * Prefix priority:
      1. Exact item name from mentioned_items (including "(required)" suffix if present)
         e.g., "Username (required): must be unique"
      2. For cross-field rules, use the dependent field: "Confirm Password (required): must match Password"
      3. Action name visible in the description: "Close action: cannot close client with active accounts"
      4. Exact workflow name from the workflows array: "Register new account: form validates on submit"
      5. The literal token "Global" for module-wide invariants: "Global: total debits must equal total credits"
  * DO NOT emit a bare rule without a prefix. If you cannot identify a governing item, action, or workflow, omit the rule entirely.

- expected_behaviors: Success/failure outcomes explicitly mentioned with STRICT PREFIXING.
  * You MUST prefix every behavior with the exact trigger item, action, or workflow.
  * Format: "<Trigger>: <behavior extracted from description>"
  * Use the same prefix priority as business_rules above.
  * Example CORRECT: ["Login with credentials: Valid credentials redirect to the Dashboard",
                      "Login with credentials: Invalid credentials show an error message",
                      "Submit button: Validation errors shown for empty required fields"]
  * Example WRONG: ["Redirects to Dashboard", "Shows error message"]

Example for a Registration page:
{{
    "mentioned_items": ["First Name (required)", "Last Name (required)", "Address (required)", "City (required)", "State (required)", "Zip Code (required)", "Phone (required)", "SSN (required)", "Username (required)", "Password (required)", "Confirm Password (required)", "Register button"],
    "workflows": ["Register new account"],
    "business_rules": [
        "First Name (required): is required",
        "Last Name (required): is required",
        "Address (required): is required",
        "City (required): is required",
        "State (required): is required",
        "Zip Code (required): is required",
        "Phone (required): is required",
        "SSN (required): is required",
        "Username (required): is required",
        "Username (required): must be unique",
        "Password (required): is required",
        "Confirm Password (required): is required",
        "Confirm Password (required): must match Password"
    ],
    "expected_behaviors": [
        "Register new account: Successful registration creates account and logs user in",
        "Register button: Validation errors shown for empty required fields",
        "Confirm Password (required): Error shown if passwords do not match",
        "Username (required): Error shown if username already exists"
    ]
}}
"""

        try:
            result = self.call_llm_json(extraction_prompt, max_tokens=16000)
        except Exception as e:
            print(f"Warning: LLM extraction failed for module {title}: {e}")
            return ParsedModule(
                id=module_id,
                title=title,
                raw_description=description,
                mentioned_items=[],
                workflows=[],
                business_rules=[],
                expected_behaviors=[],
            )

        rules = result.get("business_rules", [])
        behaviors = result.get("expected_behaviors", [])
        unprefixed = [e for e in rules + behaviors if isinstance(e, str) and ": " not in e]
        if unprefixed:
            print(f"Warning: Parser found {len(unprefixed)} unprefixed rule(s) in '{title}': {unprefixed}")

        return ParsedModule(
            id=module_id,
            title=title,
            raw_description=description,
            mentioned_items=result.get("mentioned_items", []),
            workflows=result.get("workflows", []),
            business_rules=rules,
            expected_behaviors=behaviors,
        )

    async def _aparse_module(self, module: Dict[str, Any]) -> ParsedModule:
        """Async version of _parse_module — calls acall_llm_json instead of call_llm_json."""
        module_id = module.get("id", 0)
        title = module.get("title", "Unknown Module")
        description = module.get("description", "")

        extraction_prompt = f"""Analyze this functional description and extract information for test case generation.

Module Title: {title}
Description: {description}

IMPORTANT: Extract ONLY what is explicitly mentioned. Do NOT add assumptions or infer details not present.

Return a JSON object with these fields:
{{
    "mentioned_items": ["Item1", "Item2", ...],
    "workflows": ["Workflow1", ...],
    "business_rules": ["Rule1", "Rule2", ...],
    "expected_behaviors": ["Behavior1", "Behavior2", ...]
}}

Field Descriptions:

- mentioned_items: Extract ALL individual form fields, buttons, and interactive elements as SEPARATE items.
  * List EACH field separately (not grouped as "form fields").
  * Mark required fields with "(required)" suffix.
  * Include buttons, links, dropdowns, and other interactive elements.
  * Example: ["First Name (required)", "Last Name (required)", "Submit button", "Cancel link"]

- workflows: PRIMARY actions that COMPLETE on this page with a testable outcome.
  * A workflow involves form submission or data processing.
  * Navigation links to other pages are NOT workflows.
  * MENU / DROPDOWN / TOOLBAR CONSOLIDATION: If a single control
    (three-dot menu, action dropdown, bulk-actions toolbar, context menu, kebab
    menu) exposes multiple actions on the same entity kind, list it as ONE
    workflow (e.g., "Section-level three-dot menu actions"), NOT one workflow
    per action. The individual actions (edit, duplicate, hide, delete, move)
    become items in `expected_behaviors` of that single workflow.
  * HARD CEILING: Emit AT MOST 5 workflows per module. If you identify more
    than 5, consolidate related ones by their UI surface (same menu / same
    form / same toolbar / same modal) until you are at <= 5.

  Worked example — Course Edit Mode page with three-dot menus on sections and activities:
    WRONG (over-segmented, 10+ workflows):
      ["Section menu: edit", "Section menu: duplicate", "Section menu: hide",
       "Section menu: delete", "Section menu: move",
       "Activity menu: edit settings", "Activity menu: move",
       "Activity menu: hide", "Activity menu: delete", "Enable edit mode"]
    CORRECT (consolidated, 3 workflows):
      ["Toggle edit mode",
       "Section-level three-dot menu actions",
       "Activity-level three-dot menu actions"]
    The individual menu actions live in expected_behaviors, e.g.:
      "Section menu lists edit, duplicate, hide, delete, move",
      "Clicking Edit on a section opens an inline rename field".

- business_rules: Extract ALL validation rules and constraints with STRICT PREFIXING.
  * You MUST prefix every rule with the exact name of the item, action, or workflow it governs.
  * Format: "<Prefix>: <rule text extracted from description>"
  * Prefix priority:
      1. Exact item name from mentioned_items (including "(required)" suffix if present)
         e.g., "Username (required): must be unique"
      2. For cross-field rules, use the dependent field: "Confirm Password (required): must match Password"
      3. Action name visible in the description: "Close action: cannot close client with active accounts"
      4. Exact workflow name from the workflows array: "Register new account: form validates on submit"
      5. The literal token "Global" for module-wide invariants: "Global: total debits must equal total credits"
  * DO NOT emit a bare rule without a prefix. If you cannot identify a governing item, action, or workflow, omit the rule entirely.

- expected_behaviors: Success/failure outcomes explicitly mentioned with STRICT PREFIXING.
  * You MUST prefix every behavior with the exact trigger item, action, or workflow.
  * Format: "<Trigger>: <behavior extracted from description>"
  * Use the same prefix priority as business_rules above.
  * Example CORRECT: ["Login with credentials: Valid credentials redirect to the Dashboard",
                      "Login with credentials: Invalid credentials show an error message",
                      "Submit button: Validation errors shown for empty required fields"]
  * Example WRONG: ["Redirects to Dashboard", "Shows error message"]

Example for a Registration page:
{{
    "mentioned_items": ["First Name (required)", "Last Name (required)", "Address (required)", "City (required)", "State (required)", "Zip Code (required)", "Phone (required)", "SSN (required)", "Username (required)", "Password (required)", "Confirm Password (required)", "Register button"],
    "workflows": ["Register new account"],
    "business_rules": [
        "First Name (required): is required",
        "Last Name (required): is required",
        "Address (required): is required",
        "City (required): is required",
        "State (required): is required",
        "Zip Code (required): is required",
        "Phone (required): is required",
        "SSN (required): is required",
        "Username (required): is required",
        "Username (required): must be unique",
        "Password (required): is required",
        "Confirm Password (required): is required",
        "Confirm Password (required): must match Password"
    ],
    "expected_behaviors": [
        "Register new account: Successful registration creates account and logs user in",
        "Register button: Validation errors shown for empty required fields",
        "Confirm Password (required): Error shown if passwords do not match",
        "Username (required): Error shown if username already exists"
    ]
}}
"""

        try:
            result = await self.acall_llm_json(extraction_prompt, max_tokens=16000)
        except Exception as e:
            print(f"Warning: LLM extraction failed for module {title}: {e}")
            return ParsedModule(
                id=module_id,
                title=title,
                raw_description=description,
                mentioned_items=[],
                workflows=[],
                business_rules=[],
                expected_behaviors=[],
            )

        rules = result.get("business_rules", [])
        behaviors = result.get("expected_behaviors", [])
        unprefixed = [e for e in rules + behaviors if isinstance(e, str) and ": " not in e]
        if unprefixed:
            print(f"Warning: Parser found {len(unprefixed)} unprefixed rule(s) in '{title}': {unprefixed}")

        return ParsedModule(
            id=module_id,
            title=title,
            raw_description=description,
            mentioned_items=result.get("mentioned_items", []),
            workflows=result.get("workflows", []),
            business_rules=rules,
            expected_behaviors=behaviors,
        )

    async def arun(self, functional_desc: Dict[str, Any]) -> ParsedFunctionalDescription:
        """Async version of run: all per-module LLM calls execute concurrently."""
        if not isinstance(functional_desc, dict):
            raise ValueError("Functional description must be a dictionary")

        project_name = functional_desc.get("project_name", "Unknown Project")
        base_url = functional_desc.get("website_url", "")
        navigation_overview = functional_desc.get("navigation_overview", "")
        raw_modules = functional_desc.get("modules", [])

        tasks = [self._aparse_module(m) for m in raw_modules]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        parsed_modules = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                module = raw_modules[i]
                print(f"Warning: LLM extraction failed for module {module.get('title', 'Unknown')}: {result}")
                parsed_modules.append(ParsedModule(
                    id=module.get("id", 0),
                    title=module.get("title", "Unknown Module"),
                    raw_description=module.get("description", ""),
                    mentioned_items=[],
                    workflows=[],
                    business_rules=[],
                    expected_behaviors=[],
                ))
            else:
                parsed_modules.append(result)

        return ParsedFunctionalDescription(
            project_name=project_name,
            base_url=base_url,
            navigation_overview=navigation_overview,
            modules=parsed_modules,
        )
