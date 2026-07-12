from pydantic import BaseModel, Field
from typing import List

class CriticResult(BaseModel):
    """
    Standard output returned by every critic agent.
    """

    score: float = Field(..., ge=0, le=10)
    reasoning: str
    issues: List[str]
    suggestions: List[str]

class FinalVerdict(BaseModel):
    """
    Output returned by adjudicator.
    """

    overall_score: float = Field(..., ge=0, le=10)
    confidene: float = Field(..., ge=0, le=100)
    summary: str
    cofirmed_issues: List[str]
    recommendations: List[str]