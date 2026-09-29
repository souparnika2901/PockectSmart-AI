# PocketSmart AI — Complete implementation

This repository implements the supplied project specification as a runnable FastAPI web application.

## What is included
- FastAPI backend
- Jinja2/HTML/CSS/JavaScript frontend
- Registration/login/logout
- JWT stored in an HttpOnly cookie
- SQLite recommendation history
- Home, Party and Jewelry planners
- Optional JPG/PNG/WEBP outfit upload for jewelry
- Gemini integration through the current `google-genai` SDK
- Deterministic fallback mode when no Gemini key is configured
- Demo marketplace catalog and platform search links
- Swagger/OpenAPI documentation
- Automated tests

The source document describes Gemini 1.5 Flash Pro, FastAPI routes, authentication, history, multimodal jewelry input, and mock/simulated marketplace calls. Those requirements are implemented here. The marketplace layer intentionally uses demo data and search links because the document does not provide authorized partner API credentials or contracts.

## Current Gemini model
The source document's `Gemini 1.5 Flash Pro` reference is retained as the project concept, but `.env.example` defaults to `gemini-2.5-flash` for a current deployment. Change `GEMINI_MODEL` if your account provides another supported model.

## VS Code
1. Install Python 3.11+.
2. Open this folder in VS Code.
3. Open Terminal.
4. Create/activate a virtual environment.
5. Install requirements.
6. Copy `.env.example` to `.env`.
7. Add your Gemini API key if you want live AI responses.
8. Run `uvicorn app.main:app --reload`.
9. Open `http://127.0.0.1:8000`.

### Windows
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Test
```bash
pytest -q
```

Then visit `/docs` for API testing.

## Typical test flow
1. Register.
2. Login.
3. Open Home Planner and submit ₹20,000, `Bedroom`, modern.
4. Open Party Planner and submit a budget and guest count.
5. Open Jewelry Planner and optionally upload an outfit image.
6. Open Dashboard and verify history.
7. If `GEMINI_API_KEY` is blank, results show `fallback`. With a valid key, successful Gemini calls show `gemini`.

## Architecture
Browser → FastAPI routes → recommendation service → Gemini (optional) + demo marketplace catalog → SQLite history → browser.

## Production notes
- Use HTTPS.
- Set a strong random `SECRET_KEY`.
- Use a production database.
- Add CSRF protection if authentication is moved to broader cookie-based production workflows.
- Replace demo marketplace links/catalog with official APIs or authorized affiliate/partner integrations.
- Add rate limiting and structured logging.
- Do not expose `GEMINI_API_KEY` to the frontend.
