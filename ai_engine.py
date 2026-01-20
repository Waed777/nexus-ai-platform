import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def run_ai_engine(df):
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[numeric_cols])

    model = IsolationForest(contamination=0.02, random_state=42)
    df["anomaly"] = model.fit_predict(X_scaled)
    df["anomaly"] = df["anomaly"].map({1: "Normal", -1: "Anomaly"})

    # Risk score
    df["risk_score"] = np.mean(X_scaled, axis=1)
    df["risk_score"] = (df["risk_score"] - df["risk_score"].min()) / (
        df["risk_score"].max() - df["risk_score"].min()
    )

    # Risk level
    df["risk_level"] = pd.cut(
        df["risk_score"],
        bins=[-1, 0.4, 0.7, 1],
        labels=["Low", "Medium", "High"]
    )

    summary = {
        "anomalies": (df["anomaly"] == "Anomaly").sum(),
        "high_risk": (df["risk_level"] == "High").sum()
    }

    return df, summary
