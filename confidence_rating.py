def calculate_confidence(monthly_revenue, monthly_costs, cash_on_hand, description):
    
    score = 0
    reasons = []
    deductions = []

    # Check financial inputs
    if monthly_revenue > 0:
        score += 25
        reasons.append("✅ Monthly revenue provided")
    else:
        deductions.append("❌ No revenue data — analysis is less precise")

    if monthly_costs > 0:
        score += 25
        reasons.append("✅ Monthly costs provided")
    else:
        deductions.append("❌ No cost data — financial flags may be incomplete")

    if cash_on_hand > 0:
        score += 20
        reasons.append("✅ Cash position provided")
    else:
        deductions.append("❌ No cash data — runway calculation unavailable")

    # Check description quality
    if len(description) > 150:
        score += 30
        reasons.append("✅ Detailed situation description provided")
    elif len(description) > 50:
        score += 15
        reasons.append("⚠️ Brief description — more detail would improve accuracy")
        deductions.append("💡 Tip: Describe when the crisis started and what changed")
    else:
        deductions.append("❌ Description too short — analysis may be generic")

    # Determine confidence level
    if score >= 85:
        level = "HIGH"
        color = "green"
        summary = "Strong financial data provided. Analysis is reliable."
    elif score >= 50:
        level = "MEDIUM"
        color = "orange"
        summary = "Partial data provided. Analysis is directionally correct but not precise."
    else:
        level = "LOW"
        color = "red"
        summary = "Insufficient data. Provide more details for a reliable analysis."

    return {
        "score": score,
        "level": level,
        "color": color,
        "summary": summary,
        "reasons": reasons,
        "deductions": deductions
    }