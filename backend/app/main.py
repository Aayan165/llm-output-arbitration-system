from fastapi import FastAPI

#API
from app.api.routes import router

#Databases
from app.database.session import Base, engine

#Models
from app.models.evaluation import Evaluation
from app.models.experiment import Experiment

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "LLM Output Arbitrator",
    version = "1.0.0",
)

app.include_router(router)