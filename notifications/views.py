from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from .models import NotificationPreference
from .services import EmailNotificationService


@login_required
def notification_preferences(request):
    """View to manage user notification preferences"""
    preferences, created = NotificationPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        preferences.email_on_match = request.POST.get('email_on_match') == 'on'
        preferences.email_on_like = request.POST.get('email_on_like') == 'on'
        preferences.email_on_message = request.POST.get('email_on_message') == 'on'
        preferences.email_on_profile_view = request.POST.get('email_on_profile_view') == 'on'
        preferences.daily_digest = request.POST.get('daily_digest') == 'on'
        preferences.save()
        
        messages.success(request, 'Your notification preferences have been updated!')
        return redirect('notification_preferences')
    
    context = {
        'preferences': preferences,
    }
    return render(request, 'notifications/preferences.html', context)


@login_required
@require_POST
@csrf_exempt
def send_test_email(request):
    """Send a test email to the current user"""
    try:
        data = json.loads(request.body)
        notification_type = data.get('type', 'welcome')
        
        if notification_type == 'welcome':
            success = EmailNotificationService.send_welcome_email(request.user)
        elif notification_type == 'match':
            # For testing, we'll send a match notification with the user as both participants
            success = EmailNotificationService.send_match_notification(request.user, request.user)
        elif notification_type == 'like':
            success = EmailNotificationService.send_like_notification(request.user, request.user)
        elif notification_type == 'profile_view':
            success = EmailNotificationService.send_profile_view_notification(request.user, request.user)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid notification type'})
        
        if success:
            return JsonResponse({'success': True, 'message': 'Test email sent successfully!'})
        else:
            return JsonResponse({'success': False, 'error': 'Failed to send test email'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
