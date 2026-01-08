"""
planner.py

ROLE
----
Central orchestration layer of the AI Treatment Planner.

RESPONSIBILITIES
----------------
1. Identify the disease / medical problem
2. Generate treatment plan
3. Estimate treatment cost
4. Recommend appointment & follow-up

This file DOES NOT handle UI or extraction.
"""

from backend.treatment_llm import generate_treatment_plan_llm
from backend.cost_estimator import estimate_cost
from backend.appointment_planner import recommend_appointment


# =====================================================
# DISEASE / PROBLEM IDENTIFICATION
# =====================================================
def infer_medical_problem(summary: dict) -> str:
    """
    Infer disease from extracted clinical summary.
    """

    diagnosis = summary.get("final_diagnosis", "").strip()
    text = summary.get("clinical_summary", "").lower()

    # Prefer explicit diagnosis
    if diagnosis and diagnosis.lower() != "not mentioned":
        return diagnosis

    # Heuristic inference if diagnosis missing
    if "glucose" in text or "diabetes" in text:
        return "Diabetes Mellitus"

    if "st elevation" in text or "stemi" in text or "myocardial" in text:
        return "Acute Myocardial Infarction"

    if "blood pressure" in text or "hypertension" in text:
        return "Hypertension"

    if "infection" in text or "fever" in text:
        return "Suspected Infection"

    return "General Medical Condition"


# =====================================================
# FULL CARE PLAN GENERATOR
# =====================================================
def generate_full_care_plan(
    patient: dict,
    summary: dict,
    context_docs: list
) -> dict:
    """
    Generate the complete care plan pipeline.
    """

    # 1️⃣ Identify medical problem
    problem = infer_medical_problem(summary)

    # 2️⃣ Generate treatment plan (LLM + rules)
    treatment_plan = generate_treatment_plan_llm(
        patient=patient,
        problem=problem,
        context_docs=context_docs
    )

    # 3️⃣ Estimate cost
    estimated_cost = estimate_cost(problem)

    # 4️⃣ Recommend appointment
    appointment = recommend_appointment(problem)

    return {
        "identified_problem": problem,
        "treatment_plan": treatment_plan,
        "estimated_cost": estimated_cost,
        "appointment": appointment
    }
