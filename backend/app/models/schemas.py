"""
Har provider (Gemini ho ya AgentRouter) ka response is SAME format
mein aayega. Isi consistency ki wajah se router, evaluator, cost engine
kisiko fark nahi padta ki neeche kaunsa provider chal raha hai.
"""

from pydantic import BaseModel


class ModelResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    text: str                 # model ka jawab
    provider: str              # "gemini" ya "agentrouter"
    model_id: str              # actual model ID jo call hua
    tier: str                  # "cheap" ya "strong"
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float
