from sqlalchemy.orm import Session

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
        db: Session
    ):
        return db.query(Evaluation).all()

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