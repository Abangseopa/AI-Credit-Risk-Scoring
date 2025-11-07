from __future__ import annotations
import os
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from main import score
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Load env vars (works locally; your host may inject envs differently)
load_dotenv()

app = FastAPI(title="AI Credit Risk Scoring API", version="0.1.0")

class Applicant(BaseModel):
    business: Dict[str, Any] | None = None
    financials: Dict[str, Any] | None = None
    alt_data: Dict[str, Any] | None = None
    bank_access_token: str | None = None   # optional: exchanged Plaid token

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/score")
def score_endpoint(applicant: Applicant):
    try:
        # If you later fetch bank transactions via Plaid using bank_access_token,
        # enrich applicant.financials here before scoring.
        result = score(applicant.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Optional: Plaid token exchange endpoint (front end calls this after Link)
try:
    from plaid import Client
    _has_plaid = True
except Exception:
    _has_plaid = False

@app.post("/bank/connect/exchange")
def exchange_public_token(payload: Dict[str, str]):
    if not _has_plaid:
        raise HTTPException(400, "Plaid SDK not installed")
    client_id = os.getenv("PLAID_CLIENT_ID")
    secret = os.getenv("PLAID_SECRET")
    env = os.getenv("PLAID_ENV", "sandbox")

    if not client_id or not secret:
        raise HTTPException(400, "Missing PLAID credentials")

    public_token = payload.get("public_token")
    if not public_token:
        raise HTTPException(400, "public_token required")

    client = Client(client_id=client_id, secret=secret, environment=env)
    exchange = client.Item.public_token.exchange(public_token)
    # You’ll return access_token to your UI; store it securely server-side in real apps
    return {"access_token": exchange["access_token"]}

