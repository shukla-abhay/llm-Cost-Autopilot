"""
Intelligent Router — classifier ka output lekar tier decide karta hai.
easy/medium → cheap (Gemini Flash)
hard → strong (Gemini Pro)
"""

from app.router.classifier import predict
from app.models.interface import call_model
from app.models.schemas import ModelResponse
from app.evaluation.evaluator import evaluate_and_escalate


def route(prompt: str) -> ModelResponse:
    result = predict(prompt)
    complexity = result["complexity"]
    confidence = result["confidence"]

    tier = "strong" if complexity == "hard" else "cheap"

    print(f"[ROUTER] complexity={complexity} confidence={confidence} → tier={tier}")

    response = call_model(prompt, tier=tier)
    return evaluate_and_escalate(prompt, response)


if __name__ == "__main__":
    import time
    tests = [
        "What is the capital of France?",
        "Write a Python function to check if a number is prime.",
        "Analyze and compare TCP vs UDP with trade-offs.",
    ]

    for prompt in tests:
        print(f"\nPrompt: {prompt}")
        response = route(prompt)
        print(f"Tier: {response.tier} | Model: {response.model_id}")
        print(f"Response: {response.text[:100]}")
        print(f"Cost: ${response.estimated_cost_usd}")
        time.sleep(3)
