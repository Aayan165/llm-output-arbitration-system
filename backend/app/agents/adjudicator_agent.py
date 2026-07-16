from app.llms.gemini import GeminiProvider
from app.prompts.adjudicator import SYSTEM_PROMPT
from app.schemas.verdict import FinalVerdict

class AdjudicatorAgent:
    def __init__(self, llm):
        self.llm = llm

    def evaluate(
        self,
        accuracy,
        logic,
        completeness
    ):
        prompt = f"""
{SYSTEM_PROMPT}

Accuracy Critic:

{accuracy.model_jump_json(indent=2)}

Logic Critic:

{logic.model_jump_json(indent=2)}

Completeness Critic:

{completeness.model_jump_json(indent=2)}
"""
        data = self.llm.generate_json(prompt)
        return FinalVerdict(**data)