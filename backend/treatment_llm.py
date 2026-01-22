"""
treatment_llm.py

ROLE
----
Generate clinically meaningful, disease-specific treatment plans.
This module DOES NOT rely on LLM hallucination.
All plans are rule-based and medically reasonable.
"""


def generate_treatment_plan_llm(
    patient: dict,
    problem: str,
    context_docs=None
) -> dict:
    """
    Generate structured treatment plan based on inferred disease.

    Args:
        patient (dict): Patient details
        problem (str): Inferred medical condition
        context_docs (optional): RAG context (not mandatory)

    Returns:
        dict: Treatment sections with actionable steps
    """

    problem_lower = problem.lower()

    # =====================================================
    # DIABETES MELLITUS
    # =====================================================
    if "diabetes" in problem_lower or "hyperglycemia" in problem_lower:
        return {
            "Immediate Care": [
                "Assess fasting and post-prandial blood glucose levels",
                "Evaluate hydration status and electrolyte balance",
                "Educate patient on symptoms of hypoglycemia and hyperglycemia"
            ],
            "Medications": [
                "Initiate Metformin as first-line therapy if not contraindicated",
                "Add additional oral agents or insulin based on HbA1c levels",
                "Review medication adherence and side effects"
            ],
            "Lifestyle And Diet": [
                "Low glycemic index diet",
                "Avoid refined sugars and sweetened beverages",
                "Regular physical activity (minimum 30 minutes daily)",
                "Weight reduction if overweight"
            ],
            "Monitoring": [
                "Self-monitoring of blood glucose",
                "HbA1c testing every 3 months",
                "Screen for diabetic complications (neuropathy, nephropathy, retinopathy)"
            ],
            "Follow Up": [
                "Initial follow-up in 1–2 weeks",
                "Routine follow-up every 3 months"
            ]
        }

    # =====================================================
    # ACUTE MYOCARDIAL INFARCTION / STEMI
    # =====================================================
    if (
        "myocardial infarction" in problem_lower
        or "stemi" in problem_lower
        or "acute coronary" in problem_lower
    ):
        return {
            "Immediate Care": [
                "Urgent hospital admission",
                "Continuous cardiac monitoring",
                "Administer oxygen if hypoxic"
            ],
            "Medications": [
                "Dual antiplatelet therapy (Aspirin + Clopidogrel)",
                "High-intensity statins",
                "Beta-blockers and ACE inhibitors as tolerated",
                "Anticoagulation as per protocol"
            ],
            "Lifestyle And Diet": [
                "Strict smoking cessation",
                "Low-fat and low-salt cardiac diet",
                "Cardiac rehabilitation program"
            ],
            "Monitoring": [
                "Serial ECG monitoring",
                "Cardiac biomarkers (Troponin)",
                "Blood pressure and heart rate monitoring"
            ],
            "Follow Up": [
                "Cardiology follow-up within 7 days",
                "Long-term cardiovascular risk management"
            ]
        }

    # =====================================================
    # HYPERTENSION
    # =====================================================
    if "hypertension" in problem_lower or "high blood pressure" in problem_lower:
        return {
            "Immediate Care": [
                "Confirm diagnosis with repeated blood pressure readings",
                "Assess for end-organ damage"
            ],
            "Medications": [
                "Initiate ACE inhibitors or ARBs",
                "Add calcium channel blockers or diuretics if needed"
            ],
            "Lifestyle And Diet": [
                "Low-sodium DASH diet",
                "Weight reduction",
                "Regular aerobic exercise"
            ],
            "Monitoring": [
                "Home blood pressure monitoring",
                "Periodic renal function and electrolyte testing"
            ],
            "Follow Up": [
                "Follow-up in 2–4 weeks",
                "Monthly review until blood pressure is controlled"
            ]
        }

    # =====================================================
    # NORMAL ECG / NO ACUTE DISEASE
    # =====================================================
    if "normal ecg" in problem_lower:
        return {
            "Immediate Care": [
                "Reassure patient",
                "No emergency intervention required"
            ],
            "Medications": [
                "No cardiac medications required unless otherwise indicated"
            ],
            "Lifestyle And Diet": [
                "Maintain a healthy lifestyle",
                "Regular physical activity",
                "Balanced diet"
            ],
            "Monitoring": [
                "Routine health monitoring",
                "Repeat ECG only if symptoms develop"
            ],
            "Follow Up": [
                "Routine outpatient follow-up"
            ]
        }

    # =====================================================
    # FALLBACK — GENERAL MEDICAL CONDITION
    # =====================================================
    return {
        "Immediate Care": [
            "Conduct comprehensive clinical evaluation",
            "Review all available diagnostic reports"
        ],
        "Medications": [
            "Medications as advised by the treating physician"
        ],
        "Lifestyle And Diet": [
            "Balanced diet",
            "Adequate hydration",
            "Avoid smoking and alcohol"
        ],
        "Monitoring": [
            "Monitor vital signs",
            "Repeat investigations as clinically indicated"
        ],
        "Follow Up": [
            "Follow-up with general physician",
            "Specialist referral if symptoms persist"
        ]
    }
