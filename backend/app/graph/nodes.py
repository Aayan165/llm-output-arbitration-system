from app.graph.state import ArbitrationState
from app.agents.accuracy_agent import AccuracyAgent
from app.agents.logic_agent import LogicAgent
from app.agents.completeness_agent import CompletenessAgent
from app.config.llm_factory import (
    accuracy_provider,
    logic_provider,
    completeness_provider
)

accuracy_agent = AccuracyAgent(accuracy_provider)
logic_agent = LogicAgent(logic_provider)
completeness_agent = CompletenessAgent(completeness_provider)

def accuracy_node(state: ArbitrationState):
    result = accuracy_agent.evaluate(
        prompt=state["prompt"],
        response = state["response"]
    )

    return {
        "accuracy_result": result
    }

def logic_node(state: ArbitrationState):
    result = logic_agent.evaluate(
        prompt=state["prompt"],
        response = state["response"]
    )

    return {
        "logic_result": result
    }

def completeness_node(state: ArbitrationState):
    result = completeness_agent.evaluate(
        prompt=state["prompt"],
        response = state["response"]
    )

    return {
        "completeness_result": result
    }