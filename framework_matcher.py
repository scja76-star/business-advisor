def match_framework(crisis_type, monthly_revenue, monthly_costs, cash_on_hand):
    
    # Calculate key financial indicators
    profit = monthly_revenue - monthly_costs
    cash_runway = cash_on_hand / monthly_costs if monthly_costs > 0 else 0
    cost_ratio = monthly_costs / monthly_revenue if monthly_revenue > 0 else 1
    
    # Framework matching logic
    if crisis_type == "Cash flow problems":
        if cash_runway < 2:
            return {
                "framework": "Survival Mode Framework",
                "description": "Business has less than 2 months cash runway. Immediate cash conservation is critical.",
                "priority": "CRITICAL",
                "key_actions": [
                    "Identify and cut all non-essential costs immediately",
                    "Contact creditors to negotiate payment extensions",
                    "Focus only on highest margin products or services",
                    "Pursue any outstanding receivables aggressively"
                ]
            }
        else:
            return {
                "framework": "Working Capital Optimization",
                "description": "Cash flow is strained but business has some runway to implement changes.",
                "priority": "HIGH",
                "key_actions": [
                    "Analyze accounts receivable and payable cycles",
                    "Reduce inventory to minimum viable levels",
                    "Negotiate better payment terms with suppliers",
                    "Consider invoice financing options"
                ]
            }

    elif crisis_type == "Sales have dropped significantly":
        if cost_ratio > 0.8:
            return {
                "framework": "Contribution Margin Analysis",
                "description": "High cost ratio combined with falling sales creates compounding pressure. Must identify which products or services actually generate profit.",
                "priority": "HIGH",
                "key_actions": [
                    "Calculate contribution margin for each product or service",
                    "Eliminate or reduce lowest margin offerings",
                    "Concentrate resources on highest margin products",
                    "Review pricing strategy immediately"
                ]
            }
        else:
            return {
                "framework": "Revenue Recovery Framework",
                "description": "Costs are manageable but revenue must be rebuilt. Focus on demand generation and customer retention.",
                "priority": "MEDIUM",
                "key_actions": [
                    "Survey lost customers to understand why they left",
                    "Identify your top 20% customers and protect those relationships",
                    "Test targeted promotions to reactivate dormant customers",
                    "Review competitive positioning in the market"
                ]
            }

    elif crisis_type == "Costs are too high":
        return {
            "framework": "Zero Based Cost Review",
            "description": "Every cost must justify its existence from zero. No cost is assumed necessary simply because it existed before.",
            "priority": "HIGH",
            "key_actions": [
                "List every single monthly expense",
                "Categorize each as essential, important, or optional",
                "Eliminate all optional costs immediately",
                "Renegotiate all essential costs with suppliers"
            ]
        }

    elif crisis_type == "Losing customers to competitors":
        return {
            "framework": "Competitive Differentiation Analysis",
            "description": "Customer loss to competitors signals a positioning or value problem. Must identify and strengthen unique advantages.",
            "priority": "HIGH",
            "key_actions": [
                "Identify exactly which competitor is taking your customers",
                "Determine what that competitor offers that you do not",
                "Survey recent lost customers directly",
                "Define your single strongest differentiator and double down on it"
            ]
        }

    elif crisis_type == "Demand has fallen":
        return {
            "framework": "Ansoff Market Strategy Matrix",
            "description": "Falling demand requires evaluating whether to deepen current market presence or explore new markets and products.",
            "priority": "MEDIUM",
            "key_actions": [
                "Determine if demand has fallen for your business specifically or the whole market",
                "Evaluate adjacent customer segments you could serve",
                "Consider whether current products can be repositioned",
                "Assess whether new offerings could serve existing customers"
            ]
        }

    else:
        return {
            "framework": "General Business Health Review",
            "description": "Comprehensive review of all business fundamentals required.",
            "priority": "MEDIUM",
            "key_actions": [
                "Review all financial statements for the last 6 months",
                "Identify the single biggest drain on the business",
                "Speak directly with your top 5 customers",
                "Set one measurable goal for the next 30 days"
            ]
        }