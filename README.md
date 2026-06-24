# AI API Service

A REST API built with **FastAPI** that exposes three AI-powered endpoints, backed by Google's **Gemini API**:

- `POST /summarize` — summarize a block of text
- `POST /translate` — translate text into a target language
- `POST /generate-email` — generate a draft email for a given purpose/tone

Built as part of the AI/ML Intern Round 1 assignment (Python & API Development).

---
## Live Application

👉 https://ai-api-tool.onrender.com/

[Open App](https://ai-api-tool.onrender.com/)

---
## Features

- Clean, layered project structure (routers → services → schemas/config)
- Request validation with Pydantic (auto 422 errors with clear messages)
- Centralized exception handling (custom `AIServiceError` + generic fallback)
- Logging to console and to a rotating log file (`logs/app.log`)
- Environment-based configuration (no secrets hardcoded)
- Auto-generated interactive API docs (Swagger UI + ReDoc)

---

## Project Structure

```
ai-api-project/
├── app/
│   ├── main.py                 # FastAPI app, middleware, exception handlers
│   ├── core/
│   │   ├── config.py           # Settings loaded from .env
│   │   ├── logging_config.py   # Logging setup (console + file)
│   │   └── exceptions.py       # Custom exceptions + handlers
│   ├── routers/
│   │   └── ai_routes.py        # /summarize, /translate, /generate-email
│   ├── schemas/
│   │   └── ai_schemas.py       # Pydantic request/response models
│   └── services/
│       └── ai_service.py       # Gemini API integration logic
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Setup & Run

### 1. Clone and enter the project
```bash
git clone <your-repo-url>
cd ai-api-project
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Open `.env` and add your free Gemini API key (get one at https://aistudio.google.com/app/apikey):
```
GEMINI_API_KEY=your_actual_key_here
```

### 5. Run the server
```bash
uvicorn app.main:app --reload
```

The API will be running at: `http://127.0.0.1:8000`

### 6. Open the interactive docs
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## API Reference

See [`API_DOCUMENTATION.md`](./API_DOCUMENTATION.md) for full request/response examples for every endpoint, plus error responses.

Quick example:
```bash
curl -X POST http://127.0.0.1:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Paste a long paragraph here that you want summarized into something shorter.", "max_words": 50}'
```

---

## Error Handling

| Scenario                          | Status Code | Response shape |
|------------------------------------|--------------|-----------------|
| Invalid/missing request fields     | 422          | Pydantic validation error detail |
| Gemini API/network failure         | 502          | `{"success": false, "error": "AI_SERVICE_ERROR", "message": "..."}` |
| Any unhandled server error         | 500          | `{"success": false, "error": "INTERNAL_SERVER_ERROR", "message": "..."}` |

All requests and responses (with status + duration) are logged to console and `logs/app.log`.

---

## Tech Stack

- **FastAPI** — web framework
- **Pydantic / pydantic-settings** — validation & config
- **Google Generative AI SDK (Gemini)** — summarization, translation, email generation
- **Uvicorn** — ASGI server
- **Python logging (RotatingFileHandler)** — structured logs

---

## Notes

- `.env` is git-ignored — never commit real API keys.
- The Gemini free tier is sufficient to run and demo this project.
