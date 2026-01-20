import streamlit as st
import pandas as pd
from data_ingestion import load_data
from ai_engine import run_ai_engine
from automation import run_automation
from insights import generate_insights

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="NEXUS AI – Decision Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Sidebar ----------------
st.sidebar.title("⚙️ NEXUS AI Control Center")
st.sidebar.markdown("Enterprise AI Analytics Platform")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📁 Upload Data", "📊 AI Dashboard", "🤖 AI Assistant"]
)

# ---------------- Home ----------------
if page == "🏠 Home":
    st.markdown(
        """
        <h1 style='text-align:center;'>🧠 NEXUS AI</h1>
        <h3 style='text-align:center;color:gray;'>
        From Raw Data → Intelligence → Automated Decisions
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    ### What NEXUS AI Does:
    - 🔍 Detects hidden risks & anomalies  
    - 📊 Analyzes massive datasets automatically  
    - 🤖 Generates executive-level AI insights  
    - ⚙️ Recommends automation actions  

    **Upload your data and let AI think for you.**
    """)

# ---------------- Upload Data ----------------
elif page == "📁 Upload Data":
    st.header("📁 Upload Your Dataset")

    uploaded_file = st.file_uploader(
        "Supported formats: CSV, Excel",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file:
        with st.spinner("🔄 Loading & preparing data..."):
            df = load_data(uploaded_file)

        st.success(f"✅ Data Ready | Rows: {df.shape[0]} | Columns: {df.shape[1]}")
        st.dataframe(df.head())

        st.session_state["data"] = df
    else:
        st.info("Please upload a dataset to continue.")

# ---------------- AI Dashboard ----------------
elif page == "📊 AI Dashboard":
    if "data" not in st.session_state:
        st.warning("Upload data first.")
    else:
        df = st.session_state["data"]

        with st.spinner("🤖 Running AI Engine..."):
            df_ai, summary = run_ai_engine(df)

        st.session_state["df_ai"] = df_ai
        st.session_state["summary"] = summary

        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Records", len(df_ai))
        col2.metric("Anomalies Detected", summary["anomalies"])
        col3.metric("High Risk Entities", summary["high_risk"])
        col4.metric("AI Confidence", f"{summary['confidence']}%")

        st.divider()

        # Visual Tables
        st.subheader("🚨 Critical Risk Records")
        st.dataframe(df_ai[df_ai["risk_level"] == "High"].head(20))

        st.subheader("⬇️ Export Results")
        st.download_button(
            "Download AI Analysis",
            df_ai.to_csv(index=False),
            "nexus_ai_results.csv",
            "text/csv"
        )

# ---------------- AI Assistant ----------------
elif page == "🤖 AI Assistant":
    if "summary" not in st.session_state:
        st.warning("Run AI analysis first.")
    else:
        summary = st.session_state["summary"]

        st.header("🤖 Executive AI Assistant")

        st.markdown("### 🧠 AI Executive Summary")
        insights = generate_insights(summary)
        st.write(insights)

        st.markdown("### ⚙️ Automation Recommendations")
        automation = run_automation(st.session_state["df_ai"])
        st.dataframe(pd.DataFrame(automation))
