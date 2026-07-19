from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from app.schemas.request import EvaluationRequest
from app.schemas.response import EvaluationResponse
from app.services.evaluation_service import EvaluationService
from app.database.session import SessionLocal
from app.models.evaluation import Evaluation
from app.schemas.evaluation import EvaluationRecord
from app.exceptions.custom import (
    DatabaseError,
    EvaluationError,
    LLMGenerationError
)
from app.database.dependencies import get_db

from app.graph.workflow import build_graph

router = APIRouter()
service = EvaluationService()

@router.post(
    "/evaluate",
    response_model=EvaluationResponse
)
def evaluate(
    data: EvaluationRequest,
    db: Session = Depends(get_db)
):
    try:
        result = service.evaluate(
            db=db,
            prompt=data.prompt,
            response=data.response
        )

        return EvaluationResponse(
            result = result
        )
    
    except LLMGenerationError as e:
        raise HTTPException(status_code=503, detail=str(e))
    
    except EvaluationError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected Server error.")


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
def get_evaluations(
    db: Session = Depends(get_db)
):
    return service.repository.get_all(db)

@router.get(
    "/evaluations/{evaluation_id}",
    response_model=EvaluationRecord
)
def get_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db)    
):
    return service.repository.get_by_id(db, evaluation_id)
