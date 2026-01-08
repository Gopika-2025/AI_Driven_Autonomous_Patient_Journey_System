import streamlit as st

from backend.extractor import process_pdf
from backend.planner import generate_full_care_plan
from backend.rag import add_to_rag, query_rag
from backend.pdf_builder import build_treatment_plan_pdf


# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="AI Treatment Planner",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =====================================================
# GLOBAL STYLES (GREEN HEADERS + BLUE CARDS + GAP)
# =====================================================
st.markdown("""
<style>
.stApp {
    background-color: #7CE0C3;
}
.block-container {
    padding: 2rem 3rem;
}

/* Top header */
.header {
    background-color:#00245D;
    color:white;
    padding:30px;
    border-radius:6px;
    text-align:center;
    margin-bottom:30px;
}

/* Green section titles */
.section-title {
    background-color:#5C8F3A;
    color:white;
    padding:14px;
    font-size:24px;
    font-weight:700;
    border-radius:4px;
    margin-top:35px;
    margin-bottom:18px;   /* gap before blue card */
}

/* Blue info card */
.blue-card {
    background-color:#0071BC;
    color:white;
    padding:24px;
    border-radius:6px;
    font-size:18px;
    line-height:1.6;
}

/* Dark blue result card */
.blue-result {
    background-color:#00245D;
    color:white;
    padding:22px;
    border-radius:6px;
    font-size:18px;
    line-height:1.6;
    margin-bottom:30px;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# HEADER
# =====================================================
st.markdown("""
<div class="header">
    <h1>🩺 AI Treatment Planner — Intelligent Care Pathway Assistant</h1>
    <p>From Diagnosis to Action — Personalized, Clinically Guided Treatment Plans</p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# SECTION: UPLOAD REPORT (INFO + UPLOAD)
# =====================================================
st.markdown('<div class="section-title">Upload Diagnosis Report</div>', unsafe_allow_html=True)

st.markdown("""
<div class="blue-card">
Upload the patient’s diagnosis report. Once uploaded, the system automatically:
<ul>
<li>Extracts clinical information</li>
<li>Summarizes the diagnosis</li>
<li>Generates treatment, cost, and appointment plans</li>
</ul>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload PDF Diagnosis Report",
    type=["pdf"],
    label_visibility="collapsed"
)

if not uploaded_file:
    st.stop()


# =====================================================
# AUTOMATIC PIPELINE (NO BUTTONS)
# =====================================================
with st.spinner("Analyzing diagnosis report..."):
    extraction = process_pdf(uploaded_file.read())

patient = extraction["details"]
summary = extraction["summary_data"]

# Automatically add to RAG
add_to_rag(extraction["text"], summary.get("final_diagnosis", ""))

# Retrieve context and generate care plan
context_docs = query_rag(summary.get("final_diagnosis", ""))
plan = generate_full_care_plan(
    patient=patient,
    summary=summary,
    context_docs=context_docs
)

st.session_state["care_plan"] = plan


# =====================================================
# DIAGNOSTIC SUMMARY (INFO + RESULT)
# =====================================================
st.markdown('<div class="section-title">Diagnostic Report Summary</div>', unsafe_allow_html=True)

st.markdown("""
<div class="blue-card">
AI-generated summary of the uploaded diagnostic report to help clinicians
quickly understand the patient’s condition.
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="blue-result">
<b>Patient Name:</b> {patient.get("name")}<br>
<b>Age:</b> {patient.get("age")}<br>
<b>Gender:</b> {patient.get("gender")}<br><br>

<b>Chief Complaint:</b><br>
{summary.get("chief_complaint", "Not mentioned")}<br><br>

<b>Final Diagnosis:</b><br>
{summary.get("final_diagnosis", "Not mentioned")}
</div>
""", unsafe_allow_html=True)


# =====================================================
# HELPER FUNCTION FOR CLINICAL SECTIONS
# =====================================================
def clinical_section(title: str, content: str):
    st.markdown(f"""
    <div class="section-title">{title}</div>
    <div class="blue-result">{content}</div>
    """, unsafe_allow_html=True)


# =====================================================
# CLINICAL SECTIONS
# =====================================================
clinical_section(
    "1. Clinical Presentation",
    summary.get("chief_complaint", "Not available")
)

clinical_section(
    "2. Key Risk Factors",
    "Smoking, hypertension, hyperlipidemia, sedentary lifestyle, family history."
)

clinical_section(
    "3. ECG Findings",
    summary.get("ecg_findings", "ECG findings as per report.")
)


# =====================================================
# TREATMENT PLAN
# =====================================================
for section, steps in plan["treatment_plan"]["treatment_sections"].items():
    clinical_section(
        section.replace("_", " ").title(),
        "<br>".join(steps)
    )


# =====================================================
# ESTIMATED COST
# =====================================================
cost = plan["estimated_cost"]

clinical_section(
    "Estimated Cost",
    f"""
    Consultation: {cost.get("consultation")}<br><br>
    Investigations: {cost.get("investigations")}<br><br>
    Medications: {cost.get("medications")}<br><br>
    Follow-up Visits: {cost.get("follow_up_cost")}<br><br>
    Notes: {cost.get("notes")}
    """
)


# =====================================================
# APPOINTMENT RECOMMENDATION
# =====================================================
appt = plan["appointment"]

clinical_section(
    "Appointment Recommendation",
    f"""
    Urgency: {appt.get("urgency")}<br><br>
    Specialist: {appt.get("specialist")}<br><br>
    Timeline: {appt.get("recommended_timeline")}<br><br>
    Follow-up Frequency: {appt.get("follow_up_frequency")}
    """
)


# =====================================================
# PDF DOWNLOAD
# =====================================================
st.markdown('<div class="section-title">Download Treatment Report</div>', unsafe_allow_html=True)

if st.button("📄 Download Treatment Plan PDF"):
    pdf_file = build_treatment_plan_pdf(
        patient,
        summary,
        plan
    )

    with open(pdf_file, "rb") as f:
        st.download_button(
            "⬇️ Download PDF",
            f,
            file_name=pdf_file,
            mime="application/pdf"
        )
