import streamlit as st

from backend.extractor import process_diagnosis_report   # 🔧 CHANGED
from backend.planner import generate_full_care_plan
from backend.pdf_builder import build_treatment_plan_pdf

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Treatment Planner",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------
# STYLES
# -------------------------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #7BE6C7;
}
.block-container {
    padding: 0;
}
.top-header {
    background-color: #041F5F;
    padding: 50px 40px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
}
.top-header h1 {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 10px;
    color: #FFFFFF !important;
}
.top-header p {
    font-size: 22px;
    margin: 6px 0;
    color: #FFFFFF;
}
.green-box {
    background-color: #7CB342;
    padding: 30px 40px;
    color: white;
    font-size: 20px;
    line-height: 1.6;
    text-align: center;
    margin-bottom: 30px;
}
.section-header {
    background-color: #5B8A3C;
    color: white;
    padding: 14px 20px;
    font-size: 24px;
    font-weight: 700;
    margin-top: 30px;
}
.info-panel {
    background-color: #4A74C3;
    color: white;
    padding: 28px 30px;
    font-size: 18px;
    line-height: 1.7;
    margin-top: 12px;
}
.result-panel {
    background-color: #00245D;
    color: white;
    padding: 22px;
    border-radius: 6px;
    font-size: 18px;
    line-height: 1.6;
    margin-top: 15px;
}
.validation-text {
    font-size: 16px;
    color: #000000;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("""
<div class="top-header">
    <h1>AI Treatment Planner — Intelligent Care Pathway Assistant</h1>
    <p>From Diagnosis to Action — Personalized, Clinically Guided Treatment Plans.</p>
    <br>
    <p>
        Transform care delivery with AI-generated recommendations,
        lifestyle guidance, medications, and follow-up planning.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# INTRO
# -------------------------------------------------
st.markdown("""
<div class="green-box">
    Upload a diagnosis or radiology report to automatically extract clinical insights
    and generate an AI-powered treatment plan with downloadable documentation.
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# FILE UPLOAD
# -------------------------------------------------
st.markdown('<div class="section-header">Upload Diagnosis Report</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-panel">
    Upload a diagnosis or radiology report (PDF or image).
    The system will extract patient details, detect the report type,
    summarize findings, and generate a treatment plan.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Upload PDF / JPG / PNG",
        type=["pdf", "jpg", "jpeg", "png"]
    )

with col2:
    st.markdown("""
    <div class="validation-text">
    <b>Validation:</b><br>
    1. No File Selected – Please upload a report<br>
    2. Unsupported File Type<br>
    3. Corrupted or Empty File<br>
    4. Unreadable Medical Content
    </div>
    """, unsafe_allow_html=True)

if not uploaded_file:
    st.stop()

# -------------------------------------------------
# EXTRACTION
# -------------------------------------------------
with st.spinner("Analyzing medical report..."):
    file_bytes = uploaded_file.read()
    extraction = process_diagnosis_report(file_bytes)   # 🔧 CHANGED

# 🔧 ADDED SAFETY
if not extraction.get("details") or not extraction.get("summary_data"):
    st.error("Failed to extract clinical information from the report.")
    st.stop()

patient = extraction["details"]
summary = extraction["summary_data"]

# -------------------------------------------------
# TREATMENT PLAN
# -------------------------------------------------
plan = generate_full_care_plan(patient, summary)

patient_name = patient.get("name", "Not mentioned")
patient_age = patient.get("age", "Not mentioned")
patient_gender = patient.get("gender", "Not mentioned")

identified_disease = plan.get(
    "identified_problem",
    summary.get("final_diagnosis", "Not identified")
)

# -------------------------------------------------
# PATIENT INFO
# -------------------------------------------------
st.markdown('<div class="section-header">Extracted Patient Information</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="result-panel">
<b>Patient Name:</b> {patient_name}<br>
<b>Age:</b> {patient_age}<br>
<b>Gender:</b> {patient_gender}<br><br>
<b>Identified Disease / Condition:</b><br>
{identified_disease}
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SUMMARY
# -------------------------------------------------
st.markdown(
    f'<div class="section-header">Diagnostic Report Summary — {identified_disease}</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-panel">
    AI-generated summary based on extracted clinical findings.
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="result-panel">
<b>Chief Complaint:</b><br>
{summary.get("chief_complaint", "Not mentioned")}
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TREATMENT SECTIONS
# -------------------------------------------------
treatment_sections = plan.get("treatment_plan", {}).get("treatment_sections", {})  # 🔧 ADDED SAFETY

if not treatment_sections:
    st.error("Treatment plan generation failed.")
    st.stop()

for section, steps in treatment_sections.items():
    st.markdown(f'<div class="section-header">{section}</div>', unsafe_allow_html=True)
    st.markdown(
        "<div class='result-panel'><ul>" +
        "".join(f"<li>{s}</li>" for s in steps) +
        "</ul></div>",
        unsafe_allow_html=True
    )

# -------------------------------------------------
# COST
# -------------------------------------------------
cost = plan.get("estimated_cost", {})

st.markdown('<div class="section-header">Estimated Cost</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="result-panel">
Consultation: {cost.get("consultation", "N/A")}<br>
Investigations: {cost.get("investigations", "N/A")}<br>
Medications: {cost.get("medications", "N/A")}<br>
Follow-up: {cost.get("follow_up_cost", "N/A")}
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# APPOINTMENT
# -------------------------------------------------
appt = plan.get("appointment", {})

st.markdown('<div class="section-header">Appointment Recommendation</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="result-panel">
Urgency: {appt.get("urgency", "N/A")}<br>
Specialist: {appt.get("specialist", "N/A")}<br>
Timeline: {appt.get("recommended_timeline", "N/A")}<br>
Follow-up Frequency: {appt.get("follow_up_frequency", "N/A")}
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# DOWNLOAD PDF
# -------------------------------------------------
st.markdown('<div class="section-header">Download Treatment Report</div>', unsafe_allow_html=True)

if st.button("📄 Download Treatment Plan PDF"):
    pdf_file = build_treatment_plan_pdf(patient, summary, plan)
    with open(pdf_file, "rb") as f:
        st.download_button(
            "⬇️ Download PDF",
            f,
            file_name=pdf_file,
            mime="application/pdf"
        )
