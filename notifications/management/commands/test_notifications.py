from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from notifications.services import EmailNotificationService
from notifications.models import NotificationPreference, EmailNotification


class Command(BaseCommand):
    help = 'Test email notification system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default='test@example.com',
            help='Email address to send test notifications to',
        )

    def handle(self, *args, **options):
        email = options['email']
        
        self.stdout.write(f"🧪 Testing Email Notifications for: {email}")
        self.stdout.write("=" * 50)

        try:
            user = User.objects.get(email=email)
            self.stdout.write(f"✅ Using existing user: {user.username}")
        except User.DoesNotExist:
            user = User.objects.create_user(
                username='testuser',
                email=email,
                first_name='Test',
                last_name='User'
            )
            self.stdout.write(f"✅ Created test user: {user.username}")

        prefs, created = NotificationPreference.objects.get_or_create(user=user)
        if created:
            self.stdout.write("✅ Created notification preferences")

        tests = [
            ('Welcome Email', lambda: EmailNotificationService.send_welcome_email(user)),
            ('Match Notification', lambda: EmailNotificationService.send_match_notification(user, user)),
            ('Like Notification', lambda: EmailNotificationService.send_like_notification(user, user)),
            ('Profile View Notification', lambda: EmailNotificationService.send_profile_view_notification(user, user)),
        ]

        self.stdout.write("\n📧 Testing Email Notifications:")
        self.stdout.write("-" * 30)

        for test_name, test_func in tests:
            self.stdout.write(f"Testing {test_name}...")
            try:
                success = test_func()
                status = "✅ Success" if success else "❌ Failed"
                self.stdout.write(f"   {status}")
            except Exception as e:
                self.stdout.write(f"   ❌ Error: {str(e)}")

        self.stdout.write("\n📊 Email Notification Summary:")
        self.stdout.write("-" * 35)
        total = EmailNotification.objects.filter(recipient=user).count()
        sent = EmailNotification.objects.filter(recipient=user, status='sent').count()
        failed = EmailNotification.objects.filter(recipient=user, status='failed').count()

        self.stdout.write(f"Total notifications: {total}")
        self.stdout.write(f"Sent successfully: {sent}")
        self.stdout.write(f"Failed: {failed}")

        self.stdout.write("\n💡 Since DEBUG=True, emails are printed to console.")
        self.stdout.write("🎉 Testing complete!")
