import os
from google import genai
from dotenv import load_dotenv
load_dotenv()

def run_devils_advocate(
    business_type, crisis_type,
    monthly_revenue, monthly_cogs, monthly_operating_expenses, cash_on_hand,
    ai_recommendation, framework_name, guardrail_result
):
    """
    Second-pass critique engine. Runs AFTER the main AI recommendation.
    Challenges the recommendation before the user sees it.
    This is what separates a trusted advisor from a yes-man chatbot.
    """

    monthly_profit = guardrail_result.get("net_profit", monthly_revenue - (monthly_cogs + monthly_operating_expenses))
    cash_runway = guardrail_result.get("cash_runway_months", 0)
    gross_margin = guardrail_result.get("gross_margin_percent", 0)

    # Build deterministic risk context first
    risk_context = []

    if monthly_profit < 0:
        risk_context.append(f"Business is losing ₹{abs(monthly_profit):,} per month")
    if cash_runway < 2:
        risk_context.append(f"Only {cash_runway} months of cash remaining")
    if gross_margin < 10:
        risk_context.append(f"Gross margin is dangerously thin at {gross_margin}%")
    if not guardrail_result.get("guardrail_passed", True):
        risk_context.append("Math guardrail flagged this recommendation")

    risk_summary = ". ".join(risk_context) if risk_context else "No critical financial flags"

    prompt = f"""You are a ruthless but fair business critic. A business advisor just gave a recommendation to a struggling small business owner in India. Your job is to find every way this recommendation could FAIL or HARM the business.

Business Context:
- Type: {business_type}
- Crisis: {crisis_type}
- Monthly Revenue: ₹{monthly_revenue}
- Monthly COGS: ₹{monthly_cogs}
- Monthly Operating Expenses: ₹{monthly_operating_expenses}
- Cash on Hand: ₹{cash_on_hand}
- Financial Risk Flags: {risk_summary}
- Framework Used: {framework_name}

The AI Recommendation:
{ai_recommendation}

You must respond in this exact JSON format and nothing else:
{{
    "biggest_flaw": "the single most dangerous assumption in this recommendation",
    "overlooked_risk": "one critical risk the recommendation completely ignores",
    "better_alternative": "one concrete alternative approach that is more conservative and realistic",
    "confidence_in_recommendation": "LOW or MEDIUM or HIGH — your honest assessment of whether this advice is trustworthy",
    "one_line_verdict": "one brutally honest sentence summarizing whether this advice should be followed"
}}

Return only the JSON. No explanation before or after."""

    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text