def run_automation(df):
    actions = []

    for _, row in df.iterrows():
        if row["risk_level"] == "High":
            actions.append("🔴 Immediate Investigation Required")
        elif row["risk_level"] == "Medium":
            actions.append("🟠 Monitor & Review")
        else:
            actions.append("🟢 Auto-Approved / No Action Needed")

    df["automation_action"] = actions
    return df
