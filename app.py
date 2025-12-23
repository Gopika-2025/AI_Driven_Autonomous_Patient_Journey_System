import streamlit as st
from datetime import date

from backend.extractor import process_pdf
from backend.rag import add_to_rag, query_rag
from backend.planner import generate_treatment_plan
from backend.pdf_builder import build_treatment_plan_pdf


# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="AI Treatment Planner",
    layout="wide"
)

# =====================================================
# HERO SECTION (PPT STYLE)
# =====================================================
st.markdown("## 🩺 AI Treatment Planner")
st.markdown("### Intelligent Care Pathway Assistant")

st.markdown(
    """
    **From Diagnosis to Action — Personalized, Clinically Guided Treatment Plans**

    Upload a diagnosis report to automatically extract clinical findings,
    generate an AI-assisted treatment plan, estimate hospital-specific costs,
    and produce a professional medical report.
    """
)

st.markdown("---")

# =====================================================
# STEP 1 — UPLOAD PDF
# =====================================================
st.markdown("## Step 1: Upload Diagnosis Report")

st.info(
    "Upload the diagnosis report (PDF). The system will extract patient details, "
    "diagnosis, and hospital information."
)

uploaded = st.file_uploader(
    "Upload Diagnosis Report (PDF)",
    type=["pdf"]
)

if not uploaded:
    st.warning("Please upload a diagnosis report to continue.")
    st.stop()

# =====================================================
# STEP 2 — EXTRACT DIAGNOSIS
# =====================================================
st.markdown("---")
st.markdown("## Step 2: Extract Clinical Information")

with st.spinner("Extracting diagnosis and hospital information..."):
    pdf_bytes = uploaded.read()
    extraction = process_pdf(pdf_bytes)

if not extraction.get("text"):
    st.error("Unable to extract text from the uploaded PDF.")
    st.stop()

patient = extraction["details"]
summary = extraction["summary_data"]
hospital = extraction["hospital"]

# =====================================================
# STEP 3 — DIAGNOSTIC REPORT SUMMARY (PPT STYLE)
# =====================================================
st.markdown("---")
st.markdown("## Step 3: Diagnostic Report Summary")

st.success(f"**Final Diagnosis:** {summary.get('final_diagnosis', 'Not identified')}")

with st.container():
    st.success("✅ Clinical Summary")
    st.write(summary.get("clinical_summary", ""))

    st.success("✅ Patient Details")
    st.write(
        f"""
        **Name:** {patient.get('name')}  
        **Age:** {patient.get('age')}  
        **Gender:** {patient.get('gender')}
        """
    )

    st.success("✅ Reported Hospital")
    st.write(f"🏥 **{hospital['name']}**, Bangalore")

# =====================================================
# STEP 4 — ADD TO RAG
# =====================================================
st.markdown("---")
st.markdown("## Step 4: Add Diagnosis to Knowledge Base")

st.info(
    "Store this diagnosis in the internal knowledge base to support "
    "context-aware treatment planning."
)

if st.button("➕ Add Diagnosis to Knowledge Base"):
    add_to_rag(extraction["text"])
    st.success("Diagnosis successfully added to knowledge base.")

# =====================================================
# STEP 5 — QUERY RAG
# =====================================================
st.markdown("---")
st.markdown("## Step 5: Retrieve Relevant Clinical Context")

context_docs = query_rag(summary.get("final_diagnosis", ""))

if context_docs:
    with st.expander("🔍 Retrieved Clinical Context"):
        for i, doc in enumerate(context_docs, start=1):
            st.markdown(f"**Context {i}:**")
            st.write(doc[:700] + "...")
else:
    st.info("No prior similar cases found. Proceeding without additional context.")

# =====================================================
# STEP 6 — GENERATE TREATMENT PLAN
# =====================================================
st.markdown("---")
st.markdown("## Step 6: Generate Treatment Plan")

if st.button("🧠 Generate Treatment Plan"):
    with st.spinner("Generating AI-assisted treatment plan..."):
        plan_data = generate_treatment_plan(
            patient=patient,
            diagnosis={
                "final_diagnosis": summary.get("final_diagnosis"),
                "hospital": hospital
            },
            context=context_docs
        )
        st.session_state["plan_data"] = plan_data

if "plan_data" not in st.session_state:
    st.stop()

treatment_plan = st.session_state["plan_data"]["treatment_plan"]

# =====================================================
# STEP 7 — DISPLAY TREATMENT PLAN (CLINICAL CARDS)
# =====================================================
st.markdown("---")
st.markdown("## Step 7: Treatment Plan")

for section, items in treatment_plan.items():
    st.markdown(f"### ✅ {section.replace('_', ' ').title()}")
    for item in items:
        st.markdown(f"- {item}")

# =====================================================
# STEP 8 — APPOINTMENT BOOKING (AUTO-HOSPITAL)
# =====================================================
st.markdown("---")
st.markdown("## Step 8: Appointment Booking")

st.info("The appointment will be scheduled at the same hospital as the diagnosis report.")

st.write(f"🏥 **Hospital:** {hospital['name']}")
st.write("📍 **City:** Bangalore")

with st.form("appointment_form"):
    department = st.selectbox(
        "Select Department",
        [
            "Cardiology",
            "Pulmonology",
            "General Medicine",
            "Neurology",
            "Orthopedics"
        ]
    )

    appt_date = st.date_input(
        "Select Appointment Date",
        min_value=date.today()
    )

    appt_time = st.time_input("Select Appointment Time")

    confirm_booking = st.form_submit_button("📌 Confirm Appointment")

if confirm_booking:
    st.session_state["appointment"] = {
        "hospital": hospital["name"],
        "department": department,
        "date": appt_date,
        "time": appt_time,
        "city": "Bangalore"
    }
    st.success("✅ Appointment Confirmed")

# Show appointment details
if "appointment" in st.session_state:
    appt = st.session_state["appointment"]
    st.markdown("### 🧾 Appointment Details")
    st.write(f"🏥 Hospital: **{appt['hospital']}**")
    st.write(f"🩺 Department: **{appt['department']}**")
    st.write(f"📅 Date: **{appt['date']}**")
    st.write(f"⏰ Time: **{appt['time']}**")
    st.write(f"📍 City: **{appt['city']}**")

# =====================================================
# STEP 9 — GENERATE & DOWNLOAD PDF
# =====================================================
st.markdown("---")
st.markdown("## Step 9: Generate Treatment Report")

if st.button("📄 Generate PDF Report"):
    pdf_buffer = build_treatment_plan_pdf(treatment_plan)
    st.session_state["pdf"] = pdf_buffer
    st.success("Treatment report generated successfully.")

if "pdf" in st.session_state:
    st.download_button(
        "⬇️ Download Treatment Report",
        st.session_state["pdf"],
        file_name="Patient_Treatment_Plan_Report.pdf",
        mime="application/pdf"
    )
