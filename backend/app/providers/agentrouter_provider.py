"""
DeepSeek Provider — strong tier ke liye use hota hai.
DeepSeek OpenAI-compatible API expose karta hai.
"""

from openai import OpenAI
from app.providers.base import BaseProvider
from app.config import settings

_client = OpenAI(
    api_key=settings.deepseek_api_key,
    base_url=settings.deepseek_base_url,
)


class DeepSeekProvider(BaseProvider):
    def call(self, model_id: str, prompt: str, max_tokens: int = 512) -> dict:
        response = _client.chat.completions.create(
            model=model_id,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )

        return {
            "text": response.choices[0].message.content,
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
        }
