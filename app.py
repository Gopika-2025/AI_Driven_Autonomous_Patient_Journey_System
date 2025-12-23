import streamlit as st
from datetime import date

from backend.extractor import process_pdf
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
# STEP 1 — UPLOAD DIAGNOSIS REPORT
# =====================================================
st.title("🩺 AI Treatment Planner")
st.subheader("Diagnosis → Treatment → Cost → Appointment")

uploaded = st.file_uploader(
    "Upload Diagnosis Report (PDF)",
    type=["pdf"]
)

if not uploaded:
    st.info("Please upload a diagnosis report to proceed.")
    st.stop()

# =====================================================
# STEP 2 — EXTRACT REPORT DATA
# =====================================================
with st.spinner("Extracting information from report..."):
    pdf_bytes = uploaded.read()
    extraction = process_pdf(pdf_bytes)

if not extraction.get("text"):
    st.error("Unable to read the diagnosis report.")
    st.stop()

patient = extraction["details"]
summary = extraction["summary_data"]
hospital = extraction["hospital"]

# =====================================================
# STEP 3 — DIAGNOSTIC SUMMARY
# =====================================================
st.markdown("---")
st.markdown("## Step 2: Diagnostic Report Summary")

st.success(summary.get("final_diagnosis", "Diagnosis not identified"))
st.write(summary.get("clinical_summary", ""))

st.markdown("### 🏥 Reported Hospital")
st.write(f"**{hospital['name']}**, Bangalore")

# =====================================================
# STEP 4 — GENERATE TREATMENT PLAN
# =====================================================
st.markdown("---")
st.markdown("## Step 3: Treatment Planning")

if st.button("🧠 Generate Treatment Plan"):
    with st.spinner("Generating treatment plan..."):
        plan_data = generate_treatment_plan(
            patient=patient,
            diagnosis={
                "final_diagnosis": summary.get("final_diagnosis"),
                "hospital": hospital
            },
            context=[]
        )
        st.session_state["plan_data"] = plan_data

if "plan_data" not in st.session_state:
    st.stop()

treatment_plan = st.session_state["plan_data"]["treatment_plan"]

# =====================================================
# STEP 5 — DISPLAY TREATMENT PLAN + COST
# =====================================================
st.markdown("---")
st.markdown("## Step 4: Treatment Plan & Cost")

for section, items in treatment_plan.items():
    st.markdown(f"### ✅ {section.replace('_', ' ').title()}")
    for item in items:
        st.markdown(f"- {item}")

# =====================================================
# STEP 6 — APPOINTMENT BOOKING (AUTO-HOSPITAL)
# =====================================================
st.markdown("---")
st.markdown("## Step 5: Appointment Booking")

st.write(f"🏥 **Hospital:** {hospital['name']}")
st.write("📍 **City:** Bangalore")

with st.form("appointment_form"):
    department = st.selectbox(
        "Department",
        ["Cardiology", "Pulmonology", "General Medicine", "Neurology"]
    )

    appt_date = st.date_input(
        "Appointment Date",
        min_value=date.today()
    )

    appt_time = st.time_input("Appointment Time")

    confirm = st.form_submit_button("📌 Confirm Appointment")

if confirm:
    st.session_state["appointment"] = {
        "hospital": hospital["name"],
        "department": department,
        "date": appt_date,
        "time": appt_time,
        "city": "Bangalore"
    }
    st.success("✅ Appointment Confirmed")

# =====================================================
# STEP 7 — SHOW APPOINTMENT DETAILS
# =====================================================
if "appointment" in st.session_state:
    appt = st.session_state["appointment"]

    st.markdown("### 🧾 Appointment Details")
    st.write(f"🏥 Hospital: **{appt['hospital']}**")
    st.write(f"🩺 Department: **{appt['department']}**")
    st.write(f"📅 Date: **{appt['date']}**")
    st.write(f"⏰ Time: **{appt['time']}**")
    st.write(f"📍 City: **{appt['city']}**")

# =====================================================
# STEP 8 — GENERATE PDF REPORT
# =====================================================
st.markdown("---")
st.markdown("## Step 6: Generate Treatment Report")

if st.button("📄 Generate PDF Report"):
    pdf_buffer = build_treatment_plan_pdf(treatment_plan)
    st.session_state["pdf"] = pdf_buffer
    st.success("Treatment report generated successfully.")

# =====================================================
# STEP 9 — DOWNLOAD PDF
# =====================================================
if "pdf" in st.session_state:
    st.download_button(
        "⬇️ Download Treatment Report",
        st.session_state["pdf"],
        file_name="Patient_Treatment_Plan_Report.pdf",
        mime="application/pdf"
    )
