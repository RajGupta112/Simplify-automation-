import logging
import os

from django.conf import settings

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    ListFlowable,
    ListItem,
)

logger = logging.getLogger(__name__)


class PDFService:

    def generate_audit_report(self, lead) -> str:

        reports_dir = os.path.join(settings.MEDIA_ROOT, "reports")
        os.makedirs(reports_dir, exist_ok=True)

        file_path = os.path.join(reports_dir, f"{lead.id}.pdf")

        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=30,
        )

        styles = getSampleStyleSheet()

        title = ParagraphStyle(
            "title",
            parent=styles["Heading1"],
            fontSize=22,
            spaceAfter=15,
        )

        h2 = ParagraphStyle(
            "h2",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#1F3A5F"),
            spaceBefore=12,
            spaceAfter=8,
        )

        body = ParagraphStyle(
            "body",
            parent=styles["BodyText"],
            fontSize=10,
            leading=14,
            spaceAfter=6,
        )

        elements = []

        # ---------------- TITLE ----------------
        elements.append(Paragraph("AI Company Audit Report", title))
        elements.append(Spacer(1, 10))

        # ---------------- COMPANY TABLE ----------------
        company_table = Table([
            ["Company", lead.company_name],
            ["Website", lead.website],
            ["Industry", lead.industry],
            ["Business Goal", lead.business_goal],
        ], colWidths=[140, 340])

        company_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#1F3A5F")),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))

        elements.append(company_table)
        elements.append(Spacer(1, 12))

        enrichment = lead.enrichment_data or {}

        # ---------------- AI SUMMARY ----------------
        elements.append(Paragraph("AI Summary", h2))
        elements.append(Paragraph(lead.ai_summary or "N/A", body))

        # ---------------- PAIN POINTS ----------------
        elements.append(Paragraph("Pain Points", h2))

        pain_points = enrichment.get("pain_points", [])
        if pain_points:
            elements.append(ListFlowable(
                [ListItem(Paragraph(p, body)) for p in pain_points],
                bulletType="bullet"
            ))
        else:
            elements.append(Paragraph("No pain points found", body))

        # ---------------- AI OPPORTUNITIES ----------------
        elements.append(Paragraph("AI Opportunities", h2))

        opportunities = enrichment.get("ai_opportunities", [])
        if opportunities:
            elements.append(ListFlowable(
                [ListItem(Paragraph(o, body)) for o in opportunities],
                bulletType="bullet"
            ))
        else:
            elements.append(Paragraph("No AI opportunities found", body))

        # ---------------- AUTOMATION RECOMMENDATIONS ----------------
        elements.append(Paragraph("Automation Recommendations", h2))

        recs = lead.ai_recommendations or []
        if recs:
            elements.append(ListFlowable(
                [ListItem(Paragraph(r, body)) for r in recs],
                bulletType="bullet"
            ))
        else:
            elements.append(Paragraph("No recommendations", body))

        # ---------------- WEBSITE INSIGHTS ----------------
        elements.append(Paragraph("Website Insights", h2))

        elements.append(Paragraph(
            f"<b>Title:</b> {enrichment.get('title', '')}", body
        ))
        elements.append(Paragraph(
            f"<b>Description:</b> {enrichment.get('description', '')}", body
        ))
        elements.append(Paragraph(
            f"<b>Technologies:</b> {', '.join(enrichment.get('technologies', []))}", body
        ))

        # ---------------- WHAT NEEDS IMPROVEMENT (NEW SECTION) ----------------
        elements.append(Paragraph("What Needs Improvement", h2))

        improvements = [
            "AI onboarding flow should be more structured and personalized",
            "Add better lead scoring before AI analysis",
            "Improve website scraping depth (content + metadata + blog pages)",
            "Normalize AI output structure before PDF generation",
            "Add caching to avoid repeated Gemini calls",
        ]

        elements.append(ListFlowable(
            [ListItem(Paragraph(i, body)) for i in improvements],
            bulletType="bullet"
        ))

        # ---------------- BUILD PDF ----------------
        doc.build(elements)

        logger.info(f"PDF generated: {file_path}")

        return file_path


pdf_service = PDFService()