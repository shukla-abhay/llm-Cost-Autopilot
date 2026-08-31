# Stage 4 — Model Registry + Cost Engine

## Kya banaya

- `models/registry.py` — `MODEL_REGISTRY` dictionary jisme do entries
  hain: `"cheap"` aur `"strong"`. Har entry mein:
  - `provider` — provider ka instance (`GeminiProvider()` ya
    `AgentRouterProvider()`)
  - `provider_name` — readable naam ("gemini" / "agentrouter")
  - `model_id` — actual model string jo API ko bhejna hai
  - `input_price_per_million` / `output_price_per_million` — pricing
    (USD per 1M tokens)
  - `is_free_tier` — flag ki abhi actual billing free hai ya nahi

- `get_tier_config(tier)` — ek tier ka poora config nikalta hai
- `calculate_cost(tier, input_tokens, output_tokens)` — token count
  se estimated USD cost calculate karta hai

## Kyun ye "sabse important config file" hai

Ye file **decide karti hai ki "cheap" ka matlab kya hai**. Router ya
koi aur module kabhi ye nahi sochega "Gemini use karu ya AgentRouter"
— wo bas bolega `tier="cheap"`, aur registry resolve kar degi ki
iska matlab abhi Gemini Flash hai.

Agar kal ko "cheap" tier ka provider badalna ho (jaise Gemini ki
jagah Groq), to **sirf is file mein 3-4 lines change** karni hongi.
Poora router, evaluator, API — kuch bhi touch nahi hoga.

## Cost calculation ka logic

```
cost = (input_tokens / 1,000,000) × input_price
     + (output_tokens / 1,000,000) × output_price
```

Ye standard industry practice hai — LLM providers isi tarah bill
karte hain (input aur output tokens alag rates pe, output usually
zyada mehenga).

## Important: "hypothetical cost" tracking

Chunki humare dono providers abhi **free** hain (Gemini free tier,
AgentRouter free credits), actual billing $0 hai. Lekin humne registry
mein phir bhi **estimated paid pricing** rakha hai, taaki:

- Cost-savings metric meaningful rahe ("agar paid hote to itna lagta")
- Kal ko agar free credits khatam ho jaayein aur paid pe switch karna
  pade, to numbers already realistic hain

## Test kaise kiya

`models/interface.py` ke test run mein hi verify hua — dono tiers ke
liye `estimated_cost_usd` sahi calculate ho raha tha (chhoti values,
jaise $0.0001 se $0.001 ke beech, jo expected hai chhote test prompts
ke liye).

## Status
✅ Complete
