"""
extractor.py

ROLE
----
Cloud-safe extraction module for diagnostic reports.

FEATURES
--------
- Extracts text from digitally generated PDFs
- Detects scanned PDFs (no OCR on cloud)
- Extracts:
  • Patient name
  • Age
  • Gender
  • Chief complaint
  • Final diagnosis
  • ECG findings
- Raises clean warning for scanned PDFs
"""

import re
import io
from pypdf import PdfReader


# =====================================================
# TEXT EXTRACTION (DIGITAL PDFs ONLY)
# =====================================================
def extract_text(pdf_bytes: bytes) -> str:
    """
    Extract text from a digitally generated PDF.
    OCR is intentionally NOT used (Streamlit Cloud safe).
    """
    text = ""

    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception:
        pass

    return text.strip()


# =====================================================
# PATIENT DETAILS EXTRACTION
# =====================================================
def extract_patient_details(text: str) -> dict:
    def find(pattern):
        m = re.search(pattern, text, re.I | re.S)
        return m.group(1).strip() if m else "Not mentioned"

    return {
        "name": find(r"(?:Patient Name|Patient)\s*[:\-]?\s*([A-Za-z ]+)"),
        "age": find(r"Age\s*[:\-]?\s*(\d+)"),
        "gender": find(r"(?:Gender|Sex)\s*[:\-]?\s*(Male|Female)")
    }


# =====================================================
# CLINICAL SECTIONS EXTRACTION
# =====================================================
def extract_chief_complaint(text: str) -> str:
    m = re.search(
        r"(Chief Complaint|Presenting Complaint)\s*[:\-]?\s*(.*?)(\n\n|$)",
        text,
        re.I | re.S
    )
    return m.group(2).strip() if m else "Not mentioned"


def extract_final_diagnosis(text: str) -> str:
    patterns = [
        r"(FINAL DIAGNOSIS|IMPRESSION|DIAGNOSIS)\s*[:\-]?\s*(.*?)(\n\n|$)",
        r"Conclusion\s*[:\-]?\s*(.*)"
    ]

    for p in patterns:
        m = re.search(p, text, re.I | re.S)
        if m:
            return m.group(2).strip()

    return "Not mentioned"


def extract_ecg_findings(text: str) -> str:
    m = re.search(
        r"(ECG|ECG Findings|ECG Interpretation)\s*[:\-]?\s*(.*?)(\n\n|$)",
        text,
        re.I | re.S
    )
    return m.group(2).strip() if m else "Not mentioned"


# =====================================================
# MAIN PIPELINE FUNCTION
# =====================================================
def process_pdf(pdf_bytes: bytes) -> dict:
    """
    Main entry point for PDF processing.

    Raises:
        ValueError if PDF appears to be scanned.
    """

    text = extract_text(pdf_bytes)

    # 🚨 HYBRID DETECTION LOGIC
    if len(text.strip()) < 100:
        raise ValueError(
            "⚠️ This appears to be a scanned PDF. "
            "Please upload a text-based (digitally generated) diagnostic report."
        )

    patient_details = extract_patient_details(text)

    summary_data = {
        "chief_complaint": extract_chief_complaint(text),
        "final_diagnosis": extract_final_diagnosis(text),
        "ecg_findings": extract_ecg_findings(text),
        "clinical_summary": text[:2000]
    }

    return {
        "text": text,
        "details": patient_details,
        "summary_data": summary_data
    }
