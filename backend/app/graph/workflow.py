from langgraph.graph import StateGraph, START, END
from app.graph.state import ArbitrationState
from app.graph.nodes import (
    accuracy_node,
    logic_node,
    completeness_node
)

def build_graph():
    builder = StateGraph(ArbitrationState)

    builder.add_node("accuracy", accuracy_node)
    builder.add_node("logic", logic_node)
    builder.add_node("completeness", completeness_node)

    builder.add_edge(START, "accuracy")
    builder.add_edge(START, "logic")
    builder.add_edge(START, "completeness")
    builder.add_edge("accuracy", END)
    builder.add_edge("logic", END)
    builder.add_edge("completeness", END)

    # builder.add_edge(START, "accuracy")
    # builder.add_edge("accuracy", "logic")
    # builder.add_edge("logic", "completeness")
    # builder.add_edge("completeness", END)

    return builder.compile()