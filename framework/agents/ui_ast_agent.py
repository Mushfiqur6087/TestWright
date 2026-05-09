"""UI-AST Agent: converts a module's functional description into a UI Abstract Syntax Tree."""

from importlib import resources
from typing import Any, Dict, List, Optional

from autospectest.framework.agents.base import BaseAgent

_PROMPT = resources.files("autospectest.prompts").joinpath("ui_ast.md").read_text(encoding="utf-8")


class UIASTAgent(BaseAgent):

    @property
    def name(self) -> str:
        return "UI-AST Agent"

    @property
    def system_prompt(self) -> str:
        return _PROMPT

    def run(self, module: Dict[str, Any], fixes: Optional[List[str]] = None) -> Dict[str, Any]:
        return self.call_llm_json(
            self._build_prompt(module, fixes),
            temperature=0.1,
            max_tokens=8192,
            reasoning_effort="medium",
        )

    async def arun(self, module: Dict[str, Any], fixes: Optional[List[str]] = None) -> Dict[str, Any]:
        return await self.acall_llm_json(
            self._build_prompt(module, fixes),
            temperature=0.1,
            max_tokens=8192,
            reasoning_effort="medium",
        )

    @staticmethod
    def _build_prompt(module: Dict[str, Any], fixes: Optional[List[str]]) -> str:
        prompt = f"Module: {module['title']}\n\n{module['description']}"
        if fixes:
            prompt += "\n\n**CRITIC FEEDBACK FROM PREVIOUS ATTEMPT — address every point:**\n"
            for i, fix in enumerate(fixes, 1):
                prompt += f"{i}. {fix}\n"
        return prompt
