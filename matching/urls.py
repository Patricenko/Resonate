from django.urls import path
from . import views

app_name = 'matching'

urlpatterns = [
    path('', views.match_view, name='match'),
    path('like/', views.like_profile, name='like_profile'),
    path('pass/', views.pass_profile, name='pass_profile'),
    path('matches/', views.matches_view, name='matches'),
    path('api/new-matches-count/', views.get_new_matches_count, name='new_matches_count'),
    path('api/mark-match-seen/', views.mark_match_seen, name='mark_match_seen'),
    path('api/latest-match/', views.get_latest_match, name='latest_match'),
]

