from pydantic import BaseModel

class AnalyticsResponse(BaseModel):
    total_evaluations: int
    average_overall_score: float
    average_accuracy_score: float
    average_logic_score: float
    average_completeness_score: float
    verdict_distribution: dict[str, int]