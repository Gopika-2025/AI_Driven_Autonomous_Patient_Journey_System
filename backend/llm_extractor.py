import json
from backend.llm_client import call_llm


def extract_clinical_info(report_text: str) -> dict:
    """
    Uses LLM to extract structured clinical information
    from raw diagnosis report text.

    Returns a SAFE dictionary (never breaks Streamlit UI).
    """

    prompt = f"""
You are a senior medical data extraction expert.

Your task:
Extract the following information ONLY from the report text.
If something is not explicitly present, return "Not mentioned".

Return STRICT JSON ONLY. No explanations.

Fields to extract:
- patient_name
- age
- gender
- chief_complaint
- key_findings
- risk_factors
- final_diagnosis

IMPORTANT RULES:
- Read carefully like a doctor
- Do NOT hallucinate
- If partially available, summarize briefly
- Output must be valid JSON

================= REPORT TEXT =================
{report_text}
================= END =================

JSON OUTPUT FORMAT:
{{
  "patient_name": "",
  "age": "",
  "gender": "",
  "chief_complaint": "",
  "key_findings": "",
  "risk_factors": "",
  "final_diagnosis": ""
}}
"""

    try:
        response = call_llm(prompt)

        # -------------------------------
        # Extract JSON safely
        # -------------------------------
        json_start = response.find("{")
        json_end = response.rfind("}") + 1

        if json_start == -1 or json_end == -1:
            raise ValueError("Invalid JSON from LLM")

        extracted = json.loads(response[json_start:json_end])

        # -------------------------------
        # Ensure all required keys exist
        # -------------------------------
        return normalize_output(extracted)

    except Exception as e:
        # Fallback — never break UI
        return {
            "patient_name": "Not mentioned",
            "age": "Not mentioned",
            "gender": "Not mentioned",
            "chief_complaint": "Not mentioned",
            "key_findings": "Not mentioned",
            "risk_factors": "Not mentioned",
            "final_diagnosis": "Not mentioned",
        }


def normalize_output(data: dict) -> dict:
    """
    Ensures missing or empty fields
    never break the Streamlit UI.
    """

    keys = [
        "patient_name",
        "age",
        "gender",
        "chief_complaint",
        "key_findings",
        "risk_factors",
        "final_diagnosis",
    ]

    normalized = {}

    for key in keys:
        value = data.get(key, "").strip()
        normalized[key] = value if value else "Not mentioned"

    return normalized
