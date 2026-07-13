import json
from google import genai

class GeminiProvider:
    def __init__(self, api_key: str, model: str):
        self.Client = genai.Client(
            api_key = api_key
        )

        self.model = model

    def generate_text(self, prompt: str):
        response = self.Client.models.generate_content(
            model = self.model,
            contents = prompt
        )

        return response.text.strip()
    
    def generate_json(self, prompt: str):
        text = self.generate_text(prompt)
        return json.loads(text)