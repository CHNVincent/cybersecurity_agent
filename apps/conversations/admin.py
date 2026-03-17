from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ["title", "owner", "created_at", "updated_at", "is_archived"]
    list_filter = ["is_archived", "created_at", "updated_at"]
    search_fields = ["title", "owner__username"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["conversation", "role", "timestamp", "is_flagged"]
    list_filter = ["role", "is_flagged", "timestamp"]
    search_fields = ["content"]
    readonly_fields = ["timestamp"]
