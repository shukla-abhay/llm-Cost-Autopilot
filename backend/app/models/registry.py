"""
Model Registry — sabse important config file.

Ye decide karta hai ki "cheap" tier ka matlab exactly kaunsa
provider + model hai, aur "strong" tier ka kya. Router sirf itna
kahega "mujhe cheap chahiye" ya "mujhe strong chahiye" — baaki
sab yahan se resolve hota hai.

Naya provider/model add ya switch karna ho, to SIRF yahan change
karo — router, evaluator, cost engine kuch bhi touch nahi karna padega.
"""

from app.providers.gemini_provider import GeminiProvider
from app.providers.agentrouter_provider import DeepSeekProvider
from app.config import settings

_gemini = GeminiProvider()
_deepseek = DeepSeekProvider()

MODEL_REGISTRY = {
    "cheap": {
        "provider": _gemini,
        "provider_name": "gemini",
        "model_id": settings.gemini_flash_model,
        "input_price_per_million": 0.30,
        "output_price_per_million": 2.50,
        "is_free_tier": True,
    },
    "strong": {
        "provider": _deepseek,
        "provider_name": "deepseek",
        "model_id": settings.deepseek_strong_model,
        "input_price_per_million": 0.27,
        "output_price_per_million": 1.10,
        "is_free_tier": False,
    },
}


def get_tier_config(tier: str) -> dict:
    """tier: 'cheap' ya 'strong'"""
    if tier not in MODEL_REGISTRY:
        raise ValueError(f"Unknown tier '{tier}'. Available: {list(MODEL_REGISTRY.keys())}")
    return MODEL_REGISTRY[tier]


def calculate_cost(tier: str, input_tokens: int, output_tokens: int) -> float:
    config = get_tier_config(tier)
    input_cost = (input_tokens / 1_000_000) * config["input_price_per_million"]
    output_cost = (output_tokens / 1_000_000) * config["output_price_per_million"]
    return round(input_cost + output_cost, 8)
