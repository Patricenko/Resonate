from django.urls import path
from . import views

app_name = 'matching'

urlpatterns = [
    path('', views.match_view, name='match'),
    path('like/', views.like_profile, name='like_profile'),
    path('pass/', views.pass_profile, name='pass_profile'),
    path('matches/', views.matches_view, name='matches'),
]

