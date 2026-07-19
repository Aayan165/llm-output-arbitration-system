from sqlalchemy.orm import Session

from app.graph.workflow import build_graph
from app.repositories.evaluation_repository import EvaluationRepository
from app.models.evaluation import Evaluation
from app.utils.logger import logger
from app.utils.timer import Timer
from app.exceptions.custom import DatabaseError, EvaluationError

class EvaluationService:
    def __init__(self):
        self.graph = build_graph()
        self.repository = EvaluationRepository()

    def evaluate(
        self,
        db: Session,
        prompt: str,
        response: str
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

        # try:
        #     db.add(evaluation)
        #     db.commit()
        #     db.refresh(evaluation)
        # except Exception as e:
        #     db.rollback()
        #     logger.exception("Database operation failed")

        #     raise DatabaseError(f"Database error: {e}")
        # finally:
        #     logger.info("Evaluation saved to database")
        #     db.close()

        elapsed = timer.stop()

        logger.info(
            "Evaluation completed in %.3f seconds",
            elapsed
        )

        return verdict
