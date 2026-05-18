import logging

from celery import shared_task
from django.db import transaction

from .models import Lead
from .services.enrichment_service import enrichment_service
from .services.ai_service import ai_service
from .services.pdf_service import pdf_service
from .services.email_service import email_service

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=2)
def process_lead_workflow(self, lead_id):
    lead = None

    try:
        # -----------------------------------
        # GET LEAD
        # -----------------------------------
        lead = Lead.objects.get(id=lead_id)

        lead.status = Lead.Status.PROCESSING
        lead.error_message = ""
        lead.save()

        logger.info(f"Processing lead: {lead.company_name}")

        # -----------------------------------
        # ENRICHMENT
        # -----------------------------------
        enrichment_result = enrichment_service.enrich_company(
            lead.website
        )

        if not enrichment_result["success"]:
            lead.status = Lead.Status.FAILED
            lead.error_message = enrichment_result["error"]
            lead.save()
            logger.error(f"Enrichment failed: {lead.company_name}")
            return

        lead.enrichment_data = enrichment_result["data"]
        lead.save()

        logger.info(f"Enrichment completed: {lead.company_name}")

        # -----------------------------------
        # AI ANALYSIS
        # -----------------------------------
        ai_result = ai_service.analyze_company(
            lead,
            lead.enrichment_data
        )

        if not ai_result["success"]:
            lead.status = Lead.Status.FAILED
            lead.error_message = ai_result["error"]
            lead.save()
            logger.error(f"AI failed: {lead.company_name}")
            return

        ai_data = ai_result["data"]

        lead.ai_summary = ai_data.get("company_summary", "")
        lead.ai_recommendations = ai_data.get("automation_recommendations", [])
        lead.personalized_email = ai_data.get("personalized_email", "")
        lead.save()

        logger.info(f"AI completed: {lead.company_name}")

        # -----------------------------------
        # PDF GENERATION (SAFE)
        # -----------------------------------
        pdf_path = None

        try:
            pdf_path = pdf_service.generate_audit_report(lead)
            logger.info(f"PDF generated: {pdf_path}")

        except Exception as pdf_error:
            logger.error(f"PDF failed: {pdf_error}")
            pdf_path = None

        # -----------------------------------
        # EMAIL SENDING (SAFE)
        # -----------------------------------
        try:
            email_service.send_audit_report(
                lead=lead,
                pdf_path=pdf_path,
            )
            logger.info(f"Email sent: {lead.email}")

        except Exception as email_error:
            logger.error(f"Email failed: {email_error}")
            # DO NOT fail whole workflow

        # -----------------------------------
        # FINAL STATUS
        # -----------------------------------
        lead.status = Lead.Status.COMPLETED
        lead.save()

        logger.info(f"Workflow completed: {lead.company_name}")

    except Lead.DoesNotExist:
        logger.error(f"Lead not found: {lead_id}")
        return

    except Exception as error:
        logger.error(f"Workflow crashed: {error}")

        if lead:
            try:
                lead.status = Lead.Status.FAILED
                lead.error_message = str(error)
                lead.save()
            except Exception:
                pass

        # optional retry
        raise self.retry(exc=error, countdown=30)