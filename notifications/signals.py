from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from matching.models import Like, Match
from rtchat.models import GroupMessage
from .services import EmailNotificationService
from .models import NotificationPreference


@receiver(post_save, sender=User)
def create_notification_preferences(sender, instance, created, **kwargs):
    """Create default notification preferences for new users"""
    if created:
        NotificationPreference.objects.create(user=instance)
        # Send welcome email
        EmailNotificationService.send_welcome_email(instance)


@receiver(post_save, sender=Match)
def send_match_notification(sender, instance, created, **kwargs):
    """Send email notifications when users match"""
    if created:
        # Send notification to both users
        EmailNotificationService.send_match_notification(instance.user1, instance.user2)
        EmailNotificationService.send_match_notification(instance.user2, instance.user1)


@receiver(post_save, sender=Like)
def send_like_notification(sender, instance, created, **kwargs):
    """Send email notification when someone likes a profile"""
    if created:
        EmailNotificationService.send_like_notification(instance.liked, instance.liker)


@receiver(post_save, sender=GroupMessage)
def send_message_notification(sender, instance, created, **kwargs):
    """Send email notification when someone sends a message"""
    if created and instance.group.is_private:
        # Get other members of the chat group (excluding the sender)
        recipients = instance.group.members.exclude(id=instance.author.id)
        
        # Create message preview
        if instance.body:
            message_preview = instance.body[:100] + "..." if len(instance.body) > 100 else instance.body
        elif instance.file:
            message_preview = f"📎 Sent a file: {instance.filename}"
        else:
            message_preview = "Sent a message"
        
        # Send notification to each recipient
        for recipient in recipients:
            EmailNotificationService.send_message_notification(recipient, instance.author, message_preview)
