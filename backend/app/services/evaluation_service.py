from app.graph.workflow import build_graph
from app.database.session import SessionLocal
from app.models.evaluation import Evaluation

class EvaluationService:
    def __init__(self):
        self.graph = build_graph()

    def evaluate(
        self,
        prompt: str,
        response: str
    ):
        result =  self.graph.invoke(
            {
                "prompt": prompt,
                "response": response
            }
        )

        verdict = result["final_verdict"]

        db = SessionLocal()

        evaluation = Evaluation(
            prompt=prompt,
            response=response,
            accuracy_score=result["accuracy_result"].score,
            logic_score=result["logic_result"].score,
            completeness_score=result["completeness_result"].score,
            overall_score=verdict.overall_score,
            verdict=verdict.verdict,
            summary=verdict.summary
        )

        db.add(evaluation)
        db.commit()
        db.refresh(evaluation)
        db.close()

        return verdict