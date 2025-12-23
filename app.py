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

st.title("🩺 AI Treatment Planner")
st.caption("Upload → Diagnose → Plan → Report")

# =====================================================
# STEP 1 — UPLOAD PDF
# =====================================================
st.markdown("## Step 1: Upload Diagnosis Report")

uploaded = st.file_uploader(
    "Upload Diagnosis Report (PDF)",
    type=["pdf"]
)

if not uploaded:
    st.stop()

# =====================================================
# STEP 2 — EXTRACT DIAGNOSIS
# =====================================================
st.markdown("## Step 2: Extract Diagnosis")

with st.spinner("Extracting diagnosis from report..."):
    pdf_bytes = uploaded.read()
    extraction = process_pdf(pdf_bytes)

if not extraction.get("text"):
    st.error("Unable to extract text from report.")
    st.stop()

patient = extraction["details"]
summary = extraction["summary_data"]
hospital = extraction["hospital"]

# =====================================================
# STEP 3 — SHOW SUMMARY
# =====================================================
st.markdown("## Step 3: Diagnostic Summary")

st.success(summary.get("final_diagnosis", "Diagnosis not found"))
st.write(summary.get("clinical_summary", ""))

st.markdown("**Reported Hospital:**")
st.write(f"🏥 {hospital['name']}, Bangalore")

# =====================================================
# STEP 4 — ADD TO RAG
# =====================================================
st.markdown("## Step 4: Add Diagnosis to Knowledge Base")

if st.button("➕ Add to Knowledge Base"):
    add_to_rag(extraction["text"])
    st.success("Diagnosis added to RAG")

# =====================================================
# STEP 5 — QUERY RAG
# =====================================================
st.markdown("## Step 5: Query Knowledge Base")

context_docs = query_rag(summary.get("final_diagnosis", ""))

if context_docs:
    with st.expander("🔍 Retrieved Clinical Context"):
        for i, doc in enumerate(context_docs, start=1):
            st.markdown(f"**Context {i}:**")
            st.write(doc[:700] + "...")

# =====================================================
# STEP 6 — GENERATE PLAN
# =====================================================
st.markdown("## Step 6: Generate Treatment Plan")

if st.button("🧠 Generate Treatment Plan"):
    with st.spinner("Generating treatment plan..."):
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

# =====================================================
# STEP 7 — DISPLAY PLAN
# =====================================================
st.markdown("## Step 7: Treatment Plan")

treatment_plan = st.session_state["plan_data"]["treatment_plan"]

for section, steps in treatment_plan.items():
    st.markdown(f"### {section.replace('_', ' ').title()}")
    for step in steps:
        st.markdown(f"- {step}")

# =====================================================
# STEP 8 — GENERATE PDF
# =====================================================
st.markdown("## Step 8: Generate PDF Report")

if st.button("📄 Generate PDF"):
    pdf_buffer = build_treatment_plan_pdf(treatment_plan)
    st.session_state["pdf"] = pdf_buffer
    st.success("PDF generated successfully")

# =====================================================
# STEP 9 — DOWNLOAD PDF
# =====================================================
st.markdown("## Step 9: Download Report")

if "pdf" in st.session_state:
    st.download_button(
        "⬇️ Download Treatment Report",
        st.session_state["pdf"],
        file_name="Patient_Treatment_Plan_Report.pdf",
        mime="application/pdf"
    )
