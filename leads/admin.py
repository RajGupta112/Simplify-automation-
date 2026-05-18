

# Register your models here.
from django.contrib import admin

from .models import Lead, AuditReport


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):

    list_display = (
        "company_name",
        "full_name",
        "email",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "company_name",
        "email",
    )


@admin.register(AuditReport)
class AuditReportAdmin(admin.ModelAdmin):

    list_display = (
        "lead",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
    )