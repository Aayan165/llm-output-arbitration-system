from typing import Optional, Dict, Any
from typing_extensions import TypedDict

from app.schemas.critic import CriticResult, FinalVerdict

class ArbitrationState(TypedDict):
    """
    Shared state passed between every LangGraph node.
    """

    #User input
    prompt: str
    response: str

    #Critics results
    accuracy_result: Optional[CriticResult]
    logic_result: Optional[CriticResult]
    completeness_result: Optional[CriticResult]

    #Final answer
    final_verdict: Optional[FinalVerdict]