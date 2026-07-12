from app.agents.completeness_agent import CompletenessAgent

agent = CompletenessAgent()

result = agent.evaluate(
    prompt="Name three planets in our solar system.",
    response="Earth and Mars."
)

print(result)