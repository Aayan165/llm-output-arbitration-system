import os
from dotenv import load_dotenv
from app.llms.gemini import GeminiProvider

load_dotenv()

accuracy_provider = GeminiProvider(
    api_key=os.getenv("GEMINI_KEY_1"),
    model=os.getenv("GEMINI_MODEL_1")
)
logic_provider = GeminiProvider(
    api_key=os.getenv("GEMINI_KEY_2"),
    model=os.getenv("GEMINI_MODEL_2")
)
completeness_provider = GeminiProvider(
    api_key=os.getenv("GEMINI_KEY_3"),
    model=os.getenv("GEMINI_MODEL_3")
)
adjudicator_provider = GeminiProvider(
    api_key=os.getenv("GEMINI_KEY_1"),
    model=os.getenv("GEMINI_MODEL_1")
)