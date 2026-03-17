from django.contrib import admin
from .models import AuditReport, SkillInstallLog


@admin.register(AuditReport)
class AuditReportAdmin(admin.ModelAdmin):
    list_display = [
        "conversation",
        "file_path",
        "language",
        "vulnerabilities_found",
        "severity_score",
        "generated_at",
    ]
    list_filter = [
        "language",
        "vulnerabilities_found",
        "severity_score",
        "generated_at",
    ]
    search_fields = ["file_path", "conversation__title"]
    readonly_fields = ["generated_at"]


@admin.register(SkillInstallLog)
class SkillInstallLogAdmin(admin.ModelAdmin):
    list_display = ["skill_name", "version", "installed_at", "installed_by", "status"]
    list_filter = ["status", "installed_at", "version"]
    search_fields = ["skill_name", "installed_by"]
    readonly_fields = ["installed_at"]
