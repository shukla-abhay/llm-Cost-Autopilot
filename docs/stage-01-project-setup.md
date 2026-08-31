# Stage 1 — Project Setup

## Kya banaya

- Poora repository folder structure banaya:
  ```
  llm-cost-autopilot/
  ├── backend/app/
  │   ├── api/routes/
  │   ├── providers/
  │   ├── router/
  │   ├── models/
  │   ├── evaluation/
  │   ├── analytics/
  │   └── database/
  ├── frontend/
  ├── datasets/
  └── docs/
  ```
- `requirements.txt` — sab zaroori Python packages (FastAPI, Pydantic,
  SQLAlchemy, Redis, provider SDKs)
- `.env.example` — environment variables ka template (credentials kabhi
  bhi seedha code mein nahi likhte)
- `config.py` — Pydantic `Settings` class jo `.env` se sab values load
  karti hai. Poore app mein kahin bhi `os.environ` seedha nahi likhte —
  hamesha `from app.config import settings` karke use karte hain.
- `main.py` — FastAPI ka entry point, sirf ek `/health` route ke saath

## Kyun aise kiya

**Modular folder structure kyun:** Har concern (providers, routing,
evaluation, database) apne alag folder mein hai. Isse project badhne
ke saath bhi code samajhna aasan rehta hai — koi ek 2000-line file
nahi banti.

**`.env` + `config.py` pattern kyun:** Credentials (API keys, DB
passwords) kabhi bhi GitHub pe commit nahi honi chahiye. `.env` file
`.gitignore` mein rehti hai, sirf `.env.example` (khali template)
commit hoti hai.

## Test kaise kiya

```bash
cd backend
uvicorn app.main:app --reload
```

Browser mein `http://127.0.0.1:8000/health` pe gaye, response mila:
```json
{"status": "ok", "message": "Server is running"}
```

## Status
✅ Complete
