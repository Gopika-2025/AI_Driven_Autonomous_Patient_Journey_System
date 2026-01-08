"""
treatment_llm.py

ROLE
----
Generate clinically meaningful, structured treatment plans
based on the identified medical condition.

DESIGN PRINCIPLES
-----------------
- Rule-based first (safe & predictable)
- No dependency on LLM availability
- Works on Streamlit Cloud
- Easy to audit and explain
"""
def generate_treatment_plan_llm(
    patient: dict,
    problem: str,
    context_docs=None
) -> dict:
    """
    Generate treatment plan based on disease/problem.

    Args:
        patient (dict): Patient details
        problem (str): Identified diagnosis/disease
        context_docs (list): Retrieved medical context (optional)

    Returns:
        dict: Structured treatment plan
    """
    problem_lower = problem.lower()
    if "diabetes" in problem_lower:
        return {
            "Immediate Care": [
                "Assess fasting and postprandial blood glucose levels",
                "Evaluate hydration status and electrolyte balance",
                "Educate patient on symptoms of hyperglycemia and hypoglycemia"
            ],
            "Medications": [
                "Initiate oral hypoglycemic agents such as Metformin",
                "Consider insulin therapy if glycemic control is inadequate",
                "Adjust medication based on HbA1c values"
            ],
            "Lifestyle And Diet": [
                "Low glycemic index diet",
                "Avoid refined sugars and processed foods",
                "Regular physical activity (30 minutes/day)",
                "Weight management counseling"
            ],
            "Monitoring": [
                "Daily blood glucose monitoring",
                "HbA1c every 3 months",
                "Monitor for diabetic complications"
            ],
            "Follow Up": [
                "Initial follow-up within 1–2 weeks",
                "Routine review every 3 months"
            ]
        }
    if (
        "myocardial" in problem_lower
        or "stemi" in problem_lower
        or "heart" in problem_lower
    ):
        return {
            "Immediate Care": [
                "Urgent hospital admission",
                "Continuous cardiac monitoring",
                "Administer oxygen if hypoxic"
            ],
            "Medications": [
                "Antiplatelet therapy (Aspirin, Clopidogrel)",
                "High-intensity statins",
                "Beta-blockers and ACE inhibitors if indicated"
            ],
            "Lifestyle And Diet": [
                "Smoking cessation",
                "Low-fat, low-salt cardiac diet",
                "Enroll in cardiac rehabilitation"
            ],
            "Monitoring": [
                "Serial ECG monitoring",
                "Cardiac biomarkers (Troponin levels)",
                "Blood pressure and heart rate monitoring"
            ],
            "Follow Up": [
                "Cardiology follow-up within 7 days",
                "Long-term cardiovascular risk management"
            ]
        }
    if "hypertension" in problem_lower or "high blood pressure" in problem_lower:
        return {
            "Immediate Care": [
                "Confirm diagnosis with repeated blood pressure measurements",
                "Assess for end-organ damage"
            ],
            "Medications": [
                "Initiate antihypertensive therapy (ACE inhibitors or ARBs)",
                "Add calcium channel blockers or diuretics if required"
            ],
            "Lifestyle And Diet": [
                "Low-sodium DASH diet",
                "Weight reduction if overweight",
                "Regular aerobic exercise"
            ],
            "Monitoring": [
                "Home blood pressure monitoring",
                "Renal function and electrolyte monitoring"
            ],
            "Follow Up": [
                "Follow-up in 2–4 weeks",
                "Monthly monitoring until blood pressure is controlled"
            ]
        }
    return {
        "Immediate Care": [
            "Conduct comprehensive clinical evaluation",
            "Review all available diagnostic investigations"
        ],
        "Medications": [
            "Prescribe medications based on physician assessment"
        ],
        "Lifestyle And Diet": [
            "Balanced diet",
            "Adequate hydration",
            "Avoid tobacco and alcohol"
        ],
        "Monitoring": [
            "Monitor vital signs regularly",
            "Repeat investigations as clinically indicated"
        ],
        "Follow Up": [
            "Follow-up with general physician",
            "Refer to specialist if symptoms persist"
        ]
    }
