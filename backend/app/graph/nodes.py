from app.graph.state import ArbitrationState
from app.agents.accuracy_agent import AccuracyAgent

accuracy_agent = AccuracyAgent()

def accuracy_node(state: ArbitrationState):
    result = accuracy_agent.evaluate(
        prompt=state["prompt"],
        response = state["response"]
    )

    return {
        "accuracy_result": result
    }