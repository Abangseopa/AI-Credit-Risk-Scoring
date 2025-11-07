# AI agents for Credit Risk Scoring (Plaid-ready, Alternative Data Enhanced)

Simple demo of an AI credit risk engine for SMB lending. Borrowers enter basic business info, then (in production) connect a bank account via Plaid. The model produces an overall risk score and a factor breakdown using cash-flow signals and alternative data.

## Live Flow

1) Business info → industry, loan amount, years active  
<img src="/screenshots/page1.png" width="360" />

2) Same form with sample values filled  
<img src="/screenshots/page2.png" width="360" />

3) “Connect Bank Account” explainer (what we analyze)  
<img src="/screenshots/page3.png" width="360" />

4) AI analysis loading state (simulates Plaid data ingestion)  
<img src="/screenshots/page4.png" width="360" />

5) Result: Overall risk score + short rationale  
<img src="/screenshots/page5.png" width="420" />

6) Factor breakdown: cash flow, revenue growth, payment history, debt ratio, market risk  
<img src="/screenshots/page6.png" width="420" />

---

## Repo layout
/backend
├─ api.py        # FastAPI endpoints: /score, /factors (reads demo JSON if no Plaid)
├─ main.py       # App bootstrap + simple risk logic / model stub
└─ demo.json     # Sample bank-like aggregates (cash-in/out, balances, invoices)

/ui               # Lovable front-end (no live Plaid; uses backend demo data)
/screenshots      # Images referenced above
.env.example      # MODEL_KEY=…, PLAID_* (optional), ALT_DATA_TOGGLE=true
## Notes

- This demo does **not** connect to Plaid in UI. The backend can read `demo.json` so reviewers see the full scoring workflow end-to-end.  
- In production, replace the demo reader with Plaid transactions/balance endpoints and pass normalized features to the scoring function.
