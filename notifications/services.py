from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
import logging

from .models import EmailNotification, NotificationPreference

logger = logging.getLogger(__name__)


class EmailNotificationService:
    """Service class for handling email notifications"""

    @staticmethod
    def get_user_preferences(user):
        """Get or create notification preferences for a user"""
        preferences, created = NotificationPreference.objects.get_or_create(user=user)
        return preferences

    @staticmethod
    def send_email_notification(recipient, notification_type, subject, html_content, text_content=None):
        """Send an email notification and log it"""
        try:
            # Create notification record
            notification = EmailNotification.objects.create(
                recipient=recipient,
                notification_type=notification_type,
                subject=subject,
                status='pending'
            )

            # If no text content provided, strip HTML tags
            if not text_content:
                text_content = strip_tags(html_content)

            # Send email
            send_mail(
                subject=subject,
                message=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                html_message=html_content,
                fail_silently=False,
            )

            # Mark as sent
            notification.status = 'sent'
            notification.sent_at = timezone.now()
            notification.save()

            logger.info(f"Email notification sent to {recipient.email}: {subject}")
            return True

        except Exception as e:
            # Mark as failed
            notification.status = 'failed'
            notification.error_message = str(e)
            notification.save()

            logger.error(f"Failed to send email to {recipient.email}: {str(e)}")
            return False

    @classmethod
    def send_match_notification(cls, user, matched_user):
        """Send notification when users match"""
        preferences = cls.get_user_preferences(user)
        
        if not preferences.email_on_match or not user.email:
            return False

        context = {
            'user': user,
            'matched_user': matched_user,
            'site_name': 'Resonate',
        }

        subject = f"🎉 You have a new match on Resonate!"
        html_content = render_to_string('notifications/emails/match_notification.html', context)
        
        return cls.send_email_notification(user, 'match', subject, html_content)

    @classmethod
    def send_like_notification(cls, liked_user, liker_user):
        """Send notification when someone likes your profile"""
        preferences = cls.get_user_preferences(liked_user)
        
        if not preferences.email_on_like or not liked_user.email:
            return False

        context = {
            'user': liked_user,
            'liker': liker_user,
            'site_name': 'Resonate',
        }

        subject = f"💖 Someone liked your profile on Resonate!"
        html_content = render_to_string('notifications/emails/like_notification.html', context)
        
        return cls.send_email_notification(liked_user, 'like', subject, html_content)

    @classmethod
    def send_welcome_email(cls, user):
        """Send welcome email to new users"""
        if not user.email:
            return False

        context = {
            'user': user,
            'site_name': 'Resonate',
        }

        subject = f"Welcome to Resonate - Find Your Perfect Match!"
        html_content = render_to_string('notifications/emails/welcome_email.html', context)
        
        return cls.send_email_notification(user, 'welcome', subject, html_content)

    @classmethod
    def send_profile_view_notification(cls, profile_owner, viewer):
        """Send notification when someone views your profile"""
        preferences = cls.get_user_preferences(profile_owner)
        
        if not preferences.email_on_profile_view or not profile_owner.email:
            return False

        context = {
            'user': profile_owner,
            'viewer': viewer,
            'site_name': 'Resonate',
        }

        subject = f"👁️ Someone viewed your profile on Resonate!"
        html_content = render_to_string('notifications/emails/profile_view_notification.html', context)
        
        return cls.send_email_notification(profile_owner, 'profile_view', subject, html_content)
