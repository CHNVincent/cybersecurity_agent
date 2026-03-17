from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "email",
        "security_clearance",
        "date_joined",
        "is_active",
    ]
    list_filter = ["security_clearance", "is_active", "date_joined"]
    search_fields = ["username", "email"]
    readonly_fields = ["date_joined"]
