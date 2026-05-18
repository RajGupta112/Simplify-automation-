import logging

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


class EmailService:

    def send_audit_report(self, lead, pdf_path: str = None) -> bool:

        try:
            subject = f"AI Audit Report for {lead.company_name}"

            body = lead.personalized_email or (
                f"Hi {lead.company_name},\n\n"
                "Please find your AI audit report attached."
            )

            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[lead.email],
            )

            # ----------------------------
            # ATTACH PDF SAFELY
            # ----------------------------
            if pdf_path:
                try:
                    email.attach_file(pdf_path)
                except Exception as e:
                    logger.error(f"PDF attach failed: {e}")

            email.send(fail_silently=False)

            logger.info(f"Email sent to: {lead.email}")

            return True

        except Exception as error:
            logger.error(f"Email sending failed: {error}")
            return False


email_service = EmailService()