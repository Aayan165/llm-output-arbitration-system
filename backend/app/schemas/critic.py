from pydantic import BaseModel, Field
from typing import List

class CriticResult(BaseModel):
    """
    Standard output returned by every critic agent.
    """

    score: float = Field(..., ge=0, le=10)
    reasoning: str
    strengths: List[str]
    issues: List[str]
    suggestions: List[str]
