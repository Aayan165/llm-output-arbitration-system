from fastapi import FastAPI

app = FastAPI(
    title = "LLM Output Arbitration System",
    version = "1.0.0",
)

app.get("/")
def root():
    return {"message": "LLM Output Arbitration System API"}