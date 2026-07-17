from app.graph.workflow import build_graph

class EvaluationService:
    def __init__(self):
        self.graph = build_graph()

    def evaluate(self, prompt: str, response: str):
        result =  self.graph.invoke(
            {
                "prompt": prompt,
                "response": response
            }
        )

        return result["final_verdict"]