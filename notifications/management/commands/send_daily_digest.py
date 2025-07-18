from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from notifications.services import EmailNotificationService
from notifications.models import EmailNotification


class Command(BaseCommand):
    help = 'Send daily digest emails to users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run command without actually sending emails',
        )
        parser.add_argument(
            '--user-id',
            type=int,
            help='Send digest to specific user ID only',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        user_id = options.get('user_id')

        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No emails will be sent')
            )

        users_query = User.objects.filter(is_active=True, email__isnull=False)
        if user_id:
            users_query = users_query.filter(id=user_id)

        users_sent = 0
        users_skipped = 0

        for user in users_query:
            try:
                if not hasattr(user, 'notification_preferences'):
                    users_skipped += 1
                    continue

                prefs = user.notification_preferences
                if not any([prefs.email_on_match, prefs.email_on_like, 
                           prefs.email_on_message, prefs.email_on_profile_view]):
                    users_skipped += 1
                    continue

                today = timezone.now().date()
                existing_digest = EmailNotification.objects.filter(
                    recipient=user,
                    notification_type='digest',
                    created_at__date=today
                ).exists()

                if existing_digest:
                    users_skipped += 1
                    continue

                recent_activity = self.get_recent_activity(user)

                if not recent_activity['has_activity']:
                    users_skipped += 1
                    continue

                if not dry_run:
                    success = self.send_digest_email(user, recent_activity)
                    if success:
                        users_sent += 1
                    else:
                        users_skipped += 1
                else:
                    self.stdout.write(f'Would send digest to {user.email}')
                    users_sent += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error processing user {user.id}: {str(e)}')
                )
                users_skipped += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Digest emails processed: {users_sent} sent, {users_skipped} skipped'
            )
        )

    def get_recent_activity(self, user):
        yesterday = timezone.now() - timedelta(days=1)

        recent_likes = user.received_likes.filter(created_at__gte=yesterday).count()

        recent_matches = user.matches_as_user1.filter(created_at__gte=yesterday).count() + \
                        user.matches_as_user2.filter(created_at__gte=yesterday).count()

        has_activity = recent_likes > 0 or recent_matches > 0

        return {
            'has_activity': has_activity,
            'recent_likes': recent_likes,
            'recent_matches': recent_matches,
        }

    def send_digest_email(self, user, activity):
        try:
            from django.template.loader import render_to_string
            from django.conf import settings

            context = {
                'user': user,
                'activity': activity,
                'site_name': 'Resonate',
            }

            subject = f"📊 Your Daily Resonate Activity Summary"
            html_content = render_to_string('notifications/emails/daily_digest.html', context)
            
            return EmailNotificationService.send_email_notification(
                user, 'digest', subject, html_content
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to send digest email to {user.email}: {str(e)}')
            )
            return False
