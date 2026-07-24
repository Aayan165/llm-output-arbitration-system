from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.evaluation import Evaluation

class EvaluationRepository:
    def save(
        self,
        db: Session,
        evaluation: Evaluation
    ) -> Evaluation:
        
        db.add(evaluation)
        db.commit()
        db.refresh(evaluation)
        return evaluation
    
    def get_all(
        self,
        db: Session,
        user_id: str,
        verdict: str | None = None,
        experiment_id: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        query = (
            db.query(Evaluation)
            .filter(Evaluation.user_id == user_id)
        )

        if verdict:
            query = query.filter(
                Evaluation.verdict == verdict
            )

        if experiment_id:
            query = query.filter(
                Evaluation.experiment_id == experiment_id
            )

        return (
            query.
            order_by(Evaluation.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

    def get_by_id(
            self,
            db: Session,
            evaluation_id: int
    ):
        return (
            db.query(Evaluation)
            .filter(Evaluation.id == evaluation_id)
            .first()
        )
    
    def get_user_evaluations(
        self,
        db: Session,
        user_id: str
    ):
        return (
            db.query(Evaluation)
            .filter(Evaluation.user_id == user_id)
            .order_by(Evaluation.created_at.desc())
            .all()
        )
    
    def get_evaluation(
        self,
        db: Session,
        evaluation_id: int,
        user_id: str
    ):
        return (
            db.query(Evaluation)
            .filter(Evaluation.id == evaluation_id, Evaluation.user_id == user_id)
            .first()
        )

    def get_user_analytics(
        self,
        db: Session,
        user_id: str
    ):
        total = (
            db.query(Evaluation)
            .filter(Evaluation.user_id == user_id)
            .count()
        )

        averages = (
            db.query(
                func.avg(Evaluation.overall_score),
                func.avg(Evaluation.accuracy_score),
                func.avg(Evaluation.logic_score),
                func.avg(Evaluation.completeness_score)
            )
            .filter(Evaluation.user_id == user_id)
            .first()
        )

        verdicts = (
            db.query(
                Evaluation.verdict,
                func.count(Evaluation.id)
            )
            .filter(Evaluation.user_id == user_id)
            .group_by(Evaluation.verdict)
            .all()
        )

        return {
            "total": total,
            "averages": averages,
            "verdicts": verdicts
        }

    def get_model_comparison(
        self,
        db: Session,
        user_id: str
    ):
        return (
            db.query(Evaluation)
            .filter(Evaluation.user_id == user_id)
            .order_by(Evaluation.created_at.desc())
            .all()
        )

    def get_prompt_experiments(
        self,
        db: Session,
        user_id: str
    ):
        return (
            db.query(Evaluation)
            .filter(Evaluation.user_id == user_id)
            .order_by(Evaluation.created_at.desc())
            .all()
        )

    def get_by_experiment(
        self,
        db: Session,
        experiment_id: int,
        user_id: str
    ):
        return (
            db.query(Evaluation)
            .filter(
                Evaluation.user_id == user_id,
                Evaluation.experiment_id == experiment_id
            )
            .order_by(Evaluation.created_at.desc())
            .all()
        )

    def export(
        self,
        db: Session,
        user_id: str
    ):
        return (
            db.query(Evaluation)
            .filter(Evaluation.user_id == user_id)
            .order_by(Evaluation.created_at.desc())
            .all()
        )
