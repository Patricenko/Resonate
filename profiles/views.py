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

    interests_list = []
    if profile.interests:
        interests_list = [i.strip() for i in profile.interests.split(",") if i.strip()]

    return render(request, "profiles/profile.html", {
        "profile": profile,
        "interests_list": interests_list,
    })

@login_required
def create_profile_view(request):
    # Redirect if profile already exists
    if hasattr(request.user, 'profile'):
        return redirect('profiles:profile_me')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.is_public = True  # force public
            profile.save()
            return redirect(reverse('profiles:profile_detail', kwargs={'user_id': request.user.id}))
    else:
        form = ProfileForm()
    return render(request, 'create_profile.html', {'form': form, 'GOOGLE_API_KEY': GOOGLE_API_KEY})

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

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.is_public = True
            profile.save()
            return redirect('profiles:profile_detail', user_id=request.user.id)
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'premade_interests': premade_interests,
    }
    return render(request, 'edit_profile.html', context)

