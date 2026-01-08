"""
cost_estimator.py

ROLE
----
Provide a realistic, rule-based cost estimate for treatment planning.

WHY RULE-BASED?
---------------
- Predictable output
- No AI hallucinations
- Easy to justify in review / viva
- Works offline and on Streamlit Cloud
"""

from typing import Dict


def estimate_cost(problem: str) -> Dict[str, str]:
    """
    Estimate treatment cost based on identified disease.

    Args:
        problem (str): Identified medical condition

    Returns:
        Dict[str, str]: Human-readable cost breakdown
    """

    p = (problem or "").lower()

    # =====================================================
    # DIABETES / HYPERGLYCEMIA
    # =====================================================
    if any(k in p for k in ["diabetes", "hyperglycemia"]):
        return {
            "consultation": "₹800 – ₹1,500",
            "investigations": "₹1,500 – ₹3,000",
            "medications": "₹500 – ₹1,200 per month",
            "follow_up_cost": "₹500 – ₹1,000 per visit",
            "notes": "Costs depend on oral therapy versus insulin requirement."
        }

    # =====================================================
    # HYPERTENSION
    # =====================================================
    if any(k in p for k in ["hypertension", "high blood pressure"]):
        return {
            "consultation": "₹700 – ₹1,200",
            "investigations": "₹1,000 – ₹2,000",
            "medications": "₹400 – ₹1,000 per month",
            "follow_up_cost": "₹500 – ₹1,000 per visit",
            "notes": "Lifestyle modification can reduce long-term costs."
        }

    # =====================================================
    # HEART ATTACK / MYOCARDIAL INFARCTION
    # =====================================================
    if any(k in p for k in ["stemi", "myocardial", "heart attack", "acute coronary"]):
        return {
            "emergency_care": "₹20,000 – ₹60,000",
            "procedures": "₹1,50,000 – ₹3,00,000 (angioplasty if required)",
            "icu_charges": "₹10,000 – ₹25,000 per day",
            "medications": "₹2,000 – ₹4,000 per month",
            "follow_up_cost": "₹1,000 – ₹2,000 per visit",
            "notes": "Final cost varies by hospital and intervention type."
        }

    # =====================================================
    # GENERAL / UNDIFFERENTIATED CONDITION
    # =====================================================
    return {
        "consultation": "₹500 – ₹1,000",
        "investigations": "₹1,000 – ₹2,500",
        "medications": "Depends on confirmed diagnosis",
        "follow_up_cost": "₹500 – ₹1,000 per visit",
        "notes": "Accurate cost will be determined after clinical evaluation."
    }
