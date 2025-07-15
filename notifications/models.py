from django.db import models
from django.contrib.auth.models import User


class NotificationPreference(models.Model):
    """Model to store user email notification preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    email_on_match = models.BooleanField(default=True)
    email_on_like = models.BooleanField(default=True)
    email_on_message = models.BooleanField(default=True)
    email_on_profile_view = models.BooleanField(default=False)
    daily_digest = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s notification preferences"


class EmailNotification(models.Model):
    """Model to track sent email notifications"""
    NOTIFICATION_TYPES = [
        ('match', 'New Match'),
        ('like', 'New Like'),
        ('message', 'New Message'),
        ('profile_view', 'Profile View'),
        ('welcome', 'Welcome Email'),
        ('digest', 'Daily Digest'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    subject = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.notification_type} notification to {self.recipient.username}"

    class Meta:
        ordering = ['-created_at']
