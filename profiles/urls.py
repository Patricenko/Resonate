from django.contrib import admin
from django.urls import path
from . import views


app_name = 'profiles'

urlpatterns = [
    path('create/', views.create_profile_view),
    path('edit/', views.edit_profile_view),
]
