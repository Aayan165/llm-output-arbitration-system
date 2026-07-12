from app.llms.gemini import GeminiProvider

provider = GeminiProvider()

response = provider.generate("Explain why the sky is blue in 1 sentence.")

print(response)