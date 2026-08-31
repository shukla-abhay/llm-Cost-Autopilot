# LLM Cost Autopilot

Multi-provider intelligent AI routing platform — easy requests jaate hain
free/cheap model (Gemini Flash) pe, hard requests jaate hain strong model
(AgentRouter's claude-opus-4-8) pe. Ek trained classifier decide karta hai
kaunsa request kaunse tier mein jaayega.

## Architecture

```
User Prompt
    │
    ▼
Request Analyzer (features nikalta hai: length, keywords, etc.)
    │
    ▼
Complexity Classifier (Easy / Medium / Hard + confidence)
    │
    ▼
Router (tier decide karta hai: "cheap" ya "strong")
    │
    ├── cheap  → Gemini Flash (free)
    └── strong → AgentRouter claude-opus-4-8
    │
    ▼
Quality Evaluator (jawab acha hai ya nahi?)
    │
    ├── OK  → Return response
    └── Not OK → Escalate to "strong" tier, retry
```

## Prerequisites

- Python 3.11+
- VS Code
- Gemini API key: https://aistudio.google.com (free, no card)
- AgentRouter API key: https://agentrouter.org (free credits)

## Setup

### 1. Virtual environment

```bash
cd backend
python -m venv venv
```

Activate:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment variables

```bash
cd ..
cp .env.example .env
```

`.env` file kholo aur fill karo:
```
GEMINI_API_KEY=apni_gemini_key
AGENTROUTER_API_KEY=apni_agentrouter_key
```

### 4. Test the unified model interface

Ye sabse important test hai — dono providers (cheap + strong) ko ek
saath verify karta hai:

```bash
cd backend
python -m app.models.interface
```

**Expected output:**
```
=== CHEAP TIER (Gemini Flash) ===
Response: Machine learning is...
Provider: gemini | Model: gemini-2.5-flash
Tokens: 15 in / 42 out
Estimated cost: $0.0001

=== STRONG TIER (AgentRouter claude-opus-4-8) ===
Response: Machine learning is...
Provider: agentrouter | Model: claude-opus-4-8
Tokens: 15 in / 48 out
Estimated cost: $0.0004
```

### 5. Test the FastAPI server

```bash
uvicorn app.main:app --reload
```

Browser mein kholo: http://127.0.0.1:8000/health

## Project Structure

```
backend/
├── app/
│   ├── main.py                    # FastAPI entrypoint
│   ├── config.py                  # Settings (.env se load hota hai)
│   │
│   ├── providers/                 # Har LLM provider ka adapter
│   │   ├── base.py                #   common interface (contract)
│   │   ├── gemini_provider.py     #   cheap tier
│   │   └── agentrouter_provider.py#   strong tier
│   │
│   ├── models/
│   │   ├── schemas.py             # ModelResponse (standard format)
│   │   ├── registry.py            # tier -> provider+model+pricing mapping
│   │   └── interface.py           # call_model() — SINGLE entry point
│   │
│   ├── router/                    # (Step 6-7 mein banega)
│   ├── evaluation/                # (Step 8 mein banega)
│   ├── database/                  # (Step 9 mein banega)
│   └── analytics/                 # (Step 10 mein banega)
│
datasets/
└── routing_dataset.json           # 109 labeled examples (easy/medium/hard)
```

## Current Status

- [x] Step 1 — Project setup
- [x] Step 2 — Providers (Gemini + AgentRouter)
- [x] Step 3 — Unified Model Interface
- [x] Step 4 — Model Registry + Cost Engine
- [x] Step 5 — Routing Dataset (109 examples)
- [ ] Step 6 — Complexity Classifier
- [ ] Step 7 — Intelligent Router
- [ ] Step 8 — Quality Evaluator + Escalation
- [ ] Step 9 — Database + Logging
- [ ] Step 10 — Analytics
- [ ] Step 11 — FastAPI Production Routes
- [ ] Step 12 — React Dashboard
- [ ] Step 13 — Testing
- [ ] Step 14 — Docker
- [ ] Step 15 — Deployment


