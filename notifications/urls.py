from django.urls import path
from . import views

urlpatterns = [
    path('preferences/', views.notification_preferences, name='notification_preferences'),
    path('test-email/', views.send_test_email, name='send_test_email'),
]
