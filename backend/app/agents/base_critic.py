from abc import ABC
from typing import Type

from app.llms.gemini import GeminiProvider
from app.schemas.critic import CriticResult

class BaseCriticAgent(ABC):
    def __init__(self, llm):
        self.llm = llm

    def evaluate(
            self,
            system_prompt: str,
            user_prompt: str,
            llm_response: str,
            output_schema: Type[CriticResult]
    ):
        full_prompt = f"""
{system_prompt}

User Prompt:
{user_prompt}

LLM Response:
{llm_response}
"""
        
        data = self.llm.generate_json(full_prompt)

        return output_schema(**data)