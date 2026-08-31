# Stage 3 — Unified Model Interface

## Kya banaya

- `models/schemas.py` — `ModelResponse` Pydantic model. Iske fields:
  `text`, `provider`, `model_id`, `tier`, `input_tokens`,
  `output_tokens`, `estimated_cost_usd`. **Har provider ka response
  isi exact format mein aata hai**, chahe neeche Gemini ho ya
  AgentRouter.
- `models/interface.py` — `call_model(prompt, tier, max_tokens)`
  function. Ye poore project ka **single entry point** hai model se
  baat karne ke liye.

## Kyun ye layer zaroori hai

Bina is layer ke, agar router ya evaluator ko seedha
`GeminiProvider` ya `AgentRouterProvider` import karna padta, to:
- Har jagah `if tier == "cheap": use gemini else use agentrouter`
  jaisa duplicate logic likhna padta
- Provider switch karne pe (jaisa humne 3 baar kiya — Bedrock →
  Anthropic → Gemini/AgentRouter) **poore codebase mein jagah-jagah
  changes** karne padte

Is layer ki wajah se sirf **ek jagah** (`registry.py`, Stage 4 dekho)
change karni padti hai, aur `call_model()` ka signature kabhi nahi
badalta:

```python
from app.models.interface import call_model

result = call_model("your prompt here", tier="cheap")
print(result.text)
print(result.estimated_cost_usd)
```

## Test kaise kiya

```bash
python -m app.models.interface
```

Dono tiers (`cheap` aur `strong`) ko ek hi run mein test kiya —
dono se response, token count, aur estimated cost print hua.

## Status
✅ Complete
