# Multi-cloud architecture and maturity

**Implemented locally:** original CC0 transaction fixture with simulated source-region tags; Python ingestion/validation with Bronze, Silver, Gold Parquet products; SHA-256 lineage checksum and rejected record quarantine; read-only FastAPI analytics and Streamlit dashboard; mock or opt-in local Ollama incident explanation; Docker and GitHub Actions; separate Terraform samples for Azure storage, AWS S3 and Google Cloud Storage.

**Not implemented:** actual cross-cloud ingestion or replication, managed identity federation, real-time CDC, object-storage upload adapters, cross-cloud orchestration, federated query, disaster recovery, workload benchmarking, full compliance guardrails, public-host authentication, deployed services or AI model hosting.

**Cloud design:** approved source extraction per provider -> Azure ADLS/S3/GCS Bronze buckets -> regional validation jobs -> Parquet/Delta Lake Silver/Gold -> cloud-agnostic product metadata and catalog -> FastAPI API and Streamlit portal on appropriate managed containers. Add OpenTelemetry, secrets managers, workload identity, per-provider IAM, encryption, private networking, billing and residency controls. Never copy datasets across regional boundaries without an approved legal/data-transfer basis. Terraform is opt-in and cloud resources incur costs.
