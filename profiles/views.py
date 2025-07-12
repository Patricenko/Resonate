from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
from django.urls import reverse
import os
from dotenv import load_dotenv

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # Replace with your actual Google Maps API key

@login_required
def profile_detail_view(request, user_id):
    profile = get_object_or_404(Profile, user__id=user_id)
    return render(request, "profiles/profile.html", {"profile": profile})

@login_required
def create_profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            # Tu je zmena – použitie namespaces
            return redirect(reverse('profiles:profile_detail', kwargs={'user_id': request.user.id}))
    else:
        form = ProfileForm()
    return render(request, 'create_profile.html', {'form': form, 'GOOGLE_API_KEY': GOOGLE_API_KEY})

@login_required
def edit_profile_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('create_profile')  # Redirect to creation if profile doesn't exist

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', user_id=request.user.id)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})
