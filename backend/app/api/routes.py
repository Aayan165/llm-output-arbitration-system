from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from fastapi import Query
from sqlalchemy.orm import Session

#Schemas
from app.schemas.request import EvaluationRequest
from app.schemas.response import EvaluationResponse
from app.schemas.evaluation import EvaluationRecord
from app.schemas.analytics import AnalyticsResponse
from app.schemas.model_comparision import ModelComparison
from app.schemas.experiment import (
    ExperimentCreate,
    ExperimentResponse
)

#Database
from app.database.session import SessionLocal
from app.database.dependencies import get_db

#Models
from app.models.evaluation import Evaluation

#Exceptions
from app.exceptions.custom import (
    DatabaseError,
    EvaluationError,
    LLMGenerationError
)

#Serivices
from app.services.evaluation_service import EvaluationService
from app.services.experiment_service import ExperimentService

#Workflow (langgraph)
from app.graph.workflow import build_graph

#Authentication
from app.auth.service import AuthService
from app.schemas.auth import LoginRequest, AuthResponse
from app.auth.dependencies import get_current_user

#===============================================================================

router = APIRouter()
service = EvaluationService()
experiment_service = ExperimentService()
auth_service = AuthService()

#===============================================================================
#           Posts
#===============================================================================

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
            model_name=data.model_name,
            user_id=current_user.id,
            experiment_id=data.experiment_id
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


@router.post(
    "/experiments",
    response_model=ExperimentResponse
)
def create_experiment(
    data: ExperimentCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return experiment_service.create_experiment(
        db=db,
        user_id=current_user.id,
        name=data.name,
        description=data.description
    )

#===============================================================================
#           Gets
#===============================================================================

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
    "/my-evaluations",
    response_model=list[EvaluationRecord]
)
def get_my_evaluations(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return service.get_user_evaluations(
        db=db,
        user_id=current_user.id
    )


@router.get(
    "/my-evaluations/{evaluation_id}",
    response_model=EvaluationRecord
)
def get_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)    
):
    evaluation = service.get_evaluation(
        db=db,
        evaluation_id=evaluation_id,
        user_id=current_user.id
    )
    if evaluation is None:
        raise HTTPException(
            status_code=404,
            detail="Evaluation not Found."
        )
    return evaluation

@router.get(
    "/analytics",
    response_model=AnalyticsResponse
)
def get_analytics(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return service.get_user_analytics(
        db=db,
        user_id=current_user.id
    )


@router.get(
    "/model-comparison",
    response_model=list[ModelComparison]
)
def get_model_comparison(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return service.get_model_comparison(
        db=db,
        user_id=current_user.id
    )

@router.get(
    "/experiments",
    response_model=list[ExperimentResponse]
)
def get_experiments(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return experiment_service.get_user_experiments(
        db,
        current_user.id
    )

@router.get(
    "/experiments/{experiment_id}",
    response_model=ExperimentResponse
)
def get_experiment(
    experiment_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    experiment = experiment_service.get_experiment(
        db=db,
        experiment_id=experiment_id,
        user_id=current_user.id
    )

    if experiment is None:
        raise HTTPException(
            status_code=404,
            detail="Experiment not Found."
        )

    return experiment

@router.get(
    "/experiments/{experiment_id}/evaluations",
    response_model=list[EvaluationRecord]
)
def get_experiment_evaluations(
    experiment_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    experiment = experiment_service.get_experiment(
        db=db,
        experiment_id=experiment_id,
        user_id=current_user.id
    )
    if experiment is None:
        raise HTTPException(
            status_code=404,
            detail="Experiment not Found."
        )

    return service.repository.get_by_experiment(
        db,
        experiment_id,
        current_user.id
    )

@router.get(
    "/evaluations",
    response_model=list[EvaluationRecord]
)
def get_evaluations(
    verdict: str | None = Query(None),
    experiment_id: int | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return service.get_evaluations(
        db=db,
        user_id=current_user.id,
        verdict=verdict,
        experiment_id=experiment_id,
        page=page,
        limit=limit
    )

#===============================================================================
#           Deletes
#===============================================================================

@router.delete(
    "/experiments/{experiment_id}"
)
def delete_experiment(
    experiment_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    experiment = experiment_service.delete_experiment(
        db=db,
        experiment_id=experiment_id,
        user_id=current_user.id
    )

    if experiment is None:
        raise HTTPException(
            status_code=404,
            detail="Experiment not found."
        )

    return {
        "message": "Experiment deleted successfully."
    }