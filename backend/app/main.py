from fastapi import FastAPI

from app.api.routes import router
from app.database.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "LLM Output Arbitrator",
    version = "1.0.0",
)

app.include_router(router)