import datetime

def get_indian_sme_context(business_type, crisis_type, monthly_revenue, monthly_cogs, monthly_operating_expenses, cash_on_hand):
    """
    Deterministically generates Indian SME-specific context
    before the LLM sees any data. This is what makes this tool
    different from every generic AI business advisor.
    """

    context_flags = []
    seasonal_alerts = []
    scheme_suggestions = []

    current_month = datetime.datetime.now().month
    monthly_total_costs = monthly_cogs + monthly_operating_expenses
    monthly_profit = monthly_revenue - monthly_total_costs
    cash_runway = cash_on_hand / monthly_total_costs if monthly_total_costs > 0 else 0
    annual_revenue = monthly_revenue * 12

    # === SEASONAL PRESSURE FLAGS ===

    gst_filing_months = {
        1: "Q3 GST filing (Oct-Dec)",
        4: "Q4 GST filing (Jan-Mar)",
        7: "Q1 GST filing (Apr-Jun)",
        10: "Q2 GST filing (Jul-Sep)"
    }
    if current_month in gst_filing_months:
        context_flags.append(f"GST PRESSURE: {gst_filing_months[current_month]} deadline this month — expect cash outflow beyond normal costs.")

    if current_month in [8, 9, 10] and business_type in ["Retail", "Manufacturing"]:
        seasonal_alerts.append("DIWALI PREP SEASON: Inventory investment required now but peak revenue is 4-8 weeks away. Cash gap is normal but must be actively managed.")

    if current_month in [11, 12] and business_type in ["Retail", "Restaurant"]:
        seasonal_alerts.append("POST-DIWALI CYCLE: Revenue typically drops 20-40% from October peak. This is seasonal not structural — but cash must be conserved now.")

    if current_month in [1, 2, 3]:
        context_flags.append("YEAR-END PRESSURE: Advance tax and audit season — additional cash outflow likely before March 31.")

    if current_month in [4, 5, 6] and business_type == "Restaurant":
        seasonal_alerts.append("SUMMER SLOWDOWN: Footfall drops in peak heat months in north India. Plan for 15-25% revenue dip.")

    # === WORKING CAPITAL FLAGS ===

    if crisis_type == "Cash flow problems":
        context_flags.append("VENDOR CREDIT FIRST: Negotiate 30-60 day payment extension with vendors before touching cash reserves or seeking loans. Standard practice in Indian SME context.")

    if cash_runway < 3 and monthly_profit < 0:
        context_flags.append("COLLECTIONS PRIORITY: Chase outstanding receivables immediately. Indian SME average collection delay is 45-90 days — recovering one large payment can change survival odds.")

    # === GOVERNMENT SCHEME FLAGS ===

    if annual_revenue < 2500000:
        scheme_suggestions.append("MUDRA LOAN: Collateral-free loans up to ₹10L for micro businesses. Apply via any PSU bank. Relevant to your revenue size.")

    if business_type in ["Retail", "Service Business"] and annual_revenue < 1200000:
        scheme_suggestions.append("PM SVANidhi Scheme: Working capital loan for small vendors. Low interest, no collateral required.")

    if crisis_type == "Costs are too high" and business_type == "Manufacturing":
        scheme_suggestions.append("MSME Samadhaan Portal: If delayed payments from larger buyers are straining you, file for recovery under the MSME Act.")
    if len(scheme_suggestions) >= 1:
        scheme_suggestions.append("SCHEME STACKING: These government schemes are not mutually exclusive. Udyam Registration is often a prerequisite for MUDRA and ECLGS eligibility — complete it first if not already done. GeM and ONDC marketplace listings build revenue history that strengthens future loan applications. Combine credit relief schemes with visibility schemes rather than relying on just one.")

    if annual_revenue < 5000000:
        scheme_suggestions.append("FAMILY BUSINESS DYNAMICS: In owner-led and family-run SMEs, decision authority is often informally shared across family members regardless of formal titles. Crisis response plans should account for who actually holds veto power on financial decisions, not just who is listed as owner.")
    return {
        "context_flags": context_flags,
        "seasonal_alerts": seasonal_alerts,
        "scheme_suggestions": scheme_suggestions,
        "all_context": context_flags + seasonal_alerts + scheme_suggestions
    }
    