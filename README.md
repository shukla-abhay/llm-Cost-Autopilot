# LLM Cost Autopilot

An intelligent AI routing platform that automatically decides which LLM to use based on the complexity of your prompt — saving cost without sacrificing quality.

Simple prompts go to a **cheap model** (Gemini Flash), complex prompts go to a **strong model** (DeepSeek). A trained ML classifier makes this decision in milliseconds.

---

## How It Works

```
User Prompt
    │
    ▼
Complexity Classifier  ──→  easy/medium → Gemini Flash (cheap)
    │                   └─→  hard        → DeepSeek (strong)
    ▼
Quality Evaluator
    │
    ├── OK       → Return response
    └── Not OK   → Escalate to strong tier, retry
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, FastAPI, Uvicorn |
| ML Classifier | scikit-learn (Logistic Regression), joblib |
| Cheap LLM | Google Gemini Flash via `google-genai` SDK |
| Strong LLM | DeepSeek via OpenAI-compatible API |
| Frontend | React 19, TypeScript |
| Deployment | Render (single service) |

---

## Project Structure

```
llm-cost-autopilot/
├── backend/
│   └── app/
│       ├── main.py                  # FastAPI entry point, serves frontend + API
│       ├── config.py                # All env variables loaded via pydantic-settings
│       │
│       ├── providers/               # LLM provider adapters
│       │   ├── base.py              # Abstract base class (common interface)
│       │   ├── gemini_provider.py   # Cheap tier — Gemini Flash
│       │   └── agentrouter_provider.py  # Strong tier — DeepSeek
│       │
│       ├── models/
│       │   ├── schemas.py           # ModelResponse — standard response format
│       │   ├── registry.py          # Tier → provider + model + pricing mapping
│       │   └── interface.py         # call_model() — single entry point for all LLM calls
│       │
│       ├── router/
│       │   ├── classifier.py        # Feature extraction + ML prediction
│       │   ├── router.py            # Routing logic — ties classifier + model + evaluator
│       │   └── train.py             # Script to train and save classifier.pkl
│       │
│       ├── evaluation/
│       │   └── evaluator.py         # Quality check + escalation logic
│       │
│       └── api/routes/
│           └── chat.py              # POST /api/chat endpoint
│
├── frontend/
│   └── src/
│       └── App.tsx                  # Single-page React UI
│
├── datasets/
│   └── routing_dataset.json         # 109 labeled prompts (easy/medium/hard)
│
└── models/
    └── classifier.pkl               # Trained Logistic Regression model
```

---

## Section-wise Details

### 1. Providers (`backend/app/providers/`)

Each LLM provider has its own adapter class that implements a common `BaseProvider` interface with a single `call()` method. This means the rest of the app never talks to a provider directly — it just calls `call()` and gets back a standard dict.

- **GeminiProvider** — uses `google-genai` SDK, calls Gemini Flash model. Returns `text`, `input_tokens`, `output_tokens`.
- **DeepSeekProvider** — uses `openai` SDK pointed at DeepSeek's OpenAI-compatible base URL (`https://api.deepseek.com/v1`). Same return format.

Switching providers in future = just add a new file here, no other code changes needed.

---

### 2. Model Registry (`backend/app/models/registry.py`)

Central config that maps tier names to actual providers, model IDs, and pricing:

```
"cheap"  → GeminiProvider  + gemini-flash  + $0.30/M input, $2.50/M output
"strong" → DeepSeekProvider + deepseek-chat + $0.27/M input, $1.10/M output
```

Also contains `calculate_cost()` which computes exact USD cost per request based on token counts.

---

### 3. Unified Model Interface (`backend/app/models/interface.py`)

Single function `call_model(prompt, tier)` that:
1. Looks up the tier config from registry
2. Calls the provider
3. Calculates cost
4. Returns a `ModelResponse` Pydantic object

Every part of the app (router, evaluator, API) uses only this function — never calls providers directly.

---

### 4. Complexity Classifier (`backend/app/router/classifier.py`)

A **Logistic Regression** model trained on 109 labeled prompts. It extracts 6 features from each prompt:

| Feature | Description |
|---------|-------------|
| `length` | Word count |
| `hard_kw` | Count of hard keywords (analyze, architecture, prove, etc.) |
| `medium_kw` | Count of medium keywords (explain, summarize, write, etc.) |
| `question_marks` | Number of `?` in prompt |
| `sentences` | Sentence count |
| `avg_word_len` | Average word length |

Output: `{ complexity: "easy" | "medium" | "hard", confidence: 0.0–1.0 }`

The trained model is saved as `models/classifier.pkl` using `joblib` and loaded at runtime.

---

### 5. Intelligent Router (`backend/app/router/router.py`)

Takes a prompt, runs it through the classifier, then decides the tier:

```
easy / medium  →  cheap tier (Gemini Flash)
hard           →  strong tier (DeepSeek)
```

After getting the response, it passes it to the Quality Evaluator before returning.

---

### 6. Quality Evaluator (`backend/app/evaluation/evaluator.py`)

Checks if the model's response is actually useful. Two checks:

1. **Length check** — response must be at least 20 characters
2. **Failure phrase detection** — if response contains phrases like `"i don't know"`, `"i cannot"`, `"as an ai"`, etc., it's considered bad quality

If quality is bad → automatically escalates to the **strong tier** and retries. This ensures cheap-tier failures are silently recovered.

---

### 7. API Layer (`backend/app/api/routes/chat.py`)

Single endpoint:

```
POST /api/chat
Body: { "prompt": "your question here" }

Response: {
  "response": "...",
  "tier": "cheap" | "strong",
  "model": "gemini-flash | deepseek-chat",
  "complexity": "easy" | "medium" | "hard",
  "estimated_cost_usd": 0.000012,
  "input_tokens": 15,
  "output_tokens": 42
}
```

---

### 8. FastAPI Main (`backend/app/main.py`)

- Mounts the React `frontend/build/` folder as static files
- This means **one deployment serves both frontend and backend** on the same URL
- CORS is configured to allow all origins

---

### 9. Frontend (`frontend/src/App.tsx`)

Single-page React + TypeScript app with no external UI libraries — pure inline styles. Features:

- Textarea for prompt input (Cmd+Enter to submit)
- Shows routing decision: complexity label → tier → model used
- Displays full response text
- Shows cost metrics: estimated cost, input tokens, output tokens, total tokens

---

## Setup

### 1. Clone & install

```bash
git clone https://github.com/shukla-abhay/llm-Cost-Autopilot.git
cd llm-Cost-Autopilot
```

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment variables

```bash
cp .env.example .env
```

Fill in `.env`:
```
GEMINI_API_KEY=your_gemini_key
DEEPSEEK_API_KEY=your_deepseek_key
```

- Gemini API key: https://aistudio.google.com (free)
- DeepSeek API key: https://platform.deepseek.com (cheap)

### 3. Run backend

```bash
cd backend
uvicorn app.main:app --reload
```

### 4. Run frontend (development)

```bash
cd frontend
npm install
npm start
```

---

## Deployment

Deployed as a single service on **Render** — React build is served directly by FastAPI as static files.

Build command:
```
cd frontend && npm install && npm run build && cd ../backend && pip install -r requirements.txt
```

Start command:
```
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Environment variables required on Render: `GEMINI_API_KEY`, `DEEPSEEK_API_KEY`
