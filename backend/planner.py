import os
import requests
from typing import Dict
import streamlit as st


# -------------------------------------------------
# GROQ CONFIGURATION
# -------------------------------------------------
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"


# -------------------------------------------------
# SYSTEM PROMPT (DOCTOR ROLE)
# -------------------------------------------------
SYSTEM_PROMPT = """
You are a senior medical doctor acting as a clinical decision support system.

Rules:
- Base all recommendations strictly on the provided medical report
- Do NOT invent diagnoses
- If the information is insufficient, clearly state it
- Provide safe, evidence-based medical guidance
- Use structured, professional clinical language
- Do NOT include legal disclaimers in the output
"""


# -------------------------------------------------
# LOAD GROQ API KEY (LOCAL + CLOUD SAFE)
# -------------------------------------------------
def get_groq_key() -> str | None:
    # Streamlit Cloud
    if "GROQ_API_KEY" in st.secrets:
        return st.secrets["GROQ_API_KEY"]

    # Local machine (env / .env)
    return os.getenv("GROQ_API_KEY")


# -------------------------------------------------
# MAIN TREATMENT PLAN GENERATOR
# -------------------------------------------------
def generate_full_care_plan(patient: Dict, summary: Dict) -> Dict:
    api_key = get_groq_key()
    if not api_key:
        raise RuntimeError("❌ GROQ_API_KEY not found")

    # Fail-safe: no diagnosis
    if not summary.get("final_diagnosis"):
        return {
            "solution_type": "recommendation",
            "identified_problem": "Insufficient diagnostic information",
            "recommendation": [
                "The uploaded report does not contain a clear diagnosis",
                "Consult a qualified physician for further evaluation",
                "Additional clinical assessment or investigations may be required"
            ],
            "appointment": {
                "specialist": "General Physician",
                "recommended_timeline": "As soon as possible"
            }
        }

    user_prompt = f"""
Patient Details:
Age: {patient.get("age")}
Gender: {patient.get("gender")}

Chief Complaint:
{summary.get("chief_complaint")}

Identified Condition:
{summary.get("final_diagnosis")}

Report Type:
{summary.get("report_type")}

Generate a structured doctor-like response with the following sections:
1. Identified medical problem
2. Immediate care
3. Medications (general categories only, no brand names)
4. Monitoring and investigations
5. Lifestyle and patient advice
6. Follow-up and referral plan
7. Estimated treatment cost range in INR
"""

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(
        GROQ_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"GROQ API ERROR {response.status_code}: {response.text}"
        )

    ai_text = response.json()["choices"][0]["message"]["content"]

    return _format_for_ui(summary, ai_text)


# -------------------------------------------------
# FORMAT AI RESPONSE FOR EXISTING UI
# -------------------------------------------------
def _format_for_ui(summary: Dict, ai_text: str) -> Dict:
    lines = [
        line.strip("-• ")
        for line in ai_text.split("\n")
        if line.strip()
    ]

    return {
        "solution_type": "treatment",
        "identified_problem": summary.get(
            "final_diagnosis",
            "Medical condition identified"
        ),
        "treatment_plan": {
            "treatment_sections": {
                "Doctor Recommended Treatment Plan": lines
            }
        },
        "estimated_cost": {
            "consultation": "₹500 – ₹1,500",
            "investigations": "₹2,000 – ₹10,000",
            "medications": "₹1,000 – ₹5,000",
            "follow_up_cost": "₹500 – ₹2,000",
            "notes": "Estimated by AI clinician; varies by hospital and location"
        },
        "appointment": {
            "urgency": "Based on clinical severity",
            "specialist": "Relevant medical specialist",
            "recommended_timeline": "As soon as possible",
            "follow_up_frequency": "As advised by physician"
        }
    }
