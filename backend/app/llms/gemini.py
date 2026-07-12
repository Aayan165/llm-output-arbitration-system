import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

class GeminiProvider:
    def __init__(self):
        self.Client = genai.Client(
            api_key = os.getenv("GENAI_API_KEY")
        )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.5-flash"
        )

    def generate(self, prompt: str) -> str:
        response = self.Client.models.generate_content(
            model = self.model,
            contents = prompt
        )

        return response.text