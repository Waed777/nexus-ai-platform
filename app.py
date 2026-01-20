import streamlit as st
import pandas as pd

from data_ingestion import load_data
from ai_engine import run_ai_engine
from automation import run_automation
from insights import generate_insights

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="NEXUS AI Platform",
    page_icon="🧠",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown("""
# 🧠 NEXUS AI
### Decision Intelligence & AI Automation Platform

Transform **raw data** into **decisions, insights, and automated actions**.
""")

st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Control Panel")
analysis_mode = st.sidebar.selectbox(
    "Analysis Mode",
    ["Executive Overview", "Risk & Anomalies", "Automation Opportunities"]
)

show_raw_data = st.sidebar.checkbox("Show Raw Data Preview")

# ---------------- UPLOAD ----------------
st.subheader("📁 Upload Your Data")
uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)

if not uploaded_file:
    st.info("⬆️ Upload a dataset to activate NEXUS AI")
    st.stop()

# ---------------- LOAD DATA ----------------
df = load_data(uploaded_file)

st.success(f"✅ Data Loaded | {df.shape[0]} rows × {df.shape[1]} columns")

if show_raw_data:
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head(10))

st.divider()

# ---------------- AI ENGINE ----------------
with st.spinner("🤖 NEXUS AI is analyzing your data..."):
    df_ai, summary = run_ai_engine(df)

# ---------------- KPI DASHBOARD ----------------
st.subheader("📊 Executive Dashboard")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Records", summary["total_records"])
k2.metric("Detected Anomalies", summary["anomalies"])
k3.metric("High Risk Entities", summary["high_risk"])
k4.metric("AI Confidence Score", f'{summary["confidence"]}%')

st.divider()

# ---------------- AI INSIGHTS ----------------
st.subheader("🧠 AI Executive Insights")

insights_text = generate_insights(summary)
st.markdown(insights_text)

st.divider()

# ---------------- CONDITIONAL VIEWS ----------------
if analysis_mode == "Risk & Anomalies":
    st.subheader("🚨 High Risk & Anomalous Records")
    st.dataframe(
        df_ai[df_ai["risk_level"] == "High"]
        .sort_values("risk_score", ascending=False)
        .head(25)
    )

elif analysis_mode == "Automation Opportunities":
    st.subheader("⚙️ AI Automation Opportunities")

    automation_results = run_automation(df_ai)

    for item in automation_results:
        st.markdown(f"""
        **🔹 Action:** {item['action']}  
        **📉 Impact**
