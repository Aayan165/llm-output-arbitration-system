import json
from google import genai
from google.genai.errors import ServerError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from app.utils.logger import logger
from app.exceptions.custom import LLMGenerationError

class GeminiProvider:
    def __init__(self, api_key: str, model: str):
        self.Client = genai.Client(
            api_key = api_key
        )

        self.model = model

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        retry=retry_if_exception_type(ServerError),
        reraise=True
    )
    def generate_text(self, prompt: str):
        try:
            response = self.Client.models.generate_content(
                model = self.model,
                contents = prompt
            )
            return response.text.strip()
        except ServerError:
            logger.warning("Temporary Gemini server error. Retrying...")
            raise
        except Exception as e:
            logger.exception("Gemini generation failed")
            raise LLMGenerationError(
                f"Gemini request failed: {e}"
            )

    
    def generate_json(self, prompt: str):
        text = self.generate_text(prompt)
        return json.loads(text)