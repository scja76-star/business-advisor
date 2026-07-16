def run_scenario_stress_test(monthly_revenue, monthly_cogs, monthly_operating_expenses, cash_on_hand):
    """
    Pure Python. Zero LLM.
    Calculates three financial futures deterministically.
    """

    def calculate_scenario(revenue, cogs, opex, cash, label):
        total_costs = cogs + opex
        gross_profit = revenue - cogs
        net_profit = gross_profit - opex
        cash_runway = cash / total_costs if total_costs > 0 else 0
        cost_ratio = total_costs / revenue if revenue > 0 else 1
        gross_margin = gross_profit / revenue if revenue > 0 else 0

        survival_score = 0
        if cash_runway >= 6: survival_score += 30
        elif cash_runway >= 3: survival_score += 20
        elif cash_runway >= 1: survival_score += 10

        if net_profit > 0: survival_score += 30
        elif net_profit > -revenue * 0.1: survival_score += 15

        if gross_margin >= 0.3: survival_score += 25
        elif gross_margin >= 0.1: survival_score += 15
        elif gross_margin >= 0: survival_score += 5

        if cost_ratio <= 0.7: survival_score += 15
        elif cost_ratio <= 0.9: survival_score += 8

        if survival_score >= 75:
            survival_label, survival_color = "STABLE", "green"
        elif survival_score >= 50:
            survival_label, survival_color = "VULNERABLE", "orange"
        elif survival_score >= 25:
            survival_label, survival_color = "CRITICAL", "red"
        else:
            survival_label, survival_color = "TERMINAL", "darkred"

        if net_profit < 0 and revenue > 0:
            revenue_gap = total_costs - revenue
            months_to_breakeven = cash / revenue_gap if revenue_gap > 0 else 0
        else:
            months_to_breakeven = 0

        return {
            "label": label,
            "monthly_revenue": round(revenue),
            "monthly_cogs": round(cogs),
            "monthly_operating_expenses": round(opex),
            "net_profit": round(net_profit),
            "cash_runway_months": round(cash_runway, 1),
            "gross_margin_percent": round(gross_margin * 100, 1),
            "cost_ratio_percent": round(cost_ratio * 100, 1),
            "survival_score": survival_score,
            "survival_label": survival_label,
            "survival_color": survival_color,
            "months_to_breakeven": round(months_to_breakeven, 1)
        }

    base = calculate_scenario(monthly_revenue, monthly_cogs, monthly_operating_expenses, cash_on_hand, "Base Case (Current Trajectory)")

    # COGS scales with revenue (variable cost); opex adjusts via efficiency (fixed cost)
    optimistic = calculate_scenario(
        monthly_revenue * 1.15,
        monthly_cogs * 1.15 * 0.95,
        monthly_operating_expenses * 0.95,
        cash_on_hand,
        "Optimistic (Revenue +15%, Efficiency +5%)"
    )

    pessimistic = calculate_scenario(
        monthly_revenue * 0.80,
        monthly_cogs * 0.80 * 1.10,
        monthly_operating_expenses * 1.10,
        cash_on_hand,
        "Pessimistic (Revenue -20%, Costs +10%)"
    )

    return {"base": base, "optimistic": optimistic, "pessimistic": pessimistic, "scenarios": [optimistic, base, pessimistic]}