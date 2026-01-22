from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch


def build_treatment_plan_pdf(patient: dict, summary: dict, plan: dict) -> str:
    """
    Builds a professional, hospital-style PDF treatment report
    """

    filename = "AI_Treatment_Plan_Report.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        alignment=1
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Heading2"],
        spaceAfter=12
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        spaceAfter=8
    )

    story = []

    # -------------------------------------------------
    # TITLE
    # -------------------------------------------------
    story.append(Paragraph("AI-Generated Treatment Plan", title_style))
    story.append(Spacer(1, 0.3 * inch))

    # -------------------------------------------------
    # PATIENT DETAILS
    # -------------------------------------------------
    story.append(Paragraph("Patient Details", section_style))
    story.append(Paragraph(f"<b>Name:</b> {patient.get('name')}", normal_style))
    story.append(Paragraph(f"<b>Age:</b> {patient.get('age')}", normal_style))
    story.append(Paragraph(f"<b>Gender:</b> {patient.get('gender')}", normal_style))
    story.append(Spacer(1, 0.2 * inch))

    # -------------------------------------------------
    # CLINICAL SUMMARY
    # -------------------------------------------------
    story.append(Paragraph("Clinical Summary", section_style))
    story.append(Paragraph(
        f"<b>Chief Complaint:</b> {summary.get('chief_complaint')}",
        normal_style
    ))
    story.append(Paragraph(
        f"<b>Identified Condition:</b> {plan.get('identified_problem')}",
        normal_style
    ))
    story.append(Spacer(1, 0.2 * inch))

    # -------------------------------------------------
    # TREATMENT PLAN
    # -------------------------------------------------
    story.append(Paragraph("Treatment Plan", section_style))

    treatment_sections = plan.get("treatment_plan", {}).get(
        "treatment_sections", {}
    )

    for section, items in treatment_sections.items():
        story.append(Paragraph(section, styles["Heading3"]))

        bullet_items = [
            ListItem(Paragraph(item, normal_style))
            for item in items
        ]

        story.append(
            ListFlowable(
                bullet_items,
                bulletType="bullet",
                start="circle"
            )
        )
        story.append(Spacer(1, 0.15 * inch))

    # -------------------------------------------------
    # COST ESTIMATION
    # -------------------------------------------------
    cost = plan.get("estimated_cost", {})
    story.append(Paragraph("Estimated Cost", section_style))
    story.append(Paragraph(f"Consultation: {cost.get('consultation')}", normal_style))
    story.append(Paragraph(f"Investigations: {cost.get('investigations')}", normal_style))
    story.append(Paragraph(f"Medications: {cost.get('medications')}", normal_style))
    story.append(Paragraph(f"Follow-up: {cost.get('follow_up_cost')}", normal_style))
    story.append(Paragraph(f"Notes: {cost.get('notes')}", normal_style))
    story.append(Spacer(1, 0.2 * inch))

    # -------------------------------------------------
    # APPOINTMENT PLAN
    # -------------------------------------------------
    appt = plan.get("appointment", {})
    story.append(Paragraph("Follow-up & Appointment", section_style))
    story.append(Paragraph(f"Urgency: {appt.get('urgency')}", normal_style))
    story.append(Paragraph(f"Specialist: {appt.get('specialist')}", normal_style))
    story.append(Paragraph(
        f"Recommended Timeline: {appt.get('recommended_timeline')}",
        normal_style
    ))
    story.append(Paragraph(
        f"Follow-up Frequency: {appt.get('follow_up_frequency')}",
        normal_style
    ))
    story.append(Spacer(1, 0.3 * inch))

    # -------------------------------------------------
    # DISCLAIMER
    # -------------------------------------------------
    story.append(Paragraph(
        "<i>Disclaimer: This AI-generated report is intended for clinical "
        "decision support only. Final diagnosis and treatment decisions "
        "must be made by a licensed medical professional.</i>",
        styles["Italic"]
    ))

    # -------------------------------------------------
    # BUILD PDF
    # -------------------------------------------------
    doc.build(story)

    return filename
