from pydantic import BaseModel

class EvaluationRequest(BaseModel):
    prompt: str
    response: str
    model_name: str