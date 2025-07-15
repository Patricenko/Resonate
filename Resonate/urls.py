"""
URL configuration for Resonate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static
from django.shortcuts import render

def index_view(request):
    return render(request, "index.html")
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('matching/', include('matching.urls', namespace='matching')),
<<<<<<<< HEAD:Dinter/urls.py
========
    path('notifications/', include('notifications.urls')),
>>>>>>>> origin/main:Resonate/urls.py
    path('rtchat/', include('rtchat.urls')),
    path('', index_view, name='index'),  # Homepage view
]

# Serve media files during development
# Serve static and media files when running locally
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


