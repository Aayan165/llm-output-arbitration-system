from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.models.evaluation import Evaluation
from app.repositories.evaluation_repository import EvaluationRepository

engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

def test_repository():
    db = TestingSessionLocal()

    repository = EvaluationRepository()

    evaluation = Evaluation(
        prompt="Name three planets",
        response="Earth, Mars, Jupiter",
        accuracy_score=10,
        logic_score=9,
        completeness_score=10,
        overall_score=9.67,
        verdict="Excellent",
        summary="Very good response."
    )

    repository.save(db, evaluation)

    all_records = repository.get_all(db)

    assert len(all_records) == 1

    record = repository.get_by_id(db, evaluation.id)

    assert record.prompt == "Name three planets"
    assert record.verdict == "Excellent"

    db.close()
