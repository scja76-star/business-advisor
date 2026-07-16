def run_math_guardrail(monthly_revenue, monthly_cogs, monthly_operating_expenses, cash_on_hand, ai_recommendation):

    warnings = []
    flags = []

    # Correct calculations — COGS and opex kept separate
    gross_profit = monthly_revenue - monthly_cogs
    gross_margin = gross_profit / monthly_revenue if monthly_revenue > 0 else 0
    net_profit = gross_profit - monthly_operating_expenses
    monthly_total_costs = monthly_cogs + monthly_operating_expenses
    cash_runway = cash_on_hand / monthly_total_costs if monthly_total_costs > 0 else 0
    cost_ratio = monthly_total_costs / monthly_revenue if monthly_revenue > 0 else 1

    # Rule 1: Business is losing money (net, not gross)
    if net_profit < 0:
        warnings.append(f"⚠️ Business is losing ₹{abs(net_profit):,}/month after all expenses. AI advice shown with caution.")

    # Rule 2: Less than 1 month cash runway
    if cash_runway < 1 and cash_on_hand > 0:
        flags.append(f"🚨 CRITICAL: Only {cash_runway:.1f} months of cash remaining. Survival is the only priority.")

    # Rule 3: Cost ratio dangerously high
    if cost_ratio > 0.9:
        warnings.append(f"⚠️ Total costs are {cost_ratio*100:.0f}% of revenue. Very little margin for error.")

    # Rule 4: Thin gross margin — RECONCILED, not standalone
    if 0 < gross_margin < 0.1:
        if net_profit > 0 and cash_runway < 3:
            warnings.append(f"⚠️ Gross margin is only {gross_margin*100:.1f}%. You're net profitable (₹{net_profit:,}/month) but thin margins plus low cash runway ({cash_runway:.1f} months) mean profit isn't converting to available cash — likely tied up in inventory or receivables.")
        else:
            warnings.append(f"⚠️ Gross margin is only {gross_margin*100:.1f}%. Technically profitable but fragile.")

    # Rule 5: risky words (unchanged logic, now keyed off correct net_profit)
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
    if found_risky and (net_profit < 0 or cash_runway < 2):
        risky_str = ", ".join(f"'{w}'" for w in found_risky)
        warnings.append(f"⚠️ GUARDRAIL WARNING: AI recommends {risky_str} but financial position may not support this right now.")

    guardrail_passed = len(flags) == 0 and len(warnings) == 0

    return {
        "flags": flags,
        "warnings": warnings,
        "gross_profit": gross_profit,
        "gross_margin_percent": round(gross_margin * 100, 1),
        "net_profit": net_profit,
        "cash_runway_months": round(cash_runway, 1),
        "cost_ratio_percent": round(cost_ratio * 100, 1),
        "guardrail_passed": guardrail_passed,
        "math_trace": (
            f"Revenue: ₹{monthly_revenue:,}\n"
            f"− COGS: ₹{monthly_cogs:,}\n"
            f"= Gross Profit: ₹{gross_profit:,} (Margin: {gross_margin*100:.1f}%)\n"
            f"− Operating Expenses: ₹{monthly_operating_expenses:,}\n"
            f"= Net Profit: ₹{net_profit:,}"
        )
    }