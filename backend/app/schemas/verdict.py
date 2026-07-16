from pydantic import BaseModel
from typing import List

class FinalVerdict(BaseModel):
    overall_score: float
    verdict: str
    summary: str
    strengths: List[str]
    weaknesses: List[str]
    improvements: List[str]