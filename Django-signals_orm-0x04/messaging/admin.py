
from django.contrib import admin
from .models import Message, Notification


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "timestamp")
    search_fields = ("sender__username", "receiver__username", "content")
    ordering = ("-timestamp",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "created_at", "read")
    list_filter = ("read",)
    search_fields = ("user__username", "message__content")
