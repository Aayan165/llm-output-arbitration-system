from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.experiment import Experiment

class ExperimentRepository:
    def save(
        self,
        db: Session,
        experiment: Experiment
    ):
        db.add(experiment)
        db.commit()
        db.refresh(experiment)

        return experiment

    def get_all(
        self,
        db: Session,
        user_id: str
    ):
        return (
            db.query(Experiment)
            .filter(Experiment.user_id == user_id)
            .order_by(Experiment.created_at.desc())
            .all()
        )

    def get_by_id(
            self,
            db: Session,
            experiment_id: int,
            user_id: str
    ):
        return (
            db.query(Experiment)
            .filter(
                Experiment.id == experiment_id,
                Experiment.user_id == user_id
            )
            .first()
        )

    def delete(
        self,
        db: Session,
        experiment: Experiment
    ):
        db.delete(experiment)
        db.commit()