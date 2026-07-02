from scenario_stress_tester import run_scenario_stress_test
from devils_advocate import run_devils_advocate
from dotenv import load_dotenv
load_dotenv() 
import streamlit as st
import json
import os
from google import genai
from framework_matcher import match_framework
from math_guardrail import run_math_guardrail
from confidence_rating import calculate_confidence
from explainability_trace import generate_trace
from indian_sme_context import get_indian_sme_context
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

VALID_CRISIS_TYPES = [
    "Cash flow problems",
    "Sales have dropped significantly",
    "Costs are too high",
    "Losing customers to competitors",
    "Demand has fallen",
    "Operational bottleneck",
    "Owner is the bottleneck"
]


def classify_crisis(free_text: str) -> str:
    prompt = f"""You are a business crisis classifier for Indian SMEs.

A business owner has described their situation. Your ONLY job is to classify it into exactly one of these crisis types:

1. Cash flow problems
2. Sales have dropped significantly (customers/market still exist, but conversion, retention, or competitive positioning has weakened. Example inputs: "sales are down", "we're losing deals we used to win", "revenue dropped this quarter")
3. Costs are too high
4. Losing customers to competitors
5. Demand has fallen (the market itself has shrunk or shifted — structural, not a sales execution problem. Example inputs: "nobody is buying our product anymore", "the whole market has dried up", "demand has completely stalled")
6. Operational bottleneck
7. Owner is the bottleneck

Business situation:
{free_text}

Rules:
- Return ONLY the crisis type string, copied exactly as written above
- No explanation, no punctuation, no quotes, no preamble
- Choose the single best fit"""

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)
    classified = response.text.strip()
    
    if classified not in VALID_CRISIS_TYPES:
        classified = "Cash flow problems"
    
    return classified

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

st.markdown("**Fhttp://localhost:8501/nancial Position (Monthly)**")
col1, col2, col3 = st.columns(3)
with col1:
    monthly_revenue = st.number_input("Revenue (₹)", min_value=0, help="Your total monthly income")

with col2:
    monthly_costs = st.number_input("Costs (₹)", min_value=0, help="Your total monthly expenses")

with col3:
    cash_on_hand = st.number_input("Cash on Hand (₹)", min_value=0, help="Money available right now")

situation_text = st.text_area("Describe your situation",
    placeholder="What is happening with your business? When did it start? What has changed? What have you already tried?",
    height=150)

st.markdown("---")

analyze_button = st.button("🔍 Analyze My Business", use_container_width=True, type="primary")

if analyze_button:
    if situation_text:
        with st.spinner("Running analysis..."):

            crisis_type = classify_crisis(situation_text)
            st.caption(f"🔍 Crisis detected: {crisis_type}")
            st.info("ℹ️ Strategic framework matched deterministically before AI plan generation.")
            # Step 0: Indian SME Context (deterministic, runs before everything)
            sme_context = get_indian_sme_context(
                business_type, crisis_type,
                monthly_revenue, monthly_costs, cash_on_hand
            )

            # Step 1: Confidence
            confidence = calculate_confidence(
                monthly_revenue, monthly_costs, cash_on_hand, situation_text
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
Owner's situation: {situation_text}

Strategic Framework: {framework['framework']}
Framework context: {framework['description']}
Framework key actions: {', '.join(framework['key_actions'])}

Your immediate_action MUST align with and reference the framework key actions above. Do not contradict them.
Confidence Level: {confidence['level']}

Seasonal Market Flags — use these flags to make your advice specific to Indian small business realities:
{chr(10).join(sme_context['all_context']) if sme_context['all_context'] else 'No specific seasonal or market flags this month.'}

Crisis-Specific Indian SME Context — use these framework-specific Indian SME insights to tailor the plan:
{framework.get('indian_sme_context', 'No crisis-specific Indian SME context available.')}

You must respond in this exact JSON format and nothing else:
{{
    "root_cause": "one sentence diagnosis of the core problem",
    "urgency_level": "CRITICAL or HIGH or MEDIUM or LOW",
    "immediate_action": "single most important action to take this week",
    "metric_to_track": "one specific financial metric to measure daily",
    "risk_if_ignored": "what happens in 30 days if nothing changes",
   "realistic_timeline": "honest estimate of how long recovery will take",
    "unified_plan": "2-3 sentence action plan combining the framework actions and your diagnosis into one coherent strategy"
}}

Return only the JSON. No explanation before or after.
"""
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            ai_response = response.text

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

            # --- SCENARIO STRESS TESTER ---
            if monthly_revenue and monthly_costs and cash_on_hand:
                stress_results = run_scenario_stress_test(monthly_revenue, monthly_costs, cash_on_hand)
    
                with st.expander("⚡ Scenario Stress Tests", expanded=False):
                    st.markdown("### What if conditions change?")
                    for scenario in stress_results["scenarios"]:
                        with st.container():
                            icon = {"orange": "🟡", "red": "🔴", "green": "🟢"}.get(scenario["survival_color"], "⚪")
                        st.markdown(f"**{scenario['label']}**")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Monthly Profit", f"₹{scenario['monthly_profit']:,}")
                        with col2:
                            st.metric("Cash Runway", f"{scenario['cash_runway_months']} months")
                        with col3:
                            st.metric("Survival Score", f"{icon} {scenario['survival_label']}")
                        st.divider()

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

        if framework.get("indian_sme_context"):
            st.markdown("**🧠 Crisis-Specific Indian SME Context**")
            context_value = framework["indian_sme_context"]
            if isinstance(context_value, list):
                for item in context_value:
                    st.info(f"• {item}")
            else:
                st.info(context_value)

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










        st.markdown("#### 🤔 Universal Diagnostic Question: **How many days between raw material entering your factory and cash arriving in your bank?** (This measures WIP/inventory-as-trapped-cash)")
        st.markdown("---")





        # New JTBD-style question
        if crisis_type in ["Sales have dropped significantly", "Demand has fallen", "Losing customers to competitors"]:
            st.markdown("#### ❓ JTBD Root-Cause Diagnostic: **What specific 'job' were customers hiring your product to do — and where are they now getting that job done instead?**")
        st.markdown("---")
        # 4. Altman Z-Score checkpoint - Display before other financial flags
        st.markdown("### 🔍 Universal Financial Health Checks")
        st.info("🚨 **Critical Solvency Check:** Always calculate your Altman Z-Score. A score below 1.1 indicates high financial distress and requires immediate attention, regardless of specific crisis type.")

        # Owner Time Audit (E-Myth)
        if crisis_type == "Owner is the bottleneck":
            st.markdown("#### ⏱️ Owner Time Audit: **Of your working hours this week, how many were spent working IN the business (doing tasks) versus ON the business (deciding, delegating, planning)?** If most decisions — even small ones made by staff or family — still route through you for approval, that is the structural bottleneck, not a staffing shortage.")
        st.markdown("---")


        # 9. Vendor credit before external debt
        if crisis_type == "Cash flow problems" or (cash_on_hand / (monthly_costs if monthly_costs > 0 else 1) < 3 and (monthly_revenue - monthly_costs) < 0):
             st.warning("🤝 **Prioritize Vendor Credit:** Before seeking new loans (e.g., ECLGS), aggressively renegotiate payment terms with existing vendors. This is often the fastest, lowest-cost source of temporary liquidity.")
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

        # GUARDRAIL ENFORCEMENT
        if guardrail.get("flags"):
            st.error("🚨 Critical issues detected — read warnings carefully before acting.")
            for flag in guardrail["flags"]:
                st.error(flag)
        if guardrail.get("warnings"):
            st.warning("⚠️ AI advice shown with caution — review flagged items above.")
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
                st.markdown("**🎯 Unified Action Plan**")
                st.success(analysis.get("unified_plan", ""))

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