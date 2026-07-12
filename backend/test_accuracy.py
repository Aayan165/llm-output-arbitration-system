from app.agents.accuracy_agent import AccuracyAgent


agent = AccuracyAgent()

result = agent.evaluate(
    prompt="What is the capital of France?",
    response="The capital of France is Berlin."
)

print(result)