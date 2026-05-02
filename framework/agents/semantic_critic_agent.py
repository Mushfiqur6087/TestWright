"""Semantic Critic Agent: audits UI-AST JSON against the source functional description."""

import json
from importlib import resources
from typing import Any, Dict

from autospectest.framework.agents.base import BaseAgent

_PROMPT = resources.files("autospectest.prompts").joinpath("semantic_critic.md").read_text(encoding="utf-8")


class SemanticCriticAgent(BaseAgent):

    @property
    def name(self) -> str:
        return "Semantic Critic"

    @property
    def system_prompt(self) -> str:
        return _PROMPT

    def run(self, description: str, ast: Dict[str, Any]) -> Dict[str, Any]:
        return self.call_llm_json(self._build_prompt(description, ast), temperature=0.1, mmax_tokens=8192)

    async def arun(self, description: str, ast: Dict[str, Any]) -> Dict[str, Any]:
        return await self.acall_llm_json(self._build_prompt(description, ast), temperature=0.1,max_tokens=8192)

    @staticmethod
    def _build_prompt(description: str, ast: Dict[str, Any]) -> str:
        return (
            f"<description>\n{description}\n</description>\n\n"
            f"<ast>\n{json.dumps(ast, indent=2)}\n</ast>"
        )
