[1mdiff --git a/crisis_diagnoser.py b/crisis_diagnoser.py[m
[1mindex 66118e3..2cb3366 100644[m
[1m--- a/crisis_diagnoser.py[m
[1m+++ b/crisis_diagnoser.py[m
[36m@@ -156,6 +156,7 @@[m [mif analyze_button:[m
 [m
             crisis_type = classify_crisis(situation_text)[m
             st.caption(f"🔍 Crisis detected: {crisis_type}")[m
[32m+[m[32m            st.info("ℹ️ Strategic framework matched deterministically before AI plan generation.")[m
             # Step 0: Indian SME Context (deterministic, runs before everything)[m
             sme_context = get_indian_sme_context([m
                 business_type, crisis_type,[m
[36m@@ -318,57 +319,17 @@[m [mReturn only the JSON. No explanation before or after.[m
 [m
 [m
 [m
[31m-        st.markdown("#### 🤔 Universal Diagnostic Question: **How many many days between raw material entering your factory and cash arriving in your bank?** (This measures WIP/inventory-as-trapped-cash)")[m
[32m+[m[32m        st.markdown("#### 🤔 Universal Diagnostic Question: **How many days between raw material entering your factory and cash arriving in your bank?** (This measures WIP/inventory-as-trapped-cash)")[m
         st.markdown("---")[m
 [m
 [m
 [m
 [m
 [m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
[31m-[m
         # New JTBD-style question[m
         if crisis_type in ["Sales have dropped significantly", "Demand has fallen", "Losing customers to competitors"]:[m
             st.markdown("#### ❓ JTBD Root-Cause Diagnostic: **What specific 'job' were customers hiring your product to do — and where are they now getting that job done instead?**")[m
[32m+[m[32m            st.warning("🔬 Structural vs. Cyclical Diagnosis: Apply Grove's silver bullet test — if your most feared competitor had one move to destroy you, what would it be? If they already made it, you are at a structural inflection point requiring a strategic shift, not just optimization.")[m
         st.markdown("---")[m
         # 4. Altman Z-Score checkpoint - Display before other financial flags[m
         st.markdown("### 🔍 Universal Financial Health Checks")[m
[36m@@ -407,13 +368,10 @@[m [mReturn only the JSON. No explanation before or after.[m
 [m
 [m
 [m
[31m-[m
[31m-[m
[31m-[m
             clean = ai_response.strip()[m
             if clean.startswith("```"):[m
                 clean = clean.split("```")[1][m
[31m- GST ITC            if clean.startswith("json"):[m
[32m+[m[32m            if clean.startswith("json"):[m
                 clean = clean[4:][m
             analysis = json.loads(clean)[m
 [m
