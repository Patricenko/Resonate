from django.contrib import admin
from .models import NotificationPreference, EmailNotification


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_on_match', 'email_on_like', 'email_on_message', 'email_on_profile_view', 'daily_digest']
    list_filter = ['email_on_match', 'email_on_like', 'email_on_message', 'email_on_profile_view', 'daily_digest']
    search_fields = ['user__username', 'user__email']


@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'subject', 'status', 'created_at', 'sent_at']
    list_filter = ['notification_type', 'status', 'created_at']
    search_fields = ['recipient__username', 'recipient__email', 'subject']
    readonly_fields = ['created_at', 'sent_at']
