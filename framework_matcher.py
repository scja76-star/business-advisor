def match_framework(crisis_type, monthly_revenue, monthly_costs, cash_on_hand):

    # Calculate key financial indicators
    profit = monthly_revenue - monthly_costs
    cash_runway = cash_on_hand / monthly_costs if monthly_costs > 0 else 0
    cost_ratio = monthly_costs / monthly_revenue if monthly_revenue > 0 else 1
    gross_margin = (monthly_revenue - monthly_costs) / monthly_revenue if monthly_revenue > 0 else 0

    # ─────────────────────────────────────────────────────────────
    # CRISIS TYPE 1: CASH FLOW PROBLEMS
    # ─────────────────────────────────────────────────────────────
    if crisis_type == "Cash flow problems":

        return {
            "framework": "Theory of Constraints / DBR (working capital synchronization) + Lean/TPS (WIP elimination) + DuPont Analysis (ROE decomposition)",
            "literature_basis": (
                "Eliyahu Goldratt — The Goal; Taiichi Ohno — Toyota Production System; DuPont Analysis methodology (1920s); Altman Z-Score — Edward Altman (1968)"
            ),
            "description": (
                "Cash flow crises in manufacturing SMEs are almost never a revenue problem. They are a working capital trap — cash is physically locked inside excess WIP inventory, idle machinery, and large batch overproduction. Financial statements mask the damage until the SME is days from default."
            ),
            "elite_principle": (
                "An Indian SME does not run out of cash because it lacks sales. It runs out of cash because its factory floor converts raw material into finished goods in weeks not days. Every extra day of WIP is a silent loan the owner gave their own factory — at zero interest, with no repayment date."
            ),
            "indian_sme_context": (
                "(1) Altman Z-Score survival threshold for Indian SMEs is 1.1. Calculate before doing anything else. (2) Abandon EOQ bulk purchasing logic. (3) ECLGS credit line only to bridge gap while fixing WIP velocity — not to fund continued overproduction. (4) Convert raw material to cash in days not weeks."
            ),
            "priority": "CRITICAL — cash flow failure is #1 cause of SME death",
            "key_actions": [
                "Calculate Altman Z-Score today. Below 1.1 means danger zone.",
                "Walk floor, find where WIP physically piles up. That pile is your trapped cash.",
                "Halt raw material releases until bottleneck signals it can consume them",
                "Cut batch sizes. Run SMED workshop to get changeover under 10 minutes",
                "Run DuPont decomposition: is ROE driven by real efficiency or debt leverage?",
                "Liquidate dead inventory and idle assets. Pay down highest-interest debt first."
            ],
            "decision_rule": (
                "Apply when owner reports cash shortage despite decent sales, factory has visible WIP piles, creditors being delayed, or Altman Z-Score approaches 1.1. Trigger question — How many days between raw material entering factory and cash arriving in bank?"
            )
        }

    # ─────────────────────────────────────────────────────────────
    # CRISIS TYPE 2: SALES HAVE DROPPED SIGNIFICANTLY
    # ─────────────────────────────────────────────────────────────
    elif crisis_type == "Sales have dropped significantly":
        return {
            "framework": "Jobs To Be Done (Christensen) as primary diagnostic; Porter's Five Forces for structural threat analysis; Strategic Inflection Points (Grove) for 10X shift detection; Porter's Generic Strategies for repositioning",
            "literature_basis": (
                "Clayton Christensen — JTBD theory; Michael Porter — Five Forces, Generic Strategies; Andy Grove — \"Only The Paranoid Survive\"; Kim & Mauborgne — Blue Ocean Strategy; Altman Z-Score"
            ),
            "description": (
                "Sales drops are misdiagnosed as marketing problems. They are almost always structural — the product was fired by customers for a better substitute, the industry hit a strategic inflection point, or the firm drifted into the fatal \"stuck in the middle\" zone with no defensible position."
            ),
            "elite_principle": (
                "Customers do not buy products. They hire them to make progress in a specific struggling moment. When sales drop, the product was not beaten by a competitor — it was fired by the customer for failing to do the job. Find the job. Redesign the product around it. — Christensen, JTBD"
            ),
            "indian_sme_context": (
                "[DERIVED — verify all] (1) GST implementation created a permanent structural inflection point for Indian SMEs — competitors who formalized and claimed ITC gained a structural cost advantage. If sales dropped post-2017, check if this is the real cause. (2) GeM (Government e-Marketplace) portal — if your SME sells B2G, dropping sales may reflect procurement shifting to GeM-registered competitors. Register immediately. (3) Rajasthan-specific: textile and auto parts SMEs face substitution threat from Chinese imports via informal channels. JTBD analysis will reveal if price is the job — if yes, cost leadership is the only viable path. (4) Udyam registration unlocks priority sector lending — if sales drop is forcing a credit crunch, this is the fastest legitimate financing lever."
            ),
            "priority": "HIGH — sustained sales decline triggers cash flow crisis within 60-90 days for most manufacturing SMEs",
            "key_actions": [
                "Interview your last 5 lost customers. One specific question only: what did you hire instead of us, and why? This is your JTBD diagnostic.",
                "Run Porter's Five Forces on your segment. Specifically: has a substitute product structurally entered your market, or is this a cyclical dip?",
                "Apply Grove's silver bullet test: if your most feared competitor had one move to destroy you, what would it be? If they have already made that move, you are at an inflection point.",
                "Calculate your Altman Z-Score. If below 1.1, sales recovery must happen in under 90 days or financial distress compounds.",
                "Force a binary strategic choice using Porter's Generic Strategies: cost leadership or differentiation. Being stuck in the middle during a sales drop is a death sentence.",
                "Check GeM registration status and compare your pricing to listed competitors on the portal."
            ],
            "decision_rule": (
                "Apply when: sales volume drops 20%+ over two consecutive quarters, new competitors appear with structurally lower prices, or existing customers reduce order sizes without explanation. Trigger question — 'Did our customers stop buying from everyone, or did they stop buying specifically from us?'"
            )
        }

    # ─────────────────────────────────────────────────────────────
    # CRISIS TYPE 3: COSTS ARE TOO HIGH
    # ─────────────────────────────────────────────────────────────
    elif crisis_type == "Costs are too high":
        return {
            "framework": "Zero-Based Budgeting (ZBB) as primary cost elimination tool; Value Chain Analysis for cost location; Blue Ocean ERRC Grid for cost-value restructuring; TOC for WIP cost reduction",
            "literature_basis": (
                "Zero-Based Budgeting — Peter Pyhrr (1970); Michael Porter — Value Chain Analysis; Kim & Mauborgne — \"Blue Ocean Strategy\"; Eliyahu Goldratt — TOC"
            ),
            "description": (
                "Cost crises in manufacturing SMEs are caused by three hidden mechanisms: legacy budgeting habits that let obsolete costs compound invisibly year-on-year; over-engineered products absorbing costs for features buyers never valued; and bloated support activities consuming more than primary operations. The owner sees high costs but cannot locate exactly where they live."
            ),
            "elite_principle": (
                "The most dangerous costs in any SME are the ones that have always been there. They hide behind habit, not necessity. Zero-Based Budgeting forces every single rupee to prove its right to exist — not based on last year, but based on today's strategic reality. — ZBB doctrine, Pyhrr"
            ),
            "indian_sme_context": (
                "[MIXED — DOC + DERIVED, verify marked items] FROM DOC: (1) Force every department head to justify every single rupee from zero — Indian SME owners typically inherit vendor contracts and cost structures from their father's era; ZBB breaks this cycle DERIVED: (2) GST Input Tax Credit (ITC) audit — most Indian manufacturing SMEs have unclaimed ITC sitting on input materials. Run a full ITC reconciliation before cutting operational costs (3) MSME Samadhaan portal — if high costs are partly caused by delayed receivables forcing you to bridge with expensive short-term debt, file pending payment claims here first (4) Rajasthan textile/auto parts SMEs specifically: audit power costs separately — electricity tariff arbitrage between industrial and commercial rates is a common hidden cost leak"
            ),
            "priority": "HIGH — cost structure above break-even threshold destroys margin on every unit sold regardless of sales volume",
            "key_actions": [
                "Run Value Chain mapping first: walk every step of production and mark each activity as either Revenue-Generating or Cost-Only. Any Cost-Only activity with no customer value is a cut candidate.",
                "Pull last 12 months of vendor invoices. Mark every contract that auto-renewed without review. These are your first ZBB targets.",
                "Kill every SKU with negative contribution margin immediately. Calculate contribution margin per SKU before any other action.",
                "Run ERRC grid on your top 3 products: what features can be eliminated or reduced without the customer noticing? What one feature can be raised to justify a price premium?",
                "Stop all machines except the bottleneck from running at full capacity — excess production is a cost masquerading as productivity.",
                "Audit GST ITC claims. Unclaimed input credit is cash sitting in your cost structure that belongs to you."
            ],
            "decision_rule": (
                "Apply when: costs are rising faster than revenue, vendor contracts auto-renew without scrutiny, support costs exceed primary operation costs, or owner cannot name the top 3 cost drivers without checking reports. Trigger question — 'If this cost did not exist last year, would I create it today?'"
            )
        }

    # ─────────────────────────────────────────────────────────────
    # CRISIS TYPE 4: LOSING CUSTOMERS TO COMPETITORS
    # ─────────────────────────────────────────────────────────────
    elif crisis_type == "Losing customers to competitors":
        return {
            "framework": "Jobs To Be Done (Christensen) for defection diagnosis; 7 Powers (Hamilton Helmer) for structural barrier building; Value Map / EVC for repositioning; Porter's Generic Strategies for commitment to defensible position",
            "literature_basis": (
                "Clayton Christensen — JTBD theory; Hamilton Helmer — \"7 Powers\"; Michael Porter — Generic Strategies; Kim & Mauborgne — Blue Ocean Strategy; VRIO Framework — Barney (1991)"
            ),
            "description": (
                "Customer loss is misread as a pricing problem. It is almost always a structural failure — the product was fired for a rival that better resolves the customer's struggling moment, or the SME has no defensible barrier preventing competitors from arbitraging away its margins. The firm drifted into competitive parity without noticing."
            ),
            "elite_principle": (
                "Losing customers is not a sales problem. It is a structural architecture problem. Without a Power — a Switching Cost, a Process Barrier, a Counter-Position — your margins will be arbitraged away by any competitor willing to undercut you by 5%. Build the barrier first. Compete second. — Helmer, 7 Powers"
            ),
            "indian_sme_context": (
                "[MIXED — DOC + DERIVED, verify marked] FROM DOC: (1) Embed IT, auto parts, or manufacturing systems so deeply into the customer's operations that switching becomes operationally painful — this is your primary Switching Cost barrier in the Indian B2B context DERIVED: (2) Indian B2B SMEs losing customers to larger competitors: check if the rival is GeM-registered and winning government contracts you are invisible to — register on GeM immediately (3) Rajasthan auto parts / textile SMEs: Chinese import substitution is the most common structural threat. If this is the cause, cost leadership via TOC + ZBB is the only viable path — differentiation will not work against a 40% price gap (4) JTBD interviews in Indian B2B context should specifically probe payment terms — Indian SME customers frequently defect not for product quality but because a competitor offered net-60 vs your net-30. This is a financial job, not a product job"
            ),
            "priority": "HIGH — customer defection compounds; each lost account reduces referral network and signals market weakness to remaining clients",
            "key_actions": [
                "Interview your last 3 defected customers. One question only: what was the specific moment you decided to switch, and what were you trying to get done? Map the struggling moment exactly.",
                "Draw a Value Map: plot your price and top 5 perceived benefits directly against the competitor stealing your clients. Are you above or below the Value Equivalence Line?",
                "Run 7 Powers audit: do you have any structural barrier — switching cost, process complexity, counter-position — that makes replacing you genuinely painful? If the answer is no, build one before doing anything else.",
                "Force a binary Porter choice: cost leadership or differentiation. If you are trying to do both, you are stuck in the middle and will keep losing customers regardless of other actions.",
                "Audit your VRIO assets: which of your capabilities are actually rare and costly to imitate? Double down on those. Abandon everything else.",
                "Check payment terms against competitors. In Indian B2B, net terms are frequently the real switching trigger — not quality, not price."
            ],
            "decision_rule": (
                "Apply when: 2+ customers defect to the same competitor within one quarter, lost accounts cite vague reasons like 'better fit' or 'better service', or your win rate on new pitches drops below 30%. Trigger question — 'Did our customer leave because we failed at the job they hired us for, or because a competitor built a better trap?'"
            )
        }

    # ─────────────────────────────────────────────────────────────
    # CRISIS TYPE 5: DEMAND HAS FALLEN
    # ─────────────────────────────────────────────────────────────
    elif crisis_type == "Demand has fallen":
        return {
            "framework": "Disruptive Innovation (Christensen) for permanent demand diagnosis; Ansoff Matrix for pivot path selection; Product Life Cycle for catalog triage; Strategic Inflection Points (Grove) for 10X shift detection; TOC for inventory protection during collapse",
            "literature_basis": (
                "Clayton Christensen — \"The Innovator's Dilemma\" (Disruptive Innovation); Igor Ansoff — Ansoff Matrix; Andy Grove — \"Only The Paranoid Survive\"; Eliyahu Goldratt — TOC; Product Life Cycle — Theodore Levitt (1965)"
            ),
            "description": (
                "Demand collapse is the most misdiagnosed crisis. Owners treat a structural, permanent demand shift as a temporary cyclical dip and keep cutting prices into a market that will never return. The critical first question is not how to recover demand — it is whether the demand is recoverable at all."
            ),
            "elite_principle": (
                "The single most dangerous move during a demand collapse is optimizing harder for a market that no longer exists. Before any recovery action, answer one question: is this a cyclical dip or a structural extinction? The entire strategy changes based on that single diagnosis. — Grove, Strategic Inflection Points"
            ),
            "indian_sme_context": (
                "[MIXED — DOC + DERIVED, verify marked] FROM DOC: (1) Indian SME facing a 10X demand collapse must be willing to entirely abandon its legacy identity and re-tool machinery for a new viable market — Intel's pivot from memory chips to processors is the exact model DERIVED: (2) Ansoff Market Development for Indian SMEs: ONDC (Open Network for Digital Commerce) and DGFT export promotion schemes are the fastest routes to new geographic markets without heavy capital investment (3) Rajasthan textile / auto parts SMEs facing Chinese import disruption: this is a structural 10X shift, not a cycle. PLI (Production Linked Incentive) scheme eligibility should be checked immediately — it funds exactly the machinery re-tooling Ansoff's Product Development path requires (4) Product Life Cycle triage: map your SKUs and kill decline-stage products before GST filing season — liquidating dead inventory pre-filing cleans balance sheet and recovers ITC"
            ),
            "priority": "CRITICAL — permanent demand collapse with no pivot decision is a slow liquidation event; every month of inaction compounds cash burn on dead inventory",
            "key_actions": [
                "Answer the structural question first: interview 5 lost customers. Are they buying a cheaper substitute, or have they stopped buying this product category entirely? These require completely different responses.",
                "Map your entire product catalog on the Product Life Cycle curve. Any SKU in terminal decline gets discontinued this quarter — stop the cash bleed immediately.",
                "Apply Grove's silver bullet test: if your most feared low-cost competitor had one move to permanently take your market, have they already made it? If yes, you are past the inflection point.",
                "Run Ansoff on surviving products: can existing products go to new geographies or adjacent industries? Check ONDC and DGFT export schemes before spending on product development.",
                "Halt all raw material releases immediately. Do not produce a single unit without a firm customer due date attached. Demand collapse + excess inventory = bankruptcy.",
                "Check PLI scheme eligibility if re-tooling is the chosen path — government subsidy on new machinery changes the capital calculus for Ansoff's Product Development pivot completely."
            ],
            "decision_rule": (
                "Apply when: sales volume drops 30%+ with no recovery after 2 quarters of price cuts, entire customer segments stop ordering rather than switching to competitors, or a new technology/import is structurally undercutting your cost floor. Trigger question — 'Are my customers buying less of everything, or have they found a permanently better alternative to what I sell?'"
            )
        }

    # ─────────────────────────────────────────────────────────────
    # DEFAULT: GENERAL CRISIS
    # ─────────────────────────────────────────────────────────────
    elif crisis_type == "Owner is the bottleneck":

        return {
            "framework": "E-Myth (Gerber) as primary diagnostic;\n       High Output Management (Grove) for delegation\n       architecture; Level 5 Leadership (Collins) for\n       team-building exit from bottleneck",
            "literature_basis": (
                "Michael Gerber — \"The E-Myth Revisited\";\n       Andy Grove — \"High Output Management\";\n       Jim Collins — \"Good to Great\";\n       Peter Drucker — \"Management: Tasks,\n       Responsibilities, Practices\""
            ),
            "description": (
                "The founder is the binding constraint on company\n       growth. Owner operates as technician rather than\n       executive — building a people-dependent business\n       that cannot scale beyond their physical capacity.\n       Every approval the owner withholds is throughput\n       the entire company loses."
            ),
            "elite_principle": (
                "A manager's output is not their individual work —\n       it is the total output of their entire organization.\n       The founder's job is not to do the work.\n       It is to build the system that does the work.\n       — Grove, High Output Management"
            ),
            "indian_sme_context": (
                "[DERIVED — NOT IN DOC, VERIFY]\n       Indian SMEs have a specific variant: family\n       business culture means no non-family employee\n       is trusted with real authority, so delegation\n       structurally fails even when attempted.\n       Three India-specific actions:\n       (1) Create written position contracts with\n           explicit accountability — replaces the\n           informal verbal authority structure most\n           Indian SMEs run on\n       (2) Use CII / SIDBI mentorship programs to bring\n           in a non-family executive as a neutral\n           authority figure employees will accept\n       (3) Separate owner's salary from business\n           profit — most Indian SME owners conflate\n           the two, which hides the true cost of\n           the owner doing low-leverage work"
            ),
            "priority": "CRITICAL — owner bottleneck is a compounding\n       growth ceiling; gets worse every month without\n       intervention",
            "key_actions": [
                "List every task you did this week. Mark each as\n   Strategic or Operational. Delegate 100% of\n   Operational + Low Consequence tasks immediately",
                "Identify your barrels — watch who employees go\n   to organically for help. Promote that person to\n   own entire projects, not just tasks",
                "Build one written system this week that lets an\n   ordinary person do something you currently do\n   personally — this is your franchise prototype",
                "In every team meeting, replace statements with\n   questions. Stop providing answers. Force your\n   team to think without you",
                "Hire or elevate one person specifically to absorb\n   your single biggest decision monopoly"
            ],
            "decision_rule": (
                "Apply when: owner works 12+ hour days while\n       revenue is flat, employees queue at founder's\n       desk for approvals, new hires are constantly\n       second-guessed, business cannot operate for\n       one week without owner present.\n       Trigger question — 'If a ruthless outside CEO\n       replaced me tomorrow, would they look at my\n       daily task list and fire me for doing a\n       technician's job instead of an executive's?'"
            )
        }

    elif crisis_type == "Operational bottleneck":

        return {
            "framework": "Theory of Constraints (TOC) / Drum-Buffer-Rope (DBR),\n       supported by Lean/TPS for system redesign\n       and OEE for bottleneck measurement",
            "literature_basis": (
                "Eliyahu Goldratt — \"The Goal\" (TOC/DBR);\n       Taiichi Ohno — Toyota Production System;\n       OEE methodology (Seiichi Nakajima)"
            ),
            "description": (
                "Every factory has one binding constraint that sets\n       total throughput. Running non-bottleneck machines\n       at full capacity creates WIP pile-up and hides the\n       real problem. Capacity leaks silently through\n       unmeasured micro-stops and minor speed drops."
            ),
            "elite_principle": (
                "The throughput of the entire factory is determined\n       by the speed of its single slowest constraint.\n       Optimizing anything upstream or downstream of that\n       constraint is waste disguised as productivity.\n       — Goldratt, TOC"
            ),
            "indian_sme_context": (
                "[MY ADDITION — VERIFY]\n       Indian manufacturing SMEs face three hidden OEE\n       killers not in Western literature:\n       (1) Unscheduled power cuts (load shedding) —\n           treat as a scheduled machine stop with its\n           own reason code; use inverters/DG sets as\n           buffer only at the bottleneck\n       (2) Migrant labor seasonality — bottleneck shifts\n           when skilled operators leave for harvest months;\n           cross-train at least 2 operators per bottleneck\n           station\n       (3) ECLGS financing available for bottleneck\n           machinery upgrades — if constraint is an old\n           machine, this is a direct credit instrument"
            ),
            "priority": "HIGH — operational bottleneck directly caps\n       revenue regardless of demand or sales effort",
            "key_actions": [
                "Identify bottleneck: walk the floor and find where\n   WIP inventory physically piles up before a station",
                "Run bottleneck continuously: zero unplanned downtime\n   at this single machine is worth more than 100%\n   efficiency everywhere else",
                "Measure OEE only at the bottleneck: assign a specific\n   reason code to every stop, no matter how small",
                "Slow all upstream machines to match bottleneck pace —\n   stop producing inventory no one can process",
                "Switch downstream flow to pull/Kanban:\n   only build what the bottleneck has capacity to finish"
            ],
            "decision_rule": (
                "Apply when: production is delayed despite machines\n       running, WIP inventory builds between stations,\n       owner is adding shifts but output isn't increasing.\n       Trigger question — 'If I run this machine faster,\n       do I ship more goods or just build a bigger pile?'."
            )
        }

    else:
        return {
            "framework": "First Principles Business Audit + Collins Brutal Facts Protocol",
            "literature_basis": (
                "Aristotle / Elon Musk — First Principles Reasoning; "
                "Jim Collins, Good to Great (2001) — Confronting the Brutal Facts"
            ),
            "description": (
                "When the crisis does not map to a specific type, "
                "First Principles reasoning demands stripping the business down to its foundational elements: "
                "What value does this business actually create? For whom? At what cost? "
                "Collins' research in Good to Great identified that companies in crisis "
                "consistently avoid confronting the brutal facts of their situation — "
                "replacing honest diagnosis with optimism. "
                "The first step is an unfiltered, honest assessment of what is actually true about the business today — "
                "not what was true 6 months ago, not what the owner hopes is true."
            ),
            "elite_principle": (
                "Collins: 'Confront the brutal facts, yet never lose faith.' "
                "The most dangerous response to a business crisis is optimism without diagnosis. "
                "Identify the single biggest structural problem first. Everything else is secondary noise."
            ),
            "indian_sme_context": (
                "Indian SME owners often face personal and business finances that are entangled — "
                "the first audit must separate personal liability from business liability clearly. "
                "MSME Samadhaan portal allows you to formally file delayed payment claims against large corporate buyers — "
                "many SMEs are owed significant sums they have never formally pursued."
            ),
            "priority": "MEDIUM",
            "key_actions": [
                "Apply First Principles: write in one sentence what specific value your business creates and who pays for it — if you cannot write this sentence clearly, that IS the problem",
                "Collins Brutal Facts audit: list the 3 things that are genuinely true about your situation that you have been avoiding acknowledging",
                "Separate personal and business finances immediately if they are entangled — personal liability exposure in a business crisis can be catastrophic",
                "Check MSME Samadhaan portal for delayed payment claims you can formally file against large buyers",
                "Identify your single biggest cash drain and single biggest cash source — protect the source, reduce the drain",
                "Set one measurable 30-day goal that constitutes genuine evidence of recovery — not activity, but outcome"
            ],
            "decision_rule": (
                "Identify the single biggest structural problem. "
                "Fix that first. Everything else is distraction."
            )
        }