from devils_advocate import run_devils_advocate
from dotenv import load_dotenv
load_dotenv() 
import streamlit as st
import json
import os
from groq import Groq
from framework_matcher import match_framework
from math_guardrail import run_math_guardrail
from confidence_rating import calculate_confidence
from explainability_trace import generate_trace
from indian_sme_context import get_indian_sme_context

# Page config
st.set_page_config(
    page_title="Business Crisis Advisor",
    page_icon="📊",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main { padding: 2rem 1rem; }
    .header-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .header-title {
        color: #e94560;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .header-subtitle {
        color: #a8b2d8;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    .section-card {
        background: #f8f9fa;
        border-left: 4px solid #e94560;
        padding: 1rem 1.2rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
        color: #1a1a2e;
    }
    .footer-text {
        text-align: center;
        color: #888;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <p class="header-title">📊 Business Crisis Advisor</p>
    <p class="header-subtitle">AI-powered strategic analysis for small business owners in crisis</p>
</div>
""", unsafe_allow_html=True)

# Intro
st.markdown("""
<div class="section-card">
    This tool diagnoses your business crisis, matches it to a proven strategic framework, 
    checks financial reality, and gives you a precise action plan — not generic advice.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Input form
st.subheader("📝 Tell Us About Your Situation")

col1, col2 = st.columns(2)
with col1:
    business_type = st.selectbox("Business Type",
        ["Retail", "Restaurant", "Service Business", "Manufacturing", "Other"])
with col2:
    crisis_type = st.selectbox("Primary Crisis",
        ["Sales have dropped significantly",
         "Cash flow problems",
         "Costs are too high",
         "Losing customers to competitors",
         "Demand has fallen"])

st.markdown("**Financial Position (Monthly)**")
col1, col2, col3 = st.columns(3)
with col1:
    monthly_revenue = st.number_input("Revenue (₹)", min_value=0, help="Your total monthly income")
with col2:
    monthly_costs = st.number_input("Costs (₹)", min_value=0, help="Your total monthly expenses")
with col3:
    cash_on_hand = st.number_input("Cash on Hand (₹)", min_value=0, help="Money available right now")

description = st.text_area("Describe Your Situation",
    placeholder="Be specific — when did this start? What changed? What have you already tried?",
    height=120)

st.markdown("---")

analyze_button = st.button("🔍 Analyze My Business", use_container_width=True, type="primary")

if analyze_button:
    if description:
        with st.spinner("Running analysis..."):

            # Step 0: Indian SME Context (deterministic, runs before everything)
            sme_context = get_indian_sme_context(
                business_type, crisis_type,
                monthly_revenue, monthly_costs, cash_on_hand
            )

            # Step 1: Confidence
            confidence = calculate_confidence(
                monthly_revenue, monthly_costs, cash_on_hand, description
            )

            # Step 2: Framework
            framework = match_framework(crisis_type, monthly_revenue, monthly_costs, cash_on_hand)

            # Step 3: AI
            prompt = f"""
You are a business crisis advisor analyzing a specific situation.

Business Type: {business_type}
Crisis: {crisis_type}
Monthly Revenue: ₹{monthly_revenue}
Monthly Costs: ₹{monthly_costs}
Cash on Hand: ₹{cash_on_hand}
Owner's Description: {description}

Strategic Framework: {framework['framework']}
Framework context: {framework['description']}
Confidence Level: {confidence['level']}

Indian Market Context — use these flags to make your advice specific to Indian small business realities:
{chr(10).join(sme_context['all_context']) if sme_context['all_context'] else 'No specific seasonal or market flags this month.'}

You must respond in this exact JSON format and nothing else:
{{
    "root_cause": "one sentence diagnosis of the core problem",
    "urgency_level": "CRITICAL or HIGH or MEDIUM or LOW",
    "immediate_action": "single most important action to take this week",
    "metric_to_track": "one specific financial metric to measure daily",
    "risk_if_ignored": "what happens in 30 days if nothing changes",
    "realistic_timeline": "honest estimate of how long recovery will take"
}}

Return only the JSON. No explanation before or after.
"""
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            ai_response = response.choices[0].message.content

            # Step 4: Guardrail
            guardrail = run_math_guardrail(
                monthly_revenue, monthly_costs, cash_on_hand, ai_response
            )

           

           # Step 5: Devil's Advocate
            devils_advocate_raw = run_devils_advocate(
                business_type, crisis_type,
                monthly_revenue, monthly_costs, cash_on_hand,
                ai_response, framework['framework'], guardrail
            )

            # Step 6: Trace
            trace = generate_trace(
                business_type, crisis_type, monthly_revenue,
                monthly_costs, cash_on_hand, framework,
                guardrail, confidence
            )

        # --- DISPLAY RESULTS ---

        st.markdown("---")
        st.subheader("📊 Analysis Results")

        # Confidence
        if confidence["level"] == "HIGH":
            st.success(f"✅ Analysis Confidence: {confidence['level']} ({confidence['score']}/100) — {confidence['summary']}")
        elif confidence["level"] == "MEDIUM":
            st.warning(f"⚠️ Analysis Confidence: {confidence['level']} ({confidence['score']}/100) — {confidence['summary']}")
        else:
            st.error(f"❌ Analysis Confidence: {confidence['level']} ({confidence['score']}/100) — {confidence['summary']}")

        # Financial flags
        if guardrail["flags"] or guardrail["warnings"]:
            st.markdown("**⚠️ Financial Reality Check**")
            for flag in guardrail["flags"]:
                st.error(flag)
            for warning in guardrail["warnings"]:
                st.warning(warning)

        # Indian SME Context Display
        if sme_context["context_flags"]:
            st.markdown("**🇮🇳 Indian Market Flags**")
            for flag in sme_context["context_flags"]:
                st.warning(f"🏦 {flag}")

        if sme_context["seasonal_alerts"]:
            st.markdown("**📅 Seasonal Alerts**")
            for alert in sme_context["seasonal_alerts"]:
                st.info(f"🗓️ {alert}")

        if sme_context["scheme_suggestions"]:
            st.markdown("**💡 Government Schemes Available To You**")
            for scheme in sme_context["scheme_suggestions"]:
                st.success(f"✅ {scheme}")

        # Financial position
        st.markdown("**💰 Your Financial Position**")
        col1, col2, col3 = st.columns(3)
        col1.metric("Monthly Profit/Loss", f"₹{guardrail['monthly_profit']:,}")
        col2.metric("Cash Runway", f"{guardrail['cash_runway_months']} months")
        col3.metric("Cost Ratio", f"{guardrail['cost_ratio_percent']}%")

        st.markdown("---")

        # Framework
        st.markdown(f"**🎯 Strategic Framework: {framework['framework']}**")
        priority_color = "🔴" if framework['priority'] == "CRITICAL" else "🟡" if framework['priority'] == "HIGH" else "🟢"
        st.markdown(f"{priority_color} Priority: **{framework['priority']}**")
        st.info(framework['description'])

        st.markdown("**Key Actions from Framework:**")
        for action in framework['key_actions']:
            st.markdown(f"• {action}")

        st.markdown("---")

        # AI Analysis
        st.markdown("**🤖 AI Analysis**")
        try:
            clean = ai_response.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            analysis = json.loads(clean)

            urgency = analysis.get("urgency_level", "MEDIUM")
            if urgency == "CRITICAL":
                st.error(f"🚨 Urgency Level: {urgency}")
            elif urgency == "HIGH":
                st.warning(f"⚠️ Urgency Level: {urgency}")
            else:
                st.info(f"ℹ️ Urgency Level: {urgency}")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🔍 Root Cause**")
                st.write(analysis.get("root_cause", ""))
                st.markdown("**📈 Metric to Track Daily**")
                st.write(analysis.get("metric_to_track", ""))
                st.markdown("**⏱️ Recovery Timeline**")
                st.write(analysis.get("realistic_timeline", ""))
            with col2:
                st.markdown("**✅ Immediate Action This Week**")
                st.success(analysis.get("immediate_action", ""))
                st.markdown("**🚨 Risk If Nothing Changes**")
                st.error(analysis.get("risk_if_ignored", ""))

        except:
            st.write(ai_response)

        st.markdown("---")

        # Devil's Advocate
        st.markdown("**😈 Devil's Advocate — Why This Advice Could Fail**")
        st.caption("A second AI pass that challenges the recommendation before you act on it")
        try:
            clean_da = devils_advocate_raw.strip()
            if clean_da.startswith("```"):
                clean_da = clean_da.split("```")[1]
                if clean_da.startswith("json"):
                    clean_da = clean_da[4:]
            da = json.loads(clean_da)

            verdict_confidence = da.get("confidence_in_recommendation", "MEDIUM")
            if verdict_confidence == "LOW":
                st.error(f"🚨 Confidence in Recommendation: {verdict_confidence}")
            elif verdict_confidence == "MEDIUM":
                st.warning(f"⚠️ Confidence in Recommendation: {verdict_confidence}")
            else:
                st.success(f"✅ Confidence in Recommendation: {verdict_confidence}")

            st.markdown("**⚡ One Line Verdict**")
            st.write(da.get("one_line_verdict", ""))

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🔴 Biggest Flaw**")
                st.error(da.get("biggest_flaw", ""))
                st.markdown("**🕳️ Overlooked Risk**")
                st.warning(da.get("overlooked_risk", ""))
            with col2:
                st.markdown("**✅ Better Alternative**")
                st.success(da.get("better_alternative", ""))

        except:
            st.write(devils_advocate_raw)

        # Explainability
        st.markdown("**🔎 How This Analysis Was Built**")
        st.caption("Every decision made by this tool is transparent and explainable")
        for step in trace:
            with st.expander(step["step"]):
                st.write(f"**Decision:** {step['decision']}")
                st.write(f"**Reason:** {step['reason']}")

        # Footer
        st.markdown("""
        <div class="footer-text">
            Built by Swatantra · Business Crisis Advisor v1.0 · Not a substitute for professional financial advice
        </div>
        """, unsafe_allow_html=True)

    else:
        st.warning("⚠️ Please describe your situation before analyzing.")