from fastapi import APIRouter
from fastapi import HTTPException

from app.schemas.request import EvaluationRequest
from app.schemas.response import EvaluationResponse
from app.services.evaluation_service import EvaluationService
from app.database.session import SessionLocal
from app.models.evaluation import Evaluation
from app.schemas.evaluation import EvaluationRecord

from app.graph.workflow import build_graph

router = APIRouter()
service = EvaluationService()

@router.post(
    "/evaluate",
    response_model=EvaluationResponse
)
def evaluate(data: EvaluationRequest):
    try:
        result = service.evaluate(
            prompt=data.prompt,
            response=data.response
        )

        return EvaluationResponse(
            result = result
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def home():
    return {
        "message": "LLM Output Arbitrator API is running"
    }

@router.get("/health")
def health():
    return {
        "status": "healthy"
    }

@router.get(
    "/evaluations",
    response_model=list[EvaluationRecord]
)
def get_evaluations():
    db = SessionLocal()
    evaluations = db.query(Evaluation).all()
    db.close()

    return evaluations

@router.get(
    "/evaluations/{evaluation_id}",
    response_model=EvaluationRecord
)
def get_evaluation(evaluation_id: int):
    db = SessionLocal()
    evaluation = (
        db.query(Evaluation)
        .filter(Evaluation.id == evaluation_id)
        .first()
    )
    db.close()

    return evaluation