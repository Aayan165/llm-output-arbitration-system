from pydantic import BaseModel

class EvaluationRequest(BaseModel):
    experiment_id: int | None = None
    prompt: str
    response: str
    model_name: str