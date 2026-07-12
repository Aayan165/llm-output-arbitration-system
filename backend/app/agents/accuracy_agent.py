from app.llms.gemini import GeminiProvider
from app.prompts.accuracy import SYSTEM_PROMPT
from app.schemas.critic import CriticResult

class AccuracyAgent:
    def __init__(self):
        self.llm = GeminiProvider()

    def evaluate(
        self,
        prompt: str,
        response: str
    ) -> CriticResult:
        full_prompt = f"""
{SYSTEM_PROMPT}

User Prompt:
{prompt}

LLM Response:
{response}
"""
        data = self.llm.generate_json(full_prompt)

        return CriticResult(**data)