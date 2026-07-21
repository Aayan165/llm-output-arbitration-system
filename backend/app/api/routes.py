from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

#Schemas
from app.schemas.request import EvaluationRequest
from app.schemas.response import EvaluationResponse
from app.schemas.evaluation import EvaluationRecord

#Database
from app.database.session import SessionLocal
from app.database.dependencies import get_db

#Evaluation
from app.services.evaluation_service import EvaluationService
from app.models.evaluation import Evaluation

#Exceptions
from app.exceptions.custom import (
    DatabaseError,
    EvaluationError,
    LLMGenerationError
)

#Workflow (langgraph)
from app.graph.workflow import build_graph

#Authentication
from app.auth.service import AuthService
from app.schemas.auth import LoginRequest, AuthResponse
from app.auth.dependencies import get_current_user

router = APIRouter()
service = EvaluationService()
auth_service = AuthService()

@router.post(
    "/login",
    response_model=AuthResponse
)
def login(data: LoginRequest):
    try:
        session = auth_service.login(
            email=data.email, 
            password=data.password
        )

        return AuthResponse(
            access_token=session.session.access_token,
            refresh_token=session.session.refresh_token,
            token_type=session.session.token_type
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post(
    "/evaluate",
    response_model=EvaluationResponse
)
def evaluate(
    data: EvaluationRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        result = service.evaluate(
            db=db,
            prompt=data.prompt,
            response=data.response,
            user_id=current_user.id
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
