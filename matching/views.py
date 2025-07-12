from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from profiles.models import Profile
from .models import Like, Match, Pass
import json


@login_required
def match_view(request):
    """Main matching interface - show potential matches"""
    current_user = request.user
    
    # Get users that current user has already liked or passed on
    liked_users = Like.objects.filter(liker=current_user).values_list('liked', flat=True)
    passed_users = Pass.objects.filter(passer=current_user).values_list('passed', flat=True)
    interacted_users = list(liked_users) + list(passed_users)
    
    # Get current user's preferences
    try:
        current_profile = Profile.objects.get(user=current_user)
        preferred_gender = current_profile.preferred_gender
        preferred_age_min = current_profile.preferred_age_min
        preferred_age_max = current_profile.preferred_age_max
    except Profile.DoesNotExist:
        # If user doesn't have a profile, redirect to create one
        return redirect('profiles:create_profile')
    
    # Build filter query for potential matches
    potential_matches = Profile.objects.filter(
        is_public=True,
        age__gte=preferred_age_min,
        age__lte=preferred_age_max
    ).exclude(
        user=current_user
    ).exclude(
        user__in=interacted_users
    )
    
    # Filter by preferred gender if specified
    if preferred_gender != 'B' and preferred_gender != 'O':
        potential_matches = potential_matches.filter(gender=preferred_gender)
    
    # Get the first potential match
    next_profile = potential_matches.first()
    
    context = {
        'profile': next_profile,
        'has_more_profiles': potential_matches.count() > 1
    }
    
    return render(request, 'match.html', context)


@login_required
def like_profile(request):
    """Handle liking a profile via AJAX"""
    if request.method == 'POST':
        data = json.loads(request.body)
        profile_id = data.get('profile_id')
        
        try:
            liked_profile = Profile.objects.get(id=profile_id)
            liked_user = liked_profile.user
            
            # Create the like
            like, created = Like.objects.get_or_create(
                liker=request.user,
                liked=liked_user
            )
            
            # Check if there's a mutual like (match)
            mutual_like = Like.objects.filter(
                liker=liked_user,
                liked=request.user
            ).exists()
            
            is_match = False
            if mutual_like:
                # Create a match
                match, match_created = Match.objects.get_or_create(
                    user1=min(request.user, liked_user, key=lambda u: u.id),
                    user2=max(request.user, liked_user, key=lambda u: u.id)
                )
                is_match = match_created
            
            return JsonResponse({
                'success': True,
                'is_match': is_match,
                'liked_user': liked_user.username
            })
            
        except Profile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Profile not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def pass_profile(request):
    """Handle passing on a profile via AJAX"""
    if request.method == 'POST':
        data = json.loads(request.body)
        profile_id = data.get('profile_id')
        
        try:
            passed_profile = Profile.objects.get(id=profile_id)
            passed_user = passed_profile.user
            
            # Create the pass
            pass_obj, created = Pass.objects.get_or_create(
                passer=request.user,
                passed=passed_user
            )
            
            return JsonResponse({'success': True})
            
        except Profile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Profile not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def matches_view(request):
    """Show all matches for the current user"""
    current_user = request.user
    
    # Get all matches where current user is either user1 or user2
    matches = Match.objects.filter(
        Q(user1=current_user) | Q(user2=current_user)
    ).order_by('-created_at')
    
    # Prepare match data with the other user's profile
    match_data = []
    for match in matches:
        other_user = match.user2 if match.user1 == current_user else match.user1
        try:
            other_profile = Profile.objects.get(user=other_user)
            match_data.append({
                'match': match,
                'other_user': other_user,
                'other_profile': other_profile
            })
        except Profile.DoesNotExist:
            continue
    
    context = {
        'matches': match_data
    }
    
    return render(request, 'matches.html', context)
