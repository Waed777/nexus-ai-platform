def generate_insights(summary):
    insights = []

    insights.append(
        f"📊 The dataset contains {summary['anomalies']} anomalous records requiring attention."
    )

    insights.append(
        f"⚠️ {summary['high_risk']} entities are classified as high risk and may impact operations."
    )

    insights.append(
        "🤖 AI recommends prioritizing high-risk entities and automating low-risk processes."
    )

    insights.append(
        "📈 Continuous monitoring is advised to reduce operational risk and improve efficiency."
    )

    return "\n\n".join(insights)
