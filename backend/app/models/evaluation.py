from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime

from app.database.database import Base

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    accuracy_score = Column(Float)
    logic_score = Column(Float)
    completeness_score = Column(Float)
    overall_score = Column(Float)
    verdict = Column(String)
    summary = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )