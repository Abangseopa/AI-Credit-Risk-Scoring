# AI Credit Risk Scoring (Delivered via WhatsApp & API)

Small service that scores SME/consumer credit risk using rules + ML features. 
Supports: conversational intake (WhatsApp) and a simple HTTP API.

**Demo:** <PUT_DEMO_URL_HERE>  
**Repo site:** add your demo URL in the repo “About” too.

## Live Flow
User provides business/customer info → service enriches features → model scores PD / risk band → returns decision + reasons.

## Architecture
| Folder | Purpose |
|---|---|
| /backend | Scoring API (Edge Function / serverless) + feature transforms |
| /ui | WhatsApp webhook or tiny web form for intake |
| /screenshots | Flow images for README |

## Endpoints
- `POST /score` → returns `{pd, band, reasons, limits}`

## Env
Copy `/backend/.env.example` to `.env` and fill values.

## Why it matters
Fast, explainable underwriting for thin-file or underserved companies.
