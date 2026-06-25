def run_scenario_stress_test(monthly_revenue, monthly_costs, cash_on_hand):
    """
    Pure Python. Zero LLM. 
    Calculates three financial futures deterministically.
    This is what makes a business owner trust the tool —
    they can see exactly what happens if things get worse.
    """

    def calculate_scenario(revenue, costs, cash, label):
        monthly_profit = revenue - costs
        cash_runway = cash / costs if costs > 0 else 0
        cost_ratio = costs / revenue if revenue > 0 else 1
        gross_margin = (revenue - costs) / revenue if revenue > 0 else 0

        # Survival score — pure deterministic math
        survival_score = 0

        if cash_runway >= 6:
            survival_score += 30
        elif cash_runway >= 3:
            survival_score += 20
        elif cash_runway >= 1:
            survival_score += 10
        else:
            survival_score += 0

        if monthly_profit > 0:
            survival_score += 30
        elif monthly_profit > -revenue * 0.1:
            survival_score += 15
        else:
            survival_score += 0

        if gross_margin >= 0.3:
            survival_score += 25
        elif gross_margin >= 0.1:
            survival_score += 15
        elif gross_margin >= 0:
            survival_score += 5
        else:
            survival_score += 0

        if cost_ratio <= 0.7:
            survival_score += 15
        elif cost_ratio <= 0.9:
            survival_score += 8
        else:
            survival_score += 0

        # Survival label
        if survival_score >= 75:
            survival_label = "STABLE"
            survival_color = "green"
        elif survival_score >= 50:
            survival_label = "VULNERABLE"
            survival_color = "orange"
        elif survival_score >= 25:
            survival_label = "CRITICAL"
            survival_color = "red"
        else:
            survival_label = "TERMINAL"
            survival_color = "darkred"

        # Months to break even if losing money
        if monthly_profit < 0 and revenue > 0:
            revenue_gap = costs - revenue
            months_to_breakeven = cash / revenue_gap if revenue_gap > 0 else 0
        else:
            months_to_breakeven = 0

        return {
            "label": label,
            "monthly_revenue": round(revenue),
            "monthly_costs": round(costs),
            "monthly_profit": round(monthly_profit),
            "cash_runway_months": round(cash_runway, 1),
            "gross_margin_percent": round(gross_margin * 100, 1),
            "cost_ratio_percent": round(cost_ratio * 100, 1),
            "survival_score": survival_score,
            "survival_label": survival_label,
            "survival_color": survival_color,
            "months_to_breakeven": round(months_to_breakeven, 1)
        }

    # Three deterministic scenarios
    base = calculate_scenario(
        monthly_revenue,
        monthly_costs,
        cash_on_hand,
        "Base Case (Current Trajectory)"
    )

    optimistic = calculate_scenario(
        monthly_revenue * 1.15,   # 15% revenue increase
        monthly_costs * 0.95,     # 5% cost reduction
        cash_on_hand,
        "Optimistic (Revenue +15%, Costs -5%)"
    )

    pessimistic = calculate_scenario(
        monthly_revenue * 0.80,   # 20% revenue drop
        monthly_costs * 1.10,     # 10% cost increase
        cash_on_hand,
        "Pessimistic (Revenue -20%, Costs +10%)"
    )

    return {
        "base": base,
        "optimistic": optimistic,
        "pessimistic": pessimistic,
        "scenarios": [optimistic, base, pessimistic]
    }