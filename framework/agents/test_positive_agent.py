"""Positive Test Case Agent: generates happy-path and functional test cases from a UI-AST."""

import json
from importlib import resources
from typing import Any, Dict

from autospectest.framework.agents.base import BaseAgent

_PROMPT = resources.files("autospectest.prompts").joinpath("test_positive.md").read_text(encoding="utf-8")


class TestPositiveAgent(BaseAgent):

    @property
    def name(self) -> str:
        return "Test-Positive"

    @property
    def system_prompt(self) -> str:
        return _PROMPT

    def run(self, module_title: str, ast: Dict[str, Any], description: str) -> Dict[str, Any]:
        return self.call_llm_json(
            self._build_prompt(module_title, ast, description),
            temperature=0.3,
            max_tokens=8192,
        )

    async def arun(self, module_title: str, ast: Dict[str, Any], description: str) -> Dict[str, Any]:
        return await self.acall_llm_json(
            self._build_prompt(module_title, ast, description),
            temperature=0.3,
            max_tokens=8192,
        )

    @staticmethod
    def _build_prompt(module_title: str, ast: Dict[str, Any], description: str) -> str:
        return (
            f"<module_name>{module_title}</module_name>\n\n"
            f"<ast>\n{json.dumps(ast, indent=2)}\n</ast>\n\n"
            f"<description>\n{description}\n</description>"
        )
