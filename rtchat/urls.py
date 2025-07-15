from django.urls import path
from .views import chat_view, get_or_create_chatroom

app_name = 'rtchat'

urlpatterns = [
    path('', chat_view, name='chat'),
    path('chat/<str:group_name>/', chat_view, name='chat'),
    path('chat/private/<str:username>/', get_or_create_chatroom, name='get_or_create_chatroom'),
]