from app.agents.base_critic import BaseCriticAgent
from app.prompts.accuracy import SYSTEM_PROMPT
from app.schemas.critic import CriticResult

class CompletenessAgent(BaseCriticAgent):
    def evaluate(
        self,
        prompt: str,
        response: str
    ):
        return super().evaluate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
            llm_response=response,
            output_schema=CriticResult
        )