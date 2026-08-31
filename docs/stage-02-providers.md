# Stage 2 — Providers (Gemini + AgentRouter)

## Background: kyun provider badle

Original plan AWS Bedrock tha, lekin payment method issue ki wajah se
access nahi mil paya. Fir socha Anthropic API seedha use karein, lekin
usme bhi payment card chahiye tha. End mein decide kiya:

- **Cheap tier** → Gemini Flash (Google AI Studio, genuinely free,
  koi card nahi chahiye)
- **Strong tier** → AgentRouter ka `claude-opus-4-8` (free credits
  wala third-party gateway)

Ye hybrid setup isliye chuna kyunki cheap tier ka **actual $0 cost**
hai, jo cost-saving story ko aur real banata hai.

## Kya banaya

- `providers/base.py` — ek abstract `BaseProvider` class, jisme ek
  hi method hai: `call(model_id, prompt, max_tokens)`. Ye har provider
  ka "contract" hai.
- `providers/gemini_provider.py` — `GeminiProvider` class jo
  `google-generativeai` package se Gemini Flash ko call karti hai
- `providers/agentrouter_provider.py` — `AgentRouterProvider` class
  jo `openai` package se (kyunki AgentRouter OpenAI-compatible API
  deta hai) `claude-opus-4-8` ko call karti hai, custom `base_url`
  (`https://agentrouter.org/v1`) ke saath

## Kyun `BaseProvider` abstraction banayi

Agar kal ko koi teesra provider add karna ho (jaise Groq, ya seedha
Anthropic jab payment sort ho jaye), to bas ek naya class banega jo
`BaseProvider` ko implement kare — `call()` method mein apna API
call likhna hoga, aur `text`, `input_tokens`, `output_tokens` return
karna hoga. Baaki poora system (router, registry, cost engine) ko
pata bhi nahi chalega ki naya provider add hua.

## Important caveats (yaad rakhne wali baatein)

- AgentRouter **official Anthropic/OpenAI channel nahi hai** — ek
  third-party gateway hai jo free credits deta hai. Model naam jaise
  "claude-opus-4-8" isi platform ke through resolve hote hain.
- AgentRouter apna pricing publish nahi karta, isliye humne registry
  mein **estimated/placeholder rates** rakhe hain sirf reporting ke
  liye — actual charge free credits khatam hone tak $0 rahega.
- Gemini Flash genuinely free tier pe hai, lekin free tier mein
  request rate limits hoti hain (roughly kuch hazaar requests/day) —
  production-scale load ke liye paid tier chahiye hoga.

## Test kaise kiya

Har provider ko individually import karke check kiya ki `call()`
method sahi format mein `text`, `input_tokens`, `output_tokens`
return kar raha hai (poora integration test Stage 3 mein hua).

## Status
✅ Complete
