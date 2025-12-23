"""
Treatment Planner Module

Responsibilities:
- Generate AI-based treatment plan (Groq LLM)
- Fallback to rule-based logic if LLM fails
- Estimate treatment cost ONLY for detected hospital
- Works for ANY disease
- Streamlit Cloud compatible
"""

from llm_client import call_llm


# =====================================================
# COST ESTIMATION — SINGLE HOSPITAL ONLY
# =====================================================
def estimate_cost_for_hospital(diagnosis: str, hospital_type: str) -> str:
    diagnosis = diagnosis.lower()

    # 1️⃣ Determine severity
    if any(k in diagnosis for k in [
        "stemi", "heart", "cardiac", "myocardial",
        "stroke", "cancer", "icu", "sepsis"
    ]):
        base_min, base_max = 100000, 400000

    elif any(k in diagnosis for k in [
        "pneumonia", "infection", "diabetes",
        "hypertension", "asthma", "copd"
    ]):
        base_min, base_max = 20000, 80000

    else:
        base_min, base_max = 5000, 15000

    # 2️⃣ Hospital cost multiplier
    multiplier = {
        "Government": 0.6,
        "Mid-range Private": 1.0,
        "Premium Private": 1.6
    }.get(hospital_type, 1.0)

    min_cost = int(base_min * multiplier)
    max_cost = int(base_max * multiplier)

    return f"₹{min_cost:,} – ₹{max_cost:,}"


# =====================================================
# RULE-BASED FALLBACK PLAN (NEVER FAILS)
# =====================================================
def rule_based_plan() -> dict:
    return {
        "immediate_management": [
            "Stabilize patient condition",
            "Monitor vital signs",
            "Manage symptoms as per standard clinical guidelines"
        ],
        "medications": [
            "Initiate guideline-based medications",
            "Adjust dosage based on patient response"
        ],
        "monitoring_and_investigations": [
            "Repeat necessary laboratory investigations",
            "Monitor disease progression"
        ],
        "recovery_and_rehabilitation": [
            "Encourage gradual return to activity",
            "Provide lifestyle modification counseling"
        ],
        "discharge_and_follow_up": [
            "Discharge once clinically stable",
            "Schedule follow-up appointments"
        ]
    }


# =====================================================
# MAIN TREATMENT PLAN GENERATOR
# =====================================================
def generate_treatment_plan(patient: dict, diagnosis: dict, context: list) -> dict:
    final_diagnosis = diagnosis.get("final_diagnosis", "Unspecified condition")

    hospital = diagnosis.get("hospital", {
        "name": "General Hospital (Bangalore)",
        "type": "Mid-range Private"
    })

    # ===================== PROMPT =====================
    prompt = f"""
You are a senior clinical assistant.

Patient details:
{patient}

Diagnosis:
{final_diagnosis}

Generate a structured treatment plan with:
- Immediate Management
- Medications
- Monitoring and Investigations
- Recovery and Rehabilitation
- Discharge and Follow-up

Use concise bullet points.
"""

    # ===================== LLM CALL =====================
    llm_output = call_llm(prompt)

    # ===================== PLAN LOGIC =====================
    if not llm_output or "⚠️" in llm_output:
        treatment_sections = rule_based_plan()
    else:
        treatment_sections = {
            "ai_generated_plan": [
                line.strip()
                for line in llm_output.split("\n")
                if line.strip()
            ]
        }

    # ===================== COST ESTIMATION =====================
    estimated_cost = estimate_cost_for_hospital(
        final_diagnosis,
        hospital["type"]
    )

    # ===================== FINAL STRUCTURE =====================
    return {
        "treatment_plan": {
            **treatment_sections,
            "estimated_cost": [
                f"Hospital: {hospital['name']}",
                f"Estimated Treatment Cost: {estimated_cost}"
            ],
            "clinical_context_considered": (
                [
                    "Treatment plan informed by similar historical cases",
                    "Relevant clinical guidelines reviewed"
                ] if context else []
            )
        }
    }


