"""
Unified Model Interface — poore app mein SIRF is function ko call
karna hai model se baat karne ke liye. Router, evaluator, API routes —
sabko sirf itna pata hoga: "cheap" ya "strong" tier bolo, jawab milega.

Provider kaunsa hai, model ID kya hai — sab registry.py se resolve
hota hai. Isi abstraction ki wajah se hum providers switch kar paaye
(Bedrock -> Anthropic -> Gemini -> AgentRouter) bina baaki code
touch kiye.
"""

from app.models.registry import get_tier_config, calculate_cost
from app.models.schemas import ModelResponse


def call_model(prompt: str, tier: str = "cheap", max_tokens: int = 512) -> ModelResponse:
    """
    prompt: user ka sawaal / instruction
    tier: "cheap" (Gemini Flash, free) ya "strong" (AgentRouter claude-opus-4-8)
    """
    config = get_tier_config(tier)
    provider = config["provider"]
    model_id = config["model_id"]

    result = provider.call(model_id, prompt, max_tokens)

    cost = calculate_cost(tier, result["input_tokens"], result["output_tokens"])

    return ModelResponse(
        text=result["text"],
        provider=config["provider_name"],
        model_id=model_id,
        tier=tier,
        input_tokens=result["input_tokens"],
        output_tokens=result["output_tokens"],
        estimated_cost_usd=cost,
    )


if __name__ == "__main__":
    # Test: python -m app.models.interface
    question = "What is machine learning? Answer in 2 lines."

    print("=== CHEAP TIER (Gemini Flash) ===")
    print(f"Prompt: {question}\n")
    result = call_model(question, tier="cheap")
    print(f"Response: {result.text}")
    print(f"Provider: {result.provider} | Model: {result.model_id}")
    print(f"Tokens: {result.input_tokens} in / {result.output_tokens} out")
    print(f"Estimated cost: ${result.estimated_cost_usd}\n")

    print("=== STRONG TIER (AgentRouter claude-opus-4-8) ===")
    print(f"Prompt: {question}\n")
    result = call_model(question, tier="strong")
    print(f"Response: {result.text}")
    print(f"Provider: {result.provider} | Model: {result.model_id}")
    print(f"Tokens: {result.input_tokens} in / {result.output_tokens} out")
    print(f"Estimated cost: ${result.estimated_cost_usd}")
