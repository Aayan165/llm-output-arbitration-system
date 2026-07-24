#Libraries
from sqlalchemy.orm import Session
import csv
import io

#Workflow (langgraph)
from app.graph.workflow import build_graph

#Repository
from app.repositories.evaluation_repository import EvaluationRepository
from app.repositories.experiment_repository import ExperimentRepository

#Evaluation
from app.models.evaluation import Evaluation

#Logging
from app.utils.logger import logger
from app.utils.timer import Timer

#Exceptions
from app.exceptions.custom import DatabaseError, EvaluationError

class EvaluationService:
    def __init__(self):
        self.graph = build_graph()
        self.repository = EvaluationRepository()
        self.experiment_repository = ExperimentRepository()

    def evaluate(
        self,
        db: Session,
        prompt: str,
        response: str,
        model_name: str,
        user_id: str,
        experiment_id: int | None = None
    ):
        timer = Timer()
        timer.start()
        logger.info("Evaluation started")

        try:
            result =  self.graph.invoke(
                {
                    "prompt": prompt,
                    "response": response
                }
            )
        except Exception as e:
            logger.exception("Evaluation pipeline failed")

            raise EvaluationError(f"Evaluation pipeline error: {e}")

        logger.info("LangGraph execution completed")

        verdict = result["final_verdict"]

        if experiment_id is not None:
            experiment = self.experiment_repository.get_by_id(
                db,
                experiment_id,
                user_id
            )
            if experiment is None:
                raise EvaluationError(
                    "Experiment not found."
                )

        evaluation = Evaluation(
            user_id=user_id,
            experiment_id=experiment_id,
            prompt=prompt,
            response=response,
            model_name=model_name,
            accuracy_score=result["accuracy_result"].score,
            logic_score=result["logic_result"].score,
            completeness_score=result["completeness_result"].score,
            overall_score=verdict.overall_score,
            verdict=verdict.verdict,
            summary=verdict.summary
        )

        self.repository.save(db, evaluation)

        elapsed = timer.stop()

        logger.info(
            "Evaluation completed in %.3f seconds",
            elapsed
        )

        return verdict
    
    def get_user_evaluations(
        self,
        db: Session,
        user_id: str
    ):
        return self.repository.get_user_evaluations(
            db=db,
            user_id=user_id
        )


    def get_evaluation(
        self,
        db: Session,
        evaluation_id: int,
        user_id: str
    ):
        return self.repository.get_evaluation(
            db=db,
            evaluation_id=evaluation_id,
            user_id=user_id
        )

    def get_user_analytics(
        self,
        db: Session,
        user_id: str
    ):
        analytics = self.repository.get_user_analytics(
            db=db,
            user_id=user_id
        )
        overall, accuracy, logic, completeness = analytics["averages"]

        return {
            "total_evaluations": analytics["total"],
            "average_overall_score": round(overall or 0, 2),
            "average_accuracy_score": round(accuracy or 0, 2),
            "average_logic_score": round(logic or 0, 2),
            "average_completeness_score": round(completeness or 0, 2),
            "verdict_distribution": {
                verdict: count
                for verdict, count in analytics["verdicts"]
            }
        }

    def get_model_comparison(
        self,
        db: Session,
        user_id: str
    ):
        evaluations = self.repository.get_model_comparison(
            db=db,
            user_id=user_id
        )

        return [
            {
                "model_name": e.model_name,
                "overall_score": e.overall_score,
                "accuracy_score": e.accuracy_score,
                "logic_score": e.logic_score,
                "completeness_score": e.completeness_score,
                "verdict": e.verdict,
                "created_at": e.created_at
            }
            for e in evaluations
        ]

    def get_prompt_experiments(
        self,
        db: Session,
        user_id: str
    ):
        return self.repository.get_prompt_experiments(
            db,
            user_id
        )

    def get_evaluations(
        self,
        db: Session,
        user_id: str,
        verdict: str | None = None,
        experiment_id: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        return self.repository.get_all(
            db=db,
            user_id=user_id,
            verdict=verdict,
            experiment_id=experiment_id,
            page=page,
            limit=limit
        )

    def export_csv(
        self,
        db: Session,
        user_id: str
    ):
        evaluations = self.repository.export(
            db,
            user_id
        )

        output = io.StringIO()

        writer = csv.writer(output)

        writer.writerow([
            "Model",
            "Prompt",
            "Response",
            "Accuracy",
            "Logic",
            "Completeness",
            "Overall",
            "Verdict",
            "Summary",
            "Experiment",
            "Created At"
        ])

        for evaluation in evaluations:
            writer.writerow([
            evaluation.model_name,
            evaluation.prompt,
            evaluation.response,
            evaluation.accuracy_score,
            evaluation.logic_score,
            evaluation.completeness_score,
            evaluation.overall_score,
            evaluation.verdict,
            evaluation.summary,
            evaluation.experiment_id,
            evaluation.created_at
        ])

        return output.getvalue()