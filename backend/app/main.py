from fastapi import FastAPI

from app.api.routes import router
from app.database.session import Base, engine
from app.models.evaluation import Evaluation

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "LLM Output Arbitrator",
    version = "1.0.0",
)

app.include_router(router)