import pandas as pd
from fastapi.testclient import TestClient
from backend.main import app
from platform_core.pipeline import run
from platform_core.ai import explain


def test_pipeline(tmp_path):
    source = tmp_path / "input.csv"
    pd.DataFrame([
        {"transaction_id": 1, "cloud_region": "azure-eu", "department": "ops", "amount_usd": 50, "status": "settled"},
        {"transaction_id": 2, "cloud_region": "aws-us", "department": "ops", "amount_usd": -1, "status": "settled"}
    ]).to_csv(source, index=False)
    result = run(str(source), str(tmp_path / "lake"), str(tmp_path / "report.json"))
    assert result["raw"] == 2 and result["valid"] == 1 and result["rejected"] == 1


def test_api(monkeypatch, tmp_path):
    monkeypatch.setenv("REPORT_PATH", str(tmp_path / "missing.json"))
    monkeypatch.setenv("GOLD_PATH", str(tmp_path / "missing.parquet"))
    client = TestClient(app)
    assert client.get("/health").status_code == 200
    assert client.get("/api/analytics").json()["regions"] == []
    assert client.post("/api/ai/investigate").status_code == 404


def test_mock(monkeypatch):
    monkeypatch.setenv("LLM_MODE", "mock")
    assert explain({"raw": 2, "valid": 1, "rejected": 1, "regions": 1, "alert": "review"})["human_review"]
