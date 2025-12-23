"""
Extractor Module

- Extracts text from PDF
- Extracts patient details
- Extracts diagnosis summary
- Detects hospital from report
"""

from pypdf import PdfReader
import re
import io


# =====================================================
# TEXT EXTRACTION (FIXED)
# =====================================================
def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    # ✅ FIX: Wrap bytes in BytesIO
    pdf_stream = io.BytesIO(pdf_bytes)

    reader = PdfReader(pdf_stream)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()


# =====================================================
# PATIENT DETAILS EXTRACTION
# =====================================================
def extract_patient_details(text: str) -> dict:
    details = {
        "name": "Unknown",
        "age": "Unknown",
        "gender": "Unknown"
    }

    name_match = re.search(r"Name\s*[:\-]\s*([A-Za-z ]+)", text, re.IGNORECASE)
    if name_match:
        details["name"] = name_match.group(1).strip()

    age_match = re.search(r"Age\s*[:\-]\s*(\d{1,3})", text, re.IGNORECASE)
    if age_match:
        details["age"] = age_match.group(1)

    gender_match = re.search(r"(Male|Female|Other)", text, re.IGNORECASE)
    if gender_match:
        details["gender"] = gender_match.group(1).capitalize()

    return details


# =====================================================
# DIAGNOSIS SUMMARY EXTRACTION
# =====================================================
def extract_diagnosis_summary(text: str) -> dict:
    diagnosis = "Diagnosis not specified"
    summary = ""

    diagnosis_match = re.search(
        r"(Diagnosis|Impression|Final Diagnosis)\s*[:\-]\s*(.+)",
        text,
        re.IGNORECASE
    )

    if diagnosis_match:
        diagnosis = diagnosis_match.group(2).strip()

    lines = text.split("\n")
    summary_lines = [line.strip() for line in lines if len(line.strip()) > 20][:4]

    summary = " ".join(summary_lines)

    return {
        "final_diagnosis": diagnosis,
        "clinical_summary": summary
    }


# =====================================================
# HOSPITAL DETECTION
# =====================================================
def detect_hospital(text: str) -> dict:
    text = text.lower()

    if "apollo" in text:
        return {
            "name": "Apollo Hospitals, Bannerghatta Road",
            "type": "Premium Private"
        }

    if "manipal" in text:
        return {
            "name": "Manipal Hospital, Old Airport Road",
            "type": "Mid-range Private"
        }

    if any(k in text for k in ["government", "medical college", "district hospital"]):
        return {
            "name": "Government Medical College Hospital",
            "type": "Government"
        }

    return {
        "name": "General Hospital (Bangalore)",
        "type": "Mid-range Private"
    }


# =====================================================
# MAIN PIPELINE
# =====================================================
def process_pdf(pdf_bytes: bytes) -> dict:
    text = extract_text_from_pdf(pdf_bytes)

    patient_details = extract_patient_details(text)
    summary_data = extract_diagnosis_summary(text)
    hospital_info = detect_hospital(text)

    return {
        "text": text,
        "details": patient_details,
        "summary_data": summary_data,
        "hospital": hospital_info
    }
