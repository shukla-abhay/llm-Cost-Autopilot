"""
Gemini Provider — cheap tier ke liye use hota hai (Gemini Flash, free).
"""

from google import genai
from app.providers.base import BaseProvider
from app.config import settings

_client = genai.Client(api_key=settings.gemini_api_key)


class GeminiProvider(BaseProvider):
    def call(self, model_id: str, prompt: str, max_tokens: int = 512) -> dict:
        response = _client.models.generate_content(
            model=model_id,
            contents=prompt,
        )

        usage = response.usage_metadata

        return {
            "text": response.text,
            "input_tokens": usage.prompt_token_count,
            "output_tokens": usage.candidates_token_count,
        }
