from django.db import models
from apps.conversations.models import Conversation


class AuditReport(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=500)
    language = models.CharField(max_length=50, default="unknown")
    vulnerabilities_found = models.IntegerField(default=0)
    severity_score = models.FloatField(default=0.0)  # 1-10 scale
    report_summary = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audit Report: {self.file_path}"


class SkillInstallLog(models.Model):
    skill_name = models.CharField(max_length=200)
    version = models.CharField(max_length=50)
    installed_at = models.DateTimeField(auto_now_add=True)
    installed_by = models.CharField(max_length=150)  # Username
    status = models.CharField(
        max_length=50,
        choices=[
            ("success", "Success"),
            ("failed", "Failed"),
        ],
    )

    def __str__(self):
        return f"{self.skill_name} v{self.version} - {self.status}"
