"""
PDF Builder for AI Treatment Planner

Generates a clinician-friendly Treatment Plan PDF
from a structured treatment plan dictionary.
"""

import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


# =====================================================
# MAIN PDF GENERATION FUNCTION
# =====================================================
def build_treatment_plan_pdf(treatment_plan: dict) -> io.BytesIO:
    """
    Build a Treatment Plan PDF in memory.

    Args:
        treatment_plan (dict): Structured treatment plan
                               (treatment_plan["treatment_plan"])

    Returns:
        io.BytesIO: PDF buffer ready for download
    """

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    x_margin = 0.75 * inch
    y_position = height - 1 * inch

    # ===================== TITLE =====================
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x_margin, y_position, "AI-Generated Treatment Plan")
    y_position -= 30

    c.setFont("Helvetica", 10)
    c.drawString(
        x_margin,
        y_position,
        "This document provides a structured treatment plan based on the clinical diagnosis."
    )
    y_position -= 40

    # ===================== CONTENT =====================
    for section, steps in treatment_plan.items():
        # New page check
        if y_position < 100:
            c.showPage()
            c.setFont("Helvetica", 10)
            y_position = height - 1 * inch

        # Section header
        c.setFont("Helvetica-Bold", 12)
        section_title = section.replace("_", " ").title()
        c.drawString(x_margin, y_position, section_title)
        y_position -= 20

        # Section content
        c.setFont("Helvetica", 10)
        for step in steps:
            if y_position < 80:
                c.showPage()
                c.setFont("Helvetica", 10)
                y_position = height - 1 * inch

            c.drawString(x_margin + 15, y_position, f"- {step}")
            y_position -= 15

        y_position -= 15

    # ===================== FOOTER =====================
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(
        x_margin,
        40,
        "Note: This AI-generated plan is for clinical decision support only "
        "and should not replace professional medical judgment."
    )

    c.save()
    buffer.seek(0)

    return buffer
