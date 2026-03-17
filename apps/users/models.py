from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(models.Model):
    SECURITY_CLEARANCES = [
        ("basic", "Basic"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("admin", "Administrator"),
    ]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    security_clearance = models.CharField(
        max_length=20, choices=SECURITY_CLEARANCES, default="basic"
    )

    def __str__(self):
        return f"{self.username} ({self.email})"
