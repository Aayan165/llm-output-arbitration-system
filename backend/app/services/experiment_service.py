from sqlalchemy.orm import Session

#Models
from app.models.experiment import Experiment

#Repositories
from app.repositories.experiment_repository import ExperimentRepository

class ExperimentService:
    def __init__(self):
        self.repository = ExperimentRepository()

    def create_experiment(
        self,
        db: Session,
        user_id: str,
        name: str,
        description: str | None
    ):
        experiment = Experiment(
            user_id=user_id,
            name=name,
            description=description
        )

        return self.repository.save(
            db,
            experiment
        )

    def get_user_experiments(
        self,
        db: Session,
        user_id: str
    ):
        return self.repository.get_all(
            db,
            user_id
        )

    def get_experiment(
        self,
        db: Session,
        experiment_id: int,
        user_id: str
    ):
        return self.repository.get_by_id(
            db,
            experiment_id,
            user_id
        )

    def delete_experiment(
        self,
        db: Session,
        experiment_id: int,
        user_id: str
    ):
        experiment = self.repository.get_by_id(
            db,
            experiment_id,
            user_id
        )

        if experiment is None:
            return None

        self.repository.delete(
            db,
            experiment
        )

        return experiment
    