# Multi-Cloud Data Platform

A portable **local full-stack data engineering prototype** with an open CC0 sample dataset, Bronze/Silver/Gold Parquet processing, data quality and source checksums, FastAPI analytics backend, Streamlit dashboard, optional Ollama-based open-weight AI investigation, Docker, GitHub Actions, and **three independently configurable Terraform cloud storage examples** (Azure, AWS, GCP).

> **Scope:** No cloud resources have been provisioned. The dataset's cloud tags are simulated: there is **no actual cross-cloud data movement or hosted processing** in this starter. CI, tests and Docker execution are not yet independently confirmed.

## System architecture

```text
Open synthetic CC0 CSV -> Pandas ingestion -> Bronze Parquet (raw)
                                             -> Silver Parquet (validated/rejected)
                                             -> Gold Parquet (regional summaries)
                                                    |
                                     JSON quality / checksum report
                                                    |
                                              FastAPI backend
                                                    |
                                            Streamlit frontend
                                        optional Ollama AI analysis

Azure: ADLS Gen2 (Terraform) | AWS: S3 (Terraform) | GCP: GCS (Terraform)
Cloud adapters, managed orchestration, authentication and replication: future work
```

## Open-source data

[data/public/transactions.csv](data/public/transactions.csv) contains 12 original fictional transactions published under the **CC0 1.0** dedication. See [data provenance](data/public/README.md). Cloud-region labels are synthetic source identifiers, **not observed Azure, AWS or GCP activity**.

## Windows PowerShell setup

```powershell
git clone https://github.com/Khadija162/Multi-Cloud-Data-Platform.git
cd Multi-Cloud-Data-Platform
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m platform_core.pipeline
.\.venv\Scripts\python.exe -m pytest -q
```

The ETL writes Parquet data under `data/bronze/`, `data/silver/`, `data/gold/` and a report at `artifacts/report.json`.

### Run frontend and backend locally

In separate terminals:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
.\.venv\Scripts\python.exe -m streamlit run frontend/app.py
```

API docs: http://localhost:8000/docs
Dashboard: http://localhost:8501

### Run Docker

After running the ETL locally:

```powershell
docker compose up --build
```

Both ports bind to localhost. FastAPI reads only host-mounted analytics and report files. The frontend communicates with the API over the Compose service network.

## Optional open-weight AI

Default `LLM_MODE=mock` does not need a model or API keys. For real inference with Ollama installed locally:

```powershell
ollama pull qwen2.5:3b
$env:LLM_MODE="ollama"
$env:OLLAMA_MODEL="qwen2.5:3b"
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

These environment values apply to the host-side backend, not the default Docker Compose environment. The AI only explains quality metrics; it does not change data or provision services.

## Cloud infrastructure starters

| Cloud | Directory | Example resources |
|---|---|---|
| Microsoft Azure | `infra/azure/` | Resource group, ADLS Gen2 storage |
| Amazon Web Services | `infra/aws/` | S3 bucket, public access blocking, encryption |
| Google Cloud | `infra/gcp/` | GCS bucket, uniform access, public access prevention |

These are **separate Terraform roots**, not one portable module. Cloud accounts, credentials, unique storage names, IAM permissions, budget limits and state backends must be configured before using `terraform init/plan/apply`. Applying any of them can incur charges. Do not deploy to production without authentication, least-privilege IAM, monitoring, encrypted state, private networking and regulatory data residency checks.

## What remains for enterprise-grade multi-cloud

Production next steps: ingest real appropriately licensed source data with provenance; implement cloud-specific storage adapters; manage data contracts and lineage; add scheduled orchestration and streaming/CDC; authenticate the API; establish regional policy controls, workload identity, audit/observability, cross-cloud cost accounting and disaster recovery. See [architecture roadmap](docs/architecture.md).

**Current maturity:** local reproducible data engineering and visualization starter, not operational multi-cloud infrastructure.
