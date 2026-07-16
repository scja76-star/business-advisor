def generate_trace(business_type, crisis_type, monthly_revenue, 
                   monthly_cogs, monthly_operating_expenses, cash_on_hand, framework,
                   guardrail, confidence):

    trace = []

    # Step 1: Input reading
    trace.append({
        "step": "Step 1: Situation Read",
        "decision": f"Identified a {business_type} business facing '{crisis_type}'",
        "reason": "Business type and crisis type determine which analytical path is taken"
    })

    # Step 2: Framework selection reasoning
    trace.append({
        "step": "Step 2: Framework Selected",
        "decision": f"Applied '{framework['framework']}'",
        "reason": f"Selected because: {framework['description']}"
    })

    # Step 3: Financial assessment
    profit = profit = guardrail.get("net_profit", monthly_revenue - (monthly_cogs + monthly_operating_expenses))
    if profit < 0:
        financial_note = f"Business is loss-making by ₹{abs(profit):,}/month — survival protocols prioritized"
    elif profit == 0:
        financial_note = "Business is breaking even — stability is fragile"
    else:
        financial_note = f"Business has ₹{profit:,}/month profit — focus can be on recovery not just survival"

    trace.append({
        "step": "Step 3: Financial Assessment",
        "decision": financial_note,
        "reason": "Profit/loss position determines urgency and type of recommendations given"
    })

    # Step 4: Guardrail decision
    if guardrail["guardrail_passed"]:
        guardrail_note = "No financial red flags detected — AI recommendations shown without restrictions"
    else:
        guardrail_note = f"{len(guardrail['flags'])} financial flag(s) raised — recommendations filtered for financial reality"

    trace.append({
        "step": "Step 4: Math Guardrail",
        "decision": guardrail_note,
        "reason": "Guardrail ensures AI recommendations are possible given actual financial position"
    })

    # Step 5: Confidence decision
    trace.append({
        "step": "Step 5: Confidence Rated",
        "decision": f"Confidence set to {confidence['level']} ({confidence['score']}/100)",
        "reason": confidence['summary']
    })

    return trace