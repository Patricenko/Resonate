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
    if request.user.id != user_id:
        return redirect('profiles:profile_me')
    profile = get_object_or_404(Profile, user__id=user_id)

    # Prepare interests list safely
    interests_list = []
    if profile.interests:
        interests_list = [i.strip() for i in profile.interests.split(",") if i.strip()]

    return render(request, "profiles/profile.html", {
        "profile": profile,
        "interests_list": interests_list,
    })


@login_required
def profile_me_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    interests_list = [i.strip() for i in (profile.interests or "").split(",") if i.strip()]
    return render(request, "profiles/profile.html", {
        "profile": profile,
        "interests_list": interests_list,
    })


@login_required
def create_profile_view(request):
    # Redirect if profile already exists
    if hasattr(request.user, 'profile'):
        return redirect('profiles:profile_me')

    premade_interests = [
        "Music", "Sports", "Art", "Technology", "Gaming",
        "Reading", "Travel", "Cooking", "Fitness", "Movies"
    ]

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.is_public = True

            # Clean and save interests manually
            interests_str = request.POST.get('interests', '')
            interests_list = [i.strip().lower() for i in interests_str.split(",") if i.strip()]
            profile.interests = ",".join(interests_list)

            profile.save()
            return redirect('profiles:profile_me')

    else:
        form = ProfileForm()

    return render(request, 'create_profile.html', {
        'form': form,
        'GOOGLE_API_KEY': GOOGLE_API_KEY,
        'premade_interests': premade_interests,
    })
@login_required
def edit_profile_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('profiles:create_profile')

    premade_interests = [
        "Music", "Sports", "Art", "Technology", "Gaming",
        "Reading", "Travel", "Cooking", "Fitness", "Movies"
    ]

    current_interests = []
    if profile.interests:
        current_interests = [i.strip().lower() for i in profile.interests.split(",") if i.strip()]

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            # Save interests as a clean comma-separated lowercase string
            interests_str = request.POST.get('interests', '')
            interests_list = [i.strip().lower() for i in interests_str.split(",") if i.strip()]
            profile.interests = ",".join(interests_list)
            profile.is_public = True
            profile.save()
            return redirect('profiles:profile_me')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'premade_interests': premade_interests,
        'current_interests': current_interests,
        'GOOGLE_API_KEY': GOOGLE_API_KEY,
    }
    return render(request, 'edit_profile.html', context)

