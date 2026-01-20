import streamlit as st
import pandas as pd
from data_ingestion import load_data
from ai_engine import run_ai_engine
from automation import run_automation
from insights import generate_insights

st.set_page_config(page_title="NEXUS AI Platform", layout="wide")
st.title("🧠 NEXUS AI – Enterprise Analytics & Automation Platform")

st.markdown("""
Upload any business dataset.  
NEXUS AI will automatically analyze risks, detect patterns, and generate AI-driven insights & recommendations.
""")

# -------- Upload Data --------
uploaded_file = st.file_uploader(
    "📁 Upload your data (CSV / Excel)",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file:
    df = load_data(uploaded_file)

    st.success(f"✅ Data loaded successfully | Rows: {df.shape[0]} | Columns: {df.shape[1]}")

    # -------- Run AI Engine --------
    with st.spinner("🤖 Running AI Engine..."):
        df_ai, summary = run_ai_engine(df)

    # -------- KPIs --------
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(df_ai))
    col2.metric("Detected Anomalies", summary["anomalies"])
    col3.metric("High Risk Entities", summary["high_risk"])

    # -------- Automation --------
    automation_results = run_automation(df_ai)

    # -------- Insights --------
    st.subheader("🧠 AI Executive Insights")
    insights_text = generate_insights(summary)
    st.write(insights_text)

    # -------- Tables --------
    st.subheader("🚨 High Risk & Anomalies")
    st.dataframe(df_ai[df_ai["risk_level"] == "High"].head(20))

    # -------- Download --------
    st.download_button(
        "⬇️ Download AI Results",
        df_ai.to_csv(index=False),
        "nexus_ai_results.csv",
        "text/csv"
    )

else:
    st.info("Please upload a dataset to begin AI analysis.")
