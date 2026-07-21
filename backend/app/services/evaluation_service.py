from sqlalchemy.orm import Session

#Workflow (langgraph)
from app.graph.workflow import build_graph

#Repository
from app.repositories.evaluation_repository import EvaluationRepository

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

    def evaluate(
        self,
        db: Session,
        prompt: str,
        response: str,
        user_id: str
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

        # db = SessionLocal()

        evaluation = Evaluation(
            user_id=user_id,
            prompt=prompt,
            response=response,
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