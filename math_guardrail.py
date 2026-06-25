def run_math_guardrail(monthly_revenue, monthly_costs, cash_on_hand, ai_recommendation):

    warnings = []
    flags = []

    # Basic financial calculations
    monthly_profit = monthly_revenue - monthly_costs
    cash_runway = cash_on_hand / monthly_costs if monthly_costs > 0 else 0
    cost_ratio = monthly_costs / monthly_revenue if monthly_revenue > 0 else 1
    gross_margin = (monthly_revenue - monthly_costs) / monthly_revenue if monthly_revenue > 0 else 0

    # Rule 1: Business is losing money
    if monthly_profit < 0:
        flags.append(f"⚠️ MATH FLAG: Business is losing ₹{abs(monthly_profit):,} per month. Any recommendation requiring new spending must be questioned.")

    # Rule 2: Less than 1 month cash runway
    if cash_runway < 1:
        flags.append(f"🚨 CRITICAL FLAG: Only {cash_runway:.1f} months of cash remaining. Survival is the only priority right now.")

    # Rule 3: Cost ratio dangerously high
    if cost_ratio > 0.9:
        flags.append(f"⚠️ MATH FLAG: Costs are {cost_ratio*100:.0f}% of revenue. There is almost no margin for error.")

    # Rule 4 (NEW): Gross margin too thin even if technically profitable
    if 0 < gross_margin < 0.1:
        flags.append(f"⚠️ MATH FLAG: Gross margin is only {gross_margin*100:.1f}%. Business is technically profitable but dangerously fragile.")

    # Rule 5 (FIXED): Check ALL risky words with negation detection
    negation_words = ["don't", "dont", "not", "never", "avoid", "without", "stop"]
    risky_words = ["invest", "hire", "expand", "launch", "spend", "purchase", "buy"]

    recommendation_lower = ai_recommendation.lower()
    words_list = recommendation_lower.split()

    found_risky = []
    for word in risky_words:
        if word in recommendation_lower:
            for i, w in enumerate(words_list):
                if word in w:
                    preceding = words_list[max(0, i - 3):i]
                    is_negated = any(neg in preceding for neg in negation_words)
                    if not is_negated:
                        found_risky.append(word)
                    break

    if found_risky and (monthly_profit < 0 or cash_runway < 2):
        risky_str = ", ".join(f"'{w}'" for w in found_risky)
        warnings.append(f"⚠️ GUARDRAIL WARNING: AI recommends {risky_str} but financial position may not support this right now.")

    # Rule 6 (FIXED): guardrail_passed now accounts for warnings too
    guardrail_passed = len(flags) == 0 and len(warnings) == 0

    return {
        "flags": flags,
        "warnings": warnings,
        "monthly_profit": monthly_profit,
        "cash_runway_months": round(cash_runway, 1),
        "cost_ratio_percent": round(cost_ratio * 100, 1),
        "gross_margin_percent": round(gross_margin * 100, 1),
        "guardrail_passed": guardrail_passed
    }