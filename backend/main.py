from __future__ import annotations
from typing import Dict, Any, Tuple
import yaml
import math
from pathlib import Path

CONFIG = yaml.safe_load(Path(__file__).with_name("config.yaml").read_text())
S = CONFIG["scoring"]
LIMITS = CONFIG["limits"]

def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))

def _risk_band(pd: float) -> str:
    # Simple band edges; tweak as needed
    if pd < 0.08: return "A"
    if pd < 0.15: return "B"
    if pd < 0.25: return "C"
    return "D"

def _reasons(features: Dict[str, Any]) -> list[str]:
    r = []
    if features.get("prior_defaults", 0) > 0:
        r.append("Prior default on file")
    if features.get("operating_margin", 0) <= S["margin_good_threshold"]:
        r.append("Low operating margin")
    if features.get("months_in_business", 0) < S["min_months_in_business"]:
        r.append("Short operating history")
    if features.get("bank_balance", 0) < S["min_bank_balance_good"]:
        r.append("Low available cash")
    if features.get("alt_signal_score", 0) < 0.6:
        r.append("Weak alternative data signals")
    return r

def build_features(payload: Dict[str, Any]) -> Dict[str, Any]:
    fin = payload.get("financials", {})
    biz = payload.get("business", {})
    alt = payload.get("alt_data", {})

    revenue = float(fin.get("monthly_revenue", 0))
    expenses = float(fin.get("monthly_expenses", 0))
    margin = revenue - expenses

    # Simple normalized “alt signal” (example)
    alt_signal = 0.0
    if alt:
        # scale: ratings high good, delivery days low good, SLA high good
        rating = float(alt.get("ecom_rating", 0)) / 5.0           # 0..1
        delivery = alt.get("avg_delivery_days", 7)
        delivery_norm = max(0.0, 1.0 - (float(delivery) / 10.0))  # ~0..1
        sla = float(alt.get("support_sla_score", 0))               # 0..1 already
        alt_signal = max(0.0, min(1.0, 0.5*rating + 0.3*sla + 0.2*delivery_norm))

    return {
        "operating_margin": margin,
        "months_in_business": int(biz.get("months_in_business", 0)),
        "bank_balance": float(fin.get("bank_balance", 0)),
        "prior_defaults": int(fin.get("prior_defaults", 0)),
        "alt_signal_score": alt_signal
    }

def score_pd(features: Dict[str, Any]) -> float:
    pd = float(S["base_pd"])

    if features["months_in_business"] >= S["min_months_in_business"]:
        pd += float(S["long_history_bonus"])
    if features["prior_defaults"] > 0:
        pd += float(S["default_penalty"])
    if features["bank_balance"] >= S["min_bank_balance_good"]:
        pd += float(S["high_balance_bonus"])
    if features["operating_margin"] > S["margin_good_threshold"]:
        pd += float(S["good_margin_bonus"])

    # Nudge from alternative data (±5% based on z-ish transform)
    alt = features["alt_signal_score"]  # 0..1
    pd *= (1.0 - 0.1 * (alt - 0.5))     # high alt lowers PD slightly

    return clamp(pd, 0.01, 0.99)

def score(payload: Dict[str, Any]) -> Dict[str, Any]:
    feats = build_features(payload)
    pd = score_pd(feats)
    band = _risk_band(pd)
    reasons = _reasons(feats)
    max_limit = LIMITS[band]
    return {
        "model": "baseline_rules_v1",
        "pd": round(pd, 4),
        "band": band,
        "max_limit": max_limit,
        "reasons": reasons,
        "features": feats
    }

