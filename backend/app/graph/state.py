from typing import Optional, Dict, Any
from typing_extensions import TypedDict

from app.schemas.critic import CriticResult
from app.schemas.verdict import FinalVerdict

class ArbitrationState(TypedDict):
    #User input
    prompt: str
    response: str

    #Critics results
    accuracy_result: CriticResult
    logic_result: CriticResult
    completeness_result: CriticResult

    #Final answer
    final_verdict: FinalVerdict