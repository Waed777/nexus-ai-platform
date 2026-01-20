import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def run_ai_engine(df: pd.DataFrame):
    df = df.copy()

    # -------- 1. Select numeric columns safely --------
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_cols) < 2:
        raise ValueError("Dataset must contain at least 2 numeric columns for AI analysis.")

    # -------- 2. Handle missing values --------
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    # -------- 3. Scaling --------
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[numeric_cols])

    # -------- 4. Anomaly Detection --------
    model = IsolationForest(
        n_estimators=200,
        contamination=0.02,
        random_state=42
    )

    df["anomaly_score"] = model.fit_predict(X_scaled)
    df["anomaly"] = df["anomaly_score"].map({1: "Normal", -1: "Anomaly"})

    # -------- 5. Risk Score (generic, works for ANY dataset) --------
    df["risk_score"] = np.abs(X_scaled).mean(axis=1)
    df["risk_score"] = df["risk_score"] / df["risk_score"].max()

    # -------- 6. Risk Levels --------
    df["risk_level"] = pd.cut(
        df["risk_score"],
        bins=[0, 0.4, 0.7, 1],
        labels=["Low", "Medium", "High"]
    )

    # -------- 7. Executive Summary --------
    summary = {
        "anomalies": int((df["anomaly"] == "Anomaly").sum()),
        "high_risk": int((df["risk_level"] == "High").sum()),
        "confidence": int(min(95, 70 + len(numeric_cols) * 5))
    }

    return df, summary
