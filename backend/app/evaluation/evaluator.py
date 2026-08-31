"""
Quality Evaluator — response ki quality check karta hai.
Agar cheap tier ka response bekar hai → strong tier pe escalate karta hai.
"""

from app.models.schemas import ModelResponse
from app.models.interface import call_model

FAILURE_PHRASES = [
    "i don't know", "i do not know", "i'm not sure", "i am not sure",
    "cannot answer", "can't answer", "unable to", "i apologize",
    "as an ai", "i cannot", "i can't",
]

MIN_RESPONSE_LENGTH = 20


def is_quality_ok(response: ModelResponse) -> tuple[bool, str]:
    text = response.text.strip().lower()

    if len(text) < MIN_RESPONSE_LENGTH:
        return False, "response too short"

    for phrase in FAILURE_PHRASES:
        if phrase in text:
            return False, f"failure phrase detected: '{phrase}'"

    return True, "ok"


def evaluate_and_escalate(prompt: str, response: ModelResponse) -> ModelResponse:
    ok, reason = is_quality_ok(response)

    if ok:
        print(f"[EVALUATOR] quality=ok tier={response.tier}")
        return response

    print(f"[EVALUATOR] quality=bad reason='{reason}' → escalating to strong tier")
    escalated = call_model(prompt, tier="strong")
    escalated_ok, _ = is_quality_ok(escalated)
    print(f"[EVALUATOR] escalated quality={'ok' if escalated_ok else 'bad'}")
    return escalated


if __name__ == "__main__":
    from app.models.interface import call_model

    tests = [
        ("What is the capital of France?", "cheap"),
        ("Design a scalable microservices architecture for 1 million users.", "cheap"),
    ]

    for prompt, tier in tests:
        print(f"\nPrompt: {prompt}")
        response = call_model(prompt, tier=tier)
        final = evaluate_and_escalate(prompt, response)
        print(f"Final tier: {final.tier} | Model: {final.model_id}")
        print(f"Response: {final.text[:100]}")
