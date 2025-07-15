from django.urls import re_path
from .consumers import *

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>[^/]+)/?$', ChatroomConsumer.as_asgi()),
]