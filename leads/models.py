from django.db import models
import uuid


class Lead(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    # User Submitted Data
    full_name = models.CharField(max_length=255)

    email = models.EmailField()

    company_name = models.CharField(max_length=255)

    website = models.URLField()

    industry = models.CharField(
        max_length=255,
        blank=True
    )

    business_goal = models.TextField(
        blank=True
    )

    # Workflow
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    # AI / Enrichment Data
    enrichment_data = models.JSONField(
        default=dict,
        blank=True
    )

    ai_summary = models.TextField(
        blank=True
    )

    ai_recommendations = models.JSONField(
        default=list,
        blank=True
    )

    personalized_email = models.TextField(
        blank=True
    )

    # Google Integrations
    sheets_row_id = models.CharField(
        max_length=255,
        blank=True
    )

    drive_file_id = models.CharField(
        max_length=255,
        blank=True
    )

    # Error Handling
    error_message = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["company_name"]),
        ]

    def __str__(self):
        return f"{self.company_name} ({self.status})"


class AuditReport(models.Model):

    class Status(models.TextChoices):
        GENERATING = "generating", "Generating"
        READY = "ready", "Ready"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    lead = models.OneToOneField(
        Lead,
        on_delete=models.CASCADE,
        related_name="report"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.GENERATING
    )

    pdf_file = models.FileField(
        upload_to="reports/",
        blank=True,
        null=True
    )

    drive_file_url = models.URLField(
        blank=True
    )

    report_content = models.JSONField(
        default=dict,
        blank=True
    )

    error_message = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.lead.company_name} Report"