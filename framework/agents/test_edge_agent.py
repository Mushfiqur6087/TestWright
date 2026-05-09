"""Edge Case Agent: generates boundary and unusual-interaction test cases from a UI-AST."""

import json
from importlib import resources
from typing import Any, Dict

from autospectest.framework.agents.base import BaseAgent

_PROMPT = resources.files("autospectest.prompts").joinpath("test_edge.md").read_text(encoding="utf-8")


class TestEdgeAgent(BaseAgent):

    @property
    def name(self) -> str:
        return "Test-Edge"

    @property
    def system_prompt(self) -> str:
        return _PROMPT

    def run(self, module_title: str, ast: Dict[str, Any]) -> Dict[str, Any]:
        return self.call_llm_json(
            self._build_prompt(module_title, ast),
            temperature=0.4,
            max_tokens=8192,
        )

    async def arun(self, module_title: str, ast: Dict[str, Any]) -> Dict[str, Any]:
        return await self.acall_llm_json(
            self._build_prompt(module_title, ast),
            temperature=0.4,
            max_tokens=8192,
        )

    @staticmethod
    def _build_prompt(module_title: str, ast: Dict[str, Any]) -> str:
        return (
            f"<module_name>{module_title}</module_name>\n\n"
            f"<ast>\n{json.dumps(ast, indent=2)}\n</ast>"
        )
