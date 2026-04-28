"""
StandardPatternsAgent — emits a small fixed catalog of session/login/logout
flow tests that every authenticated app needs but functional specs never
describe (post-logout redirect, browser refresh after logout, direct URL
access while logged out, etc.).

Login and logout modules are detected by case-insensitive substring match on
node titles. If no logout module exists, logout tests fall back to the login
module. If no login module exists, the agent emits no tests.

All tests use test_type "positive" or "negative" — there is no "standard" type.
"""

from typing import List, Optional

from autospectest.framework.agents.base import BaseAgent
from autospectest.framework.schemas.schemas import (
    NavigationGraph,
    ParsedFunctionalDescription,
    ProjectContext,
    TestCase,
)


class StandardPatternsAgent(BaseAgent):
    """Emit session/login/logout flow tests."""

    _LOGIN_TITLE_KEYWORDS = (
        "login",
        "log in",
        "sign in",
        "signin",
        "log on",
        "logon",
        "sign on",
        "signon",
        "authenticate",
        "authentication",
    )
    _LOGOUT_TITLE_KEYWORDS = (
        "logout",
        "log out",
        "sign out",
        "signout",
        "log off",
        "logoff",
        "sign off",
        "signoff",
    )

    @property
    def name(self) -> str:
        return "Standard Patterns Agent"

    @property
    def system_prompt(self) -> str:
        return """You generate a small fixed catalog of session/login/logout
flow tests for web applications — concerns that apply to every authenticated
app regardless of its functional spec.

HARD RULES:
1. Emit ONLY the patterns enumerated in the user prompt. Do NOT invent extra
   patterns (no Remember Me, no CAPTCHA, no password reset, no RBAC, no edge
   variants).
2. Every test is concrete and executable in a browser (describe what the
   tester does and what they verify).
3. test_type is "positive" or "negative" — never "standard".
4. Use ONLY the module_ids supplied in the user prompt for attachment.
5. Output valid JSON matching the schema in the user prompt.

STEP STYLE:
- 2 to 4 short, imperative steps per test.
- Reference real protected pages by their actual titles when given (e.g.,
  "Navigate to Dashboard"). If no protected modules are listed, use the
  generic phrase "a protected page".
- Do not hardcode specific URLs, credentials, or error message strings."""

    def _find_module_id_by_keywords(
        self,
        nav_graph: NavigationGraph,
        keywords: tuple,
    ) -> Optional[int]:
        for node in nav_graph.nodes.values():
            title_lower = (node.title or "").lower()
            if any(k in title_lower for k in keywords):
                return node.module_id
        return None

    def _build_user_prompt(
        self,
        project_name: str,
        navigation_overview: str,
        login_module_id: int,
        login_module_title: str,
        logout_module_id: int,
        logout_module_title: str,
        logout_is_fallback: bool,
        protected_modules: List[dict],
    ) -> str:
        import json as _json

        protected_blob = _json.dumps(protected_modules[:10], indent=2)
        logout_note = (
            f"(no separate logout module; falling back to login module {login_module_id})"
            if logout_is_fallback
            else ""
        )

        return f"""Project: {project_name or 'Web Application'}
Navigation overview: {navigation_overview or '(none provided)'}

LOGIN MODULE: id={login_module_id}, title="{login_module_title}"
LOGOUT MODULE: id={logout_module_id}, title="{logout_module_title}" {logout_note}

PROTECTED MODULES (use only to phrase realistic step text — do NOT attach tests to these):
{protected_blob}

GENERATE EXACTLY THESE 6 TESTS — one per pattern, in this order. Use the
provided module_id verbatim for each test's attachment.

LOGIN MODULE TESTS (module_id = {login_module_id}, workflow = "Login"):

  L1. title: "Direct URL access while logged out redirects to login"
      test_type: positive   priority: High
      preconditions: User is not logged in
      idea: Without logging in, navigate directly to a protected URL → user
            is redirected to the login page.

  L2. title: "Page refresh while logged in keeps user logged in"
      test_type: positive   priority: Medium
      preconditions: User is logged in on an authenticated page
      idea: Refresh the browser → user remains authenticated and the page
            re-renders without redirecting to login.

  L3. title: "Already-logged-in user navigating to login URL is redirected to authenticated landing page"
      test_type: positive   priority: Medium
      preconditions: User is already logged in
      idea: Navigate to the login URL while already authenticated → user is
            redirected away from login (to the authenticated landing page).

LOGOUT MODULE TESTS (module_id = {logout_module_id}, workflow = "Logout"):

  O1. title: "Logout from user menu terminates session and shows login page"
      test_type: positive   priority: High
      preconditions: User is logged in
      idea: Open the user/profile menu and click Logout → session is
            terminated and the login page is displayed.

  O2. title: "Protected routes inaccessible after logout"
      test_type: positive   priority: High
      preconditions: User has just logged out after an active session
      idea: After logout, attempt to navigate to a protected route → user is
            redirected to login or access is denied.

  O3. title: "Browser refresh after logout does not restore authenticated session"
      test_type: positive   priority: High
      preconditions: User has just logged out
      idea: Refresh the browser after logout → user remains logged out (no
            authenticated content reappears).

OUTPUT SCHEMA (JSON only):
{{
  "tests": [
    {{
      "title": "<exactly the title shown above>",
      "test_type": "positive",
      "priority": "High" | "Medium" | "Low",
      "preconditions": "<single precondition statement>",
      "steps": ["step 1", "step 2", ...],
      "expected_result": "<single verifiable outcome>",
      "module_id": <int>,
      "workflow": "Login" | "Logout"
    }}
  ]
}}

Emit all 6 tests. Do not skip, merge, or add tests."""

    def run(
        self,
        parsed_desc: ParsedFunctionalDescription,
        nav_graph: NavigationGraph,
        project_context: Optional[ProjectContext] = None,
    ) -> List[TestCase]:
        """Generate the fixed login/logout session test catalog."""

        login_module_id = self._find_module_id_by_keywords(nav_graph, self._LOGIN_TITLE_KEYWORDS)
        if login_module_id is None:
            if self.debug:
                self._log_debug("SIGNALS", "no login module found — skipping standard patterns")
            return []

        logout_module_id = self._find_module_id_by_keywords(nav_graph, self._LOGOUT_TITLE_KEYWORDS)
        logout_is_fallback = logout_module_id is None
        if logout_is_fallback:
            logout_module_id = login_module_id

        module_title_by_id = {n.module_id: n.title for n in nav_graph.nodes.values()}
        login_module_title = module_title_by_id.get(login_module_id, "")
        logout_module_title = module_title_by_id.get(logout_module_id, "")

        protected_modules = [
            {"module_id": n.module_id, "title": n.title}
            for n in nav_graph.nodes.values()
            if n.module_id != login_module_id and n.module_id != logout_module_id
        ]

        project_name = (
            project_context.project_name if project_context else parsed_desc.project_name
        ) or "Web Application"
        navigation_overview = (
            project_context.navigation_overview if project_context else parsed_desc.navigation_overview
        ) or ""

        prompt = self._build_user_prompt(
            project_name=project_name,
            navigation_overview=navigation_overview,
            login_module_id=login_module_id,
            login_module_title=login_module_title,
            logout_module_id=logout_module_id,
            logout_module_title=logout_module_title,
            logout_is_fallback=logout_is_fallback,
            protected_modules=protected_modules,
        )

        try:
            raw = self.call_llm_json(
                user_prompt=prompt,
                temperature=0.3,
                max_tokens=3000,
            )
        except Exception as e:
            print(f"  !! StandardPatternsAgent: LLM call failed ({e}); emitting no standard tests")
            return []

        raw_tests = raw.get("tests", []) if isinstance(raw, dict) else []
        allowed_module_ids = {n.module_id for n in nav_graph.nodes.values()}

        out: List[TestCase] = []
        for r in raw_tests:
            try:
                module_id = int(r.get("module_id"))
            except (TypeError, ValueError):
                continue
            if module_id not in allowed_module_ids:
                continue

            title = (r.get("title") or "").strip()
            steps = r.get("steps") or []
            expected = (r.get("expected_result") or "").strip()
            if not title or not steps or not expected:
                continue

            test_type = (r.get("test_type") or "positive").strip().lower()
            if test_type not in ("positive", "negative"):
                test_type = "positive"

            priority = (r.get("priority") or "Medium").strip()
            if priority not in ("High", "Medium", "Low"):
                priority = "Medium"

            tc = TestCase(
                id="",  # assigned by assembler
                title=title,
                module_id=module_id,
                module_title=module_title_by_id.get(module_id, ""),
                workflow=(r.get("workflow") or "Session").strip(),
                test_type=test_type,
                priority=priority,
                preconditions=(r.get("preconditions") or "").strip() or "None",
                steps=[str(s).strip() for s in steps if str(s).strip()],
                expected_result=expected,
                spec_evidence="",
            )
            out.append(tc)

        if self.debug:
            self._log_debug(
                "STANDARD TESTS EMITTED",
                f"{len(out)} tests "
                f"(login_module_id={login_module_id}, "
                f"logout_module_id={logout_module_id}, "
                f"logout_is_fallback={logout_is_fallback})",
            )
        return out
