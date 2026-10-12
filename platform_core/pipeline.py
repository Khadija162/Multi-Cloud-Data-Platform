"""Portable local lakehouse ETL with provenance, quality quarantine and data products."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

REQUIRED = ["transaction_id", "cloud_region", "department", "amount_usd", "status"]
STATUSES = {"pending", "settled", "failed"}


def run(source="data/public/transactions.csv", root="data", report="artifacts/report.json"):
    file = Path(source)
    frame = pd.read_csv(file)
    missing = set(REQUIRED) - set(frame.columns)
    if missing:
        raise ValueError(f"Missing fields: {sorted(missing)}")
    base = Path(root)
    for layer in ("bronze", "silver", "gold"):
        (base / layer).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(base / "bronze" / "transactions.parquet", index=False)
    amounts = pd.to_numeric(frame["amount_usd"], errors="coerce")
    valid = frame["transaction_id"].notna() & ~frame["transaction_id"].duplicated()
    valid &= amounts.notna() & amounts.ge(0)
    valid &= frame["cloud_region"].notna() & frame["department"].notna()
    valid &= frame["status"].isin(STATUSES)
    clean = frame.loc[valid].copy()
    clean["amount_usd"] = amounts.loc[valid]
    clean.to_parquet(base / "silver" / "transactions.parquet", index=False)
    frame.loc[~valid].to_parquet(base / "silver" / "rejected.parquet", index=False)
    gold = clean.groupby("cloud_region", as_index=False).agg(
        transactions=("transaction_id", "size"), total_amount_usd=("amount_usd", "sum")
    )
    gold.to_parquet(base / "gold" / "regional_summary.parquet", index=False)
    result = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "source_sha256": hashlib.sha256(file.read_bytes()).hexdigest(),
        "source_license": "CC0 original synthetic sample",
        "raw": int(len(frame)), "valid": int(len(clean)),
        "rejected": int((~valid).sum()), "regions": int(len(gold)),
        "alert": "review" if (~valid).sum() else "passed"
    }
    destination = Path(report)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="data/public/transactions.csv")
    args = parser.parse_args()
    print(json.dumps(run(args.source), indent=2))
