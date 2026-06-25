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

    # Check description quality — length AND semantic richness
    business_keywords = [
        "revenue", "sales", "customer", "cost", "profit", "loss", "cash",
        "debt", "loan", "supplier", "rent", "staff", "employee", "competition",
        "price", "demand", "stock", "inventory", "month", "year", "started",
        "changed", "tried", "problem", "issue", "dropped", "increased"
    ]
    description_lower = description.lower()
    keyword_hits = sum(1 for word in business_keywords if word in description_lower)

    if len(description) > 150 and keyword_hits >= 3:
        score += 30
        reasons.append(f"✅ Detailed description with {keyword_hits} relevant business terms detected")
    elif len(description) > 150 and keyword_hits < 3:
        score += 15
        reasons.append("⚠️ Long description but lacks specific business details")
        deductions.append("💡 Tip: Mention specific numbers, timelines, and what changed")
    elif len(description) > 50 and keyword_hits >= 2:
        score += 15
        reasons.append("⚠️ Brief but relevant description provided")
        deductions.append("💡 Tip: Add more detail about when this started and what you tried")
    else:
        deductions.append("❌ Description too vague — analysis will be generic")

    # Sanity check on numbers
    if monthly_revenue > 0 and monthly_costs > monthly_revenue * 5:
        deductions.append("⚠️ Costs are 5x revenue — please double check your numbers")
        score = max(0, score - 15)

    
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