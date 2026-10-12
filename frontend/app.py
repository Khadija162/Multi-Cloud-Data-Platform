import os
import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Multi-Cloud Data Control Center", layout="wide")
st.title("Multi-Cloud Data Platform")
st.caption("Portable Bronze / Silver / Gold data products · Azure / AWS / GCP design")
st.info("Cloud-region names are simulated source tags. No real cross-cloud ingestion is configured.")
api = os.getenv("API_URL", "http://localhost:8000")
try:
    response = requests.get(api + "/api/analytics", timeout=8)
    response.raise_for_status()
    data = response.json()
except requests.RequestException as exc:
    st.error(f"API unavailable: {exc}")
    data = {"report": None, "regions": []}
report = data.get("report")
if report:
    a, b, c = st.columns(3)
    a.metric("Raw records", report["raw"])
    b.metric("Validated", report["valid"])
    c.metric("Rejected", report["rejected"])
    st.write("Data quality:", report["alert"])
    if st.button("AI: investigate data quality"):
        try:
            response = requests.post(api + "/api/ai/investigate", timeout=100)
            response.raise_for_status()
            st.json(response.json())
        except requests.RequestException as exc:
            st.error(str(exc))
else:
    st.info("Run python -m platform_core.pipeline to create the first report.")
if data.get("regions"):
    regions = pd.DataFrame(data["regions"])
    st.subheader("Analytics by simulated source region")
    st.bar_chart(regions.set_index("cloud_region")["total_amount_usd"])
    st.dataframe(regions, use_container_width=True)
