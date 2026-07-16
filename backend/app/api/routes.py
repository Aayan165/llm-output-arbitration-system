from fastapi import APIRouter
from fastapi import HTTPException

from app.schemas.request import EvaluationRequest
from app.schemas.response import EvaluationResponse

from app.graph.workflow import build_graph

router = APIRouter()
graph = build_graph()

@router.post(
    "/evaluate",
    response_model=EvaluationResponse
)
def evaluate(data: EvaluationRequest):
    try:
        result = graph.invoke(
            {
                "prompt": data.prompt,
                "response": data.response
            }
        )

        return EvaluationResponse(
            result = result["final_verdict"]
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