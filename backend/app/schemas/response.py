from pydantic import BaseModel
from app.schemas.verdict import FinalVerdict

class EvaluationResponse(BaseModel):
    result: FinalVerdict