"""
StandardPatternsAgent — emits generic web-app quality tests
(session security + RBAC boundaries) that functional specs never describe.

Patterns are emitted CONDITIONALLY based on signals pre-computed in Python
from the spec and navigation graph. The LLM receives explicit True/False
per signal and is forbidden from inventing patterns whose signal is False.

Tests produced here carry test_type="standard" and bypass the spec_evidence
grounding check that applies to spec-derived negative/edge tests.
"""

import re
from typing import Any, Dict, List, Optional

from testwright.agents.base import BaseAgent
from testwright.models.schemas import (
    NavigationGraph,
    ParsedFunctionalDescription,
    ParsedModule,
    ProjectContext,
    TestCase,
)


class StandardPatternsAgent(BaseAgent):
    """Emit generic quality test patterns (session + RBAC)."""

    @property
    def name(self) -> str:
        return "Standard Patterns Agent"

    @property
    def system_prompt(self) -> str:
        return """You generate STANDARD QUALITY tests for web applications — concerns
that apply to every authenticated app regardless of its functional spec:
session security (logout behavior, session expiry, direct URL access) and
role/permission boundaries (cross-role access, data scoping).

HARD RULES:
1. Emit ONLY patterns from the catalog below.
2. Never invent a pattern not in the catalog.
3. Never emit a pattern whose signal is False in the input. If has_remember_me
   is False, NEVER emit a Remember-Me test. If has_multiple_roles is False,
   NEVER emit RBAC tests. No exceptions.
4. Every test must be concrete and executable in a browser (describe what the
   tester does and what they verify).
5. Output valid JSON matching the schema in the user prompt.

CATALOG OF PATTERNS:

UNIVERSAL (emit when has_auth=True AND has_logout=True):
  U1. Post-logout redirect — navigating to a previously-open authenticated page
      after logout redirects to login.
  U2. Browser back button after logout does not restore the authenticated page
      (no cached authenticated content is shown).
  U3. Direct URL access while logged out redirects to login (emit ONCE per app,
      attached to a representative protected module).
  U4. Session expiry mid-form shows an expiry notice or redirects to login.
  U5. Page refresh on an authenticated page keeps the user logged in.

FEATURE-CONDITIONAL (emit only if the matching signal is True):
  F1. (has_remember_me) Remember Me checked → session persists after closing
      and reopening the browser.
  F2. (has_remember_me) Remember Me unchecked → session does NOT persist after
      closing and reopening the browser.
  F3. (has_captcha) After the stated number of failed login attempts, a CAPTCHA
      or lockout is enforced before another attempt is allowed.
  F4. (has_password_reset) A forgot-password reset link expires after the stated
      duration; using an expired link shows an appropriate error.
  F5. (has_password_reset) Forgot password shows a clear error for an email not
      registered in the system (not silent success).
  F6. (has_password_change) After a successful password change, the old password
      no longer authenticates.

RBAC (emit when has_multiple_roles=True):
  R1. Lower-privileged role cannot see UI elements reserved for higher roles
      on a given module.
  R2. Lower-privileged role receives an access-denied or redirect when hitting
      the direct URL of a higher-role page.
  R3. A user cannot access another user's private data (cross-user isolation)
      on modules with per-user scoped data.
  R4. An unauthenticated user clicking a protected action is redirected to
      login before being able to proceed.

OUTPUT:
  - test_type is ALWAYS "standard".
  - Steps are concrete tester actions (2–5 steps typical).
  - expected_result states the verifiable outcome.
  - module_id attaches the test to an existing module in the app (session
    patterns → login_module_id; RBAC → module where the privileged UI lives).
  - Do not fabricate features. If the spec does not describe a Remember Me
    checkbox, do not generate a Remember Me test even if users might expect it."""

    # ------------------------------------------------------------------
    # Signal pre-computation (Python, before LLM)
    # ------------------------------------------------------------------

    _LOGOUT_KEYWORDS = ("logout", "log out", "sign out", "signout")
    _REMEMBER_ME_KEYWORDS = (
        "remember me",
        "keep me signed in",
        "keep me logged in",
        "stay logged in",
        "stay signed in",
    )
    _CAPTCHA_KEYWORDS = (
        "captcha",
        "failed attempts",
        "failed login",
        "attempt limit",
        "lockout",
        "locked out",
        "account lock",
    )
    _PASSWORD_RESET_KEYWORDS = (
        "forgot password",
        "password reset",
        "reset password",
        "reset link",
    )
    _PASSWORD_CHANGE_KEYWORDS = (
        "change password",
        "update password",
        "new password",
    )
    _ROLE_KEYWORDS = (
        "administrator",
        "admin role",
        "teacher",
        "student",
        "manager",
        "role",
        "roles",
        "permission",
        "permissions",
        "privilege",
    )

    def _build_spec_blob(
        self,
        parsed_desc: ParsedFunctionalDescription,
    ) -> str:
        parts: List[str] = [
            parsed_desc.navigation_overview or "",
        ]
        for m in parsed_desc.modules:
            parts.append(m.raw_description or "")
            parts.extend(m.workflows or [])
            parts.extend(m.business_rules or [])
            parts.extend(m.expected_behaviors or [])
        return " ".join(parts).lower()

    def _any_keyword(self, blob: str, keywords) -> bool:
        return any(k in blob for k in keywords)

    def _compute_signals(
        self,
        parsed_desc: ParsedFunctionalDescription,
        nav_graph: NavigationGraph,
    ) -> Dict[str, Any]:
        blob = self._build_spec_blob(parsed_desc)

        has_auth = any(n.requires_auth for n in nav_graph.nodes.values())
        has_logout = self._any_keyword(blob, self._LOGOUT_KEYWORDS)
        has_remember_me = self._any_keyword(blob, self._REMEMBER_ME_KEYWORDS)
        has_captcha = self._any_keyword(blob, self._CAPTCHA_KEYWORDS)
        has_password_reset = self._any_keyword(blob, self._PASSWORD_RESET_KEYWORDS)
        has_password_change = self._any_keyword(blob, self._PASSWORD_CHANGE_KEYWORDS)

        # Multiple roles: at least two of the role-noun keywords appear, OR
        # the navigation_overview explicitly lists roles.
        role_hits = sum(1 for k in self._ROLE_KEYWORDS if k in blob)
        has_multiple_roles = role_hits >= 2

        protected_modules = [
            {"module_id": n.module_id, "title": n.title}
            for n in nav_graph.nodes.values()
            if n.requires_auth and n.module_id != nav_graph.login_module_id
        ]

        return {
            "has_auth": has_auth,
            "has_logout": has_logout,
            "has_remember_me": has_remember_me,
            "has_captcha": has_captcha,
            "has_password_reset": has_password_reset,
            "has_password_change": has_password_change,
            "has_multiple_roles": has_multiple_roles,
            "login_module_id": nav_graph.login_module_id,
            "protected_modules": protected_modules,
        }

    # ------------------------------------------------------------------
    # Prompt + run
    # ------------------------------------------------------------------

    def _build_user_prompt(
        self,
        signals: Dict[str, Any],
        project_name: str,
    ) -> str:
        import json as _json

        protected_list = signals["protected_modules"][:15]

        return f"""Project: {project_name or 'Web Application'}

DETECTED SIGNALS (computed from spec — TRUST these; DO NOT override):
{_json.dumps({k: v for k, v in signals.items() if k != 'protected_modules'}, indent=2)}

PROTECTED MODULES (candidates for RBAC or direct-URL-access tests):
{_json.dumps(protected_list, indent=2)}

LOGIN MODULE ID: {signals['login_module_id']}

TASK:
Generate standard quality tests per the catalog in your system prompt.
For EACH catalog pattern:
  - If its precondition signal is True → emit exactly ONE test.
  - If its precondition signal is False → emit NOTHING for that pattern.

ATTACHMENT RULES:
  - Session / password / Remember Me / CAPTCHA tests → attach to login module
    (module_id = {signals['login_module_id']}).
  - U3 (direct URL access while logged out) → emit ONCE, attach to the FIRST
    protected module in the list above.
  - R1/R2 (role-gated UI and URL) → pick a relevant protected module from the
    list; attach the test to it. Emit for 2–3 different modules if multiple
    protected modules exist.
  - R3 (cross-user isolation) → attach to a module with clearly per-user data
    (accounts, grades, bookings, profile) — pick from the protected list.
  - R4 (unauthenticated user hits protected action) → attach to an
    entry-point protected module.

OUTPUT SCHEMA (JSON only):
{{
  "tests": [
    {{
      "title": "concise test title",
      "test_type": "standard",
      "priority": "High" | "Medium" | "Low",
      "preconditions": "what must be true before running",
      "steps": ["step 1", "step 2", ...],
      "expected_result": "verifiable outcome",
      "module_id": <int>,
      "workflow": "Session Security" | "RBAC" | "Password" | "Remember Me" | "Login Protection"
    }}
  ]
}}

HARD REMINDER:
- Do NOT emit a pattern whose signal is False.
- If has_auth is False, emit an empty "tests" list.
- Use ONLY module_ids from the PROTECTED MODULES list or LOGIN MODULE ID."""

    def run(
        self,
        parsed_desc: ParsedFunctionalDescription,
        nav_graph: NavigationGraph,
        project_context: Optional[ProjectContext] = None,
    ) -> List[TestCase]:
        """Generate standard quality test patterns for the app."""

        signals = self._compute_signals(parsed_desc, nav_graph)

        # Short-circuit: no auth at all → no standard patterns apply.
        if not signals["has_auth"]:
            if self.debug:
                self._log_debug("SIGNALS", "has_auth=False — skipping standard patterns")
            return []

        project_name = (
            project_context.project_name if project_context else parsed_desc.project_name
        ) or "Web Application"

        prompt = self._build_user_prompt(signals, project_name)

        try:
            raw = self.call_llm_json(
                user_prompt=prompt,
                temperature=0.3,
                max_tokens=4000,
            )
        except Exception as e:
            print(f"  !! StandardPatternsAgent: LLM call failed ({e}); emitting no standard tests")
            return []

        raw_tests = raw.get("tests", []) if isinstance(raw, dict) else []
        module_id_by_lookup = {n.module_id: n.title for n in nav_graph.nodes.values()}

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

            tc = TestCase(
                id="",  # assigned by assembler
                title=title,
                module_id=module_id,
                module_title=module_id_by_lookup.get(module_id, ""),
                workflow=(r.get("workflow") or "Standard Quality").strip(),
                test_type="standard",
                priority=(r.get("priority") or "Medium").strip() or "Medium",
                preconditions=(r.get("preconditions") or "").strip(),
                steps=[str(s).strip() for s in steps if str(s).strip()],
                expected_result=expected,
                spec_evidence="",
                needs_post_verification=False,
            )
            out.append(tc)

        if self.debug:
            self._log_debug(
                "STANDARD TESTS EMITTED",
                f"{len(out)} tests from signals={signals}",
            )
        return out
