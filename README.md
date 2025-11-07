# AI Credit Risk Scoring (Plaid + Alternative Data)

Score SME/consumer credit risk from connected bank data (Plaid) plus alternative signals (e-commerce quality, ops metrics). 
Simple Python backend with two files: `main.py` (scoring logic) and `api.py` (FastAPI API). UI can be any frontend (e.g., Lovable).

**Demo:** <ADD_DEMO_URL> • **API Base:** <ADD_API_URL>

## Live Flow
1) Borrower connects bank via Plaid Link →  
2) Backend exchanges token and (optionally) pulls key features →  
3) Alternative data merged →  
4) Model returns `pd`, risk band, max limit, and reasons.

## Endpoints
- `GET /health` → `{ ok: true }`  
- `POST /score` → body like `backend/demo_payload.json` → returns `{ pd, band, max_limit, reasons, features }`  
- `POST /bank/connect/exchange` → `{ public_token }` → `{ access_token }` (optional helper for Plaid)

## Run locally
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill PLAID_*
uvicorn api:app --reload --port 8000
