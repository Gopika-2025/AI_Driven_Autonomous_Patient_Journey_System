"""
appointment_planner.py

ROLE
----
Recommend appropriate specialist consultation and follow-up timeline
based on the identified disease or medical problem.

DESIGN PRINCIPLES
-----------------
- Rule-based (no AI hallucination)
- Clinically conservative
- Easy to understand and explain
"""

from typing import Dict


def recommend_appointment(problem: str) -> Dict[str, str]:
    """
    Recommend specialist and appointment timeline.

    Args:
        problem (str): Identified disease / medical condition

    Returns:
        dict: Appointment recommendation
    """

    p = problem.lower()

    # =====================================================
    # HEART ATTACK / MYOCARDIAL INFARCTION (EMERGENCY)
    # =====================================================
    if "stemi" in p or "myocardial" in p or "heart attack" in p:
        return {
            "urgency": "Emergency",
            "specialist": "Cardiologist",
            "recommended_timeline": "Immediate (Emergency admission)",
            "follow_up_frequency": "As per cardiology protocol"
        }

    # =====================================================
    # DIABETES / HYPERGLYCEMIA
    # =====================================================
    if "diabetes" in p or "hyperglycemia" in p:
        return {
            "urgency": "High",
            "specialist": "Endocrinologist / General Physician",
            "recommended_timeline": "Within 7 days",
            "follow_up_frequency": "Every 3 months (or as advised)"
        }

    # =====================================================
    # HYPERTENSION
    # =====================================================
    if "hypertension" in p or "blood pressure" in p:
        return {
            "urgency": "Moderate",
            "specialist": "General Physician / Cardiologist",
            "recommended_timeline": "Within 5–7 days",
            "follow_up_frequency": "Every 1–3 months"
        }

    # =====================================================
    # GENERAL / UNDIFFERENTIATED CONDITION
    # =====================================================
    return {
        "urgency": "Routine",
        "specialist": "General Physician",
        "recommended_timeline": "Within 3–5 days",
        "follow_up_frequency": "As advised after evaluation"
    }
