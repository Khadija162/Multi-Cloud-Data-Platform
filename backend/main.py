"""Read-only local multi-cloud catalog/analytics service."""
import json
import os
from pathlib import Path
import pandas as pd
import requests
from fastapi import FastAPI, HTTPException
from platform_core.ai import explain

app = FastAPI(title="Multi-Cloud Data Platform API", version="0.1.0")


def report():
    path = Path(os.getenv("REPORT_PATH", "artifacts/report.json"))
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


@app.get("/health")
def health():
    return {"status": "ok", "report_ready": report() is not None}


@app.get("/api/analytics")
def analytics():
    file = Path(os.getenv("GOLD_PATH", "data/gold/regional_summary.parquet"))
    records = pd.read_parquet(file).round(2).to_dict("records") if file.is_file() else []
    return {"report": report(), "regions": records}


@app.post("/api/ai/investigate")
def investigate():
    current = report()
    if current is None:
        raise HTTPException(404, "Run the data pipeline first")
    try:
        return explain(current)
    except (requests.RequestException, ValueError, KeyError) as exc:
        raise HTTPException(502, "Model unavailable") from exc
