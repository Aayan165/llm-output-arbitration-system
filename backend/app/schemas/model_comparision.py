from datetime import datetime
from pydantic import BaseModel

class ModelComparison(BaseModel):
    model_name: str
    overall_score: float
    accuracy_score: float
    logic_score: float
    completeness_score: float
    verdict: str
    # summary: str
    created_at: datetime