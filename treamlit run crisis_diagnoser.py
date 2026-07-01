[1mdiff --git a/crisis_diagnoser.py b/crisis_diagnoser.py[m
[1mindex e9ba003..bcfde1c 100644[m
[1m--- a/crisis_diagnoser.py[m
[1m+++ b/crisis_diagnoser.py[m
[36m@@ -30,10 +30,12 @@[m [mdef classify_crisis(free_text: str) -> str:[m
 A business owner has described their situation. Your ONLY job is to classify it into exactly one of these crisis types:[m
 [m
 1. Cash flow problems[m
[31m-2. Sales have dropped significantly[m
[32m+[m
[32m+[m[32m2. Sales have dropped significantly (customers/market still exist, but conversion, retention, or competitive positioning has weakened. Example inputs: "sales are down", "we're losing deals we used to win", "revenue dropped this quarter")[m
 3. Costs are too high[m
 4. Losing customers to competitors[m
[31m-5. Demand has fallen[m
[32m+[m
[32m+[m[32m5. Demand has fallen (the market itself has shrunk or shifted — structural, not a sales execution problem. Example inputs: "nobody is buying our product anymore", "the whole market has dried up", "demand has completely stalled")[m
 6. Operational bottleneck[m
 7. Owner is the bottleneck[m
 [m
[36m@@ -182,15 +184,18 @@[m [mCash on Hand: ₹{cash_on_hand}[m
 Owner's situation: {situation_text}[m
 [m
 Strategic Framework: {framework['framework']}[m
[31m-Framework context: {framework['description']}Framework context: {framework['description']}[m
[32m+[m[32mFramework context: {framework['description']}[m
 Framework key actions: {', '.join(framework['key_actions'])}[m
 [m
 Your immediate_action MUST align with and reference the framework key actions above. Do not contradict them.[m
 Confidence Level: {confidence['level']}[m
 [m
[31m-Indian Market Context — use these flags to make your advice specific to Indian small business realities:[m
[32m+[m[32mSeasonal Market Flags — use these flags to make your advice specific to Indian small business realities:[m
 {chr(10).join(sme_context['all_context']) if sme_context['all_context'] else 'No specific seasonal or market flags this month.'}[m
 [m
[32m+[m[32mCrisis-Specific Indian SME Context — use these framework-specific Indian SME insights to tailor the plan:[m
[32m+[m[32m{framework.get('indian_sme_context', 'No crisis-specific Indian SME context available.')}[m
[32m+[m
 You must respond in this exact JSON format and nothing else:[m
 {{[m
     "root_cause": "one sentence diagnosis of the core problem",[m
[36m@@ -278,6 +283,15 @@[m [mReturn only the JSON. No explanation before or after.[m
             for flag in sme_context["context_flags"]:[m
                 st.warning(f"🏦 {flag}")[m
 [m
[32m+[m[32m        if framework.get("indian_sme_context"):[m
[32m+[m[32m            st.markdown("**🧠 Crisis-Specific Indian SME Context**")[m
[32m+[m[32m            context_value = framework["indian_sme_context"][m
[32m+[m[32m            if isinstance(context_value, list):[m
[32m+[m[32m                for item in context_value:[m
[32m+[m[32m                    st.info(f"• {item}")[m
[32m+[m[32m            else:[m
[32m+[m[32m                st.info(context_value)[m
[32m+[m
         if sme_context["seasonal_alerts"]:[m
             st.markdown("**📅 Seasonal Alerts**")[m
             for alert in sme_context["seasonal_alerts"]:[m
