import re
from typing import Dict, List


# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------
def normalize(text: str) -> str:
    return text.lower().replace("\n", " ")


# -------------------------------------------------
# PATIENT INFO (SECONDARY CHECK)
# -------------------------------------------------
def parse_patient_info(text: str) -> Dict:
    info = {
        "age": None,
        "gender": None
    }

    age_match = re.search(r"\b(\d{1,3})\s*(years|yrs|y)\b", text, re.I)
    if age_match:
        info["age"] = age_match.group(1)

    gender_match = re.search(r"\b(male|female|other)\b", text, re.I)
    if gender_match:
        info["gender"] = gender_match.group(1).capitalize()

    return info


# -------------------------------------------------
# LAB FINDINGS
# -------------------------------------------------
def extract_lab_findings(text: str) -> List[str]:
    findings = []

    patterns = {
        "Glucose": r"glucose\s*[:\-]?\s*(\d+)",
        "Hemoglobin": r"hemoglobin\s*[:\-]?\s*(\d+\.?\d*)",
        "Creatinine": r"creatinine\s*[:\-]?\s*(\d+\.?\d*)",
        "Cholesterol": r"cholesterol\s*[:\-]?\s*(\d+)"
    }

    for test, pattern in patterns.items():
        match = re.search(pattern, text, re.I)
        if match:
            findings.append(f"{test}: {match.group(1)}")

    return findings


# -------------------------------------------------
# RADIOLOGY FINDINGS
# -------------------------------------------------
def extract_radiology_findings(text: str) -> List[str]:
    findings = []

    impression_match = re.search(
        r"(impression|conclusion)[:\-]?\s*(.+)",
        text, re.I | re.S
    )

    if impression_match:
        line = impression_match.group(2).split("\n")[0].strip()
        findings.append(line)

    return findings


# -------------------------------------------------
# DIAGNOSIS EXTRACTION
# -------------------------------------------------
def extract_diagnosis(text: str) -> str:
    patterns = [
        r"final diagnosis[:\-]?\s*(.+)",
        r"diagnosis[:\-]?\s*(.+)",
        r"impression[:\-]?\s*(.+)"
    ]

    for p in patterns:
        match = re.search(p, text, re.I)
        if match:
            return match.group(1).split("\n")[0].strip()

    return "Diagnosis not clearly specified"


# -------------------------------------------------
# CHIEF COMPLAINT
# -------------------------------------------------
def extract_chief_complaint(text: str) -> str:
    match = re.search(
        r"(chief complaint|presenting complaint)[:\-]?\s*(.+)",
        text, re.I
    )
    if match:
        return match.group(2).strip()

    return "Not mentioned"


# -------------------------------------------------
# MAIN PARSER (USED BY app.py)
# -------------------------------------------------
def parse_medical_report(raw_text: str, report_type: str) -> Dict:
    text = normalize(raw_text)

    diagnosis = extract_diagnosis(raw_text)
    complaint = extract_chief_complaint(raw_text)

    lab_findings = []
    radiology_findings = []

    if report_type == "lab":
        lab_findings = extract_lab_findings(text)

    if report_type == "radiology":
        radiology_findings = extract_radiology_findings(raw_text)

    return {
        "chief_complaint": complaint,
        "final_diagnosis": diagnosis,
        "lab_findings": lab_findings,
        "radiology_findings": radiology_findings
    }
