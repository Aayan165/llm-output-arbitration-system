from app.graph.workflow import build_graph

graph = build_graph()

result = graph.invoke(
    {

        "prompt": "Name three planets.",

        "response": "Earth and Mars."

    }
)

print(result)