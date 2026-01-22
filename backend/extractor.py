import re
from io import BytesIO
from typing import Dict

from pypdf import PdfReader
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image

# Tesseract path (Streamlit Cloud / Docker safe)
pytesseract.pytesseract.tesseract_cmd = "./bin/tesseract"
def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    text = ""

    # Try digital PDF extraction
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception:
        pass

    # If very little text → OCR
    if len(text.strip()) < 200:
        images = convert_from_bytes(
            pdf_bytes,
            dpi=300,
            poppler_path="./bin/poppler"
        )
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"

    return text.strip()
def detect_report_type(text: str) -> str:
    t = text.lower()

    radiology_keywords = [
        "ct scan", "x-ray", "mri",
        "ultrasound", "radiology", "imaging"
    ]

    for k in radiology_keywords:
        if k in t:
            return "radiology"

    return "diagnosis"
def extract_patient_name(text: str) -> str:
    t = text.replace("\n", " ")

    match = re.search(
        r"(Patient Name|Patient|Name)\s*[:\-]?\s*([A-Z][a-z]+(?:\s[A-Z][a-z]+){1,2})",
        t
    )

    if match:
        name = match.group(2).strip()

        # Remove trailing junk words
        junk = ["patient", "age", "sex", "gender"]
        if not any(j in name.lower() for j in junk):
            return name

    return "Not mentioned"
def extract_age(text: str) -> str:
    match = re.search(r"(Age)\s*[:\-]?\s*(\d{1,3})", text, re.I)
    return match.group(2) if match else "Not mentioned"
def extract_gender(text: str) -> str:
    match = re.search(
        r"(Gender|Sex)\s*[:\-]?\s*(Male|Female|M|F)",
        text,
        re.I
    )

    if match:
        g = match.group(2).upper()
        return "Male" if g in ["M", "MALE"] else "Female"

    return "Not mentioned"
def extract_diagnosis(text: str) -> str:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    diagnosis = "Diagnosis not clearly specified"

    for i, line in enumerate(lines):
        if any(k in line.lower() for k in [
            "final diagnosis", "impression",
            "diagnosis", "conclusion"
        ]):
            if i + 1 < len(lines):
                candidate = lines[i + 1]

                stop_words = [
                    "section", "lab", "patient",
                    "page", "date", "signed",
                    "imaging", "investigation"
                ]

                if (
                    len(candidate) < 100 and
                    not any(sw in candidate.lower() for sw in stop_words)
                ):
                    diagnosis = candidate
                    break

    # Normalize normal findings
    if diagnosis.lower().startswith("normal"):
        diagnosis = "No abnormal findings detected"

    return diagnosis
def extract_chief_complaint(text: str) -> str:
    match = re.search(
        r"(Chief Complaint|Presenting Complaint|Reason for Admission)[:\-]?\s*(.+)",
        text,
        re.I
    )

    return match.group(2).strip() if match else "Not mentioned"
def process_diagnosis_report(pdf_bytes: bytes) -> Dict:
    text = extract_text_from_pdf(pdf_bytes)
    report_type = detect_report_type(text)

    patient_details = {
        "name": extract_patient_name(text),
        "age": extract_age(text),
        "gender": extract_gender(text)
    }

    diagnosis = extract_diagnosis(text)
    chief_complaint = extract_chief_complaint(text)

    # Radiology fallback
    if report_type == "radiology" and diagnosis == "Diagnosis not clearly specified":
        diagnosis = "No acute cardiopulmonary process identified"

    return {
        "details": patient_details,
        "summary_data": {
            "final_diagnosis": diagnosis,
            "chief_complaint": chief_complaint,
            "report_type": report_type
        },
        "raw_text": text
    }
