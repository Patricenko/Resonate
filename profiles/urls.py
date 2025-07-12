from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


app_name = 'profiles'

urlpatterns = [
    path('me/', views.profile_me_view, name='profile_me'),
    path('create/', views.create_profile_view, name='create_profile'),
    path('edit/', views.edit_profile_view, name='edit_profile'),
    path('<int:user_id>/', views.profile_detail_view, name='profile_detail'),
]