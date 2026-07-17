from pydantic import BaseModel
from datetime import datetime

class EvaluationRecord(BaseModel):
    id: int
    prompt: str
    response: str
    accuracy_score: float
    logic_score: float
    completeness_score: float
    overall_score: float
    verdict: str
    summary: str
    created_at: datetime

    class Config:
        from_attributes = True