from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from profiles.models import Profile
from .models import Like, Match, Pass
import json
from django.db.models import Case, When, Value, IntegerField
from django.db.models import Sum
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import googlemaps
from django.conf import settings


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
        interests = current_profile.interests.split(",") if current_profile.interests else []
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

    # location-filtering
    # Filter by location/distance if user has location preferences
    if hasattr(current_profile, 'location') and current_profile.location:
        
        # Initialize Google Maps client
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        
        try:
            # Get coordinates for current user's location
            current_location_result = gmaps.geocode(current_profile.location)
            if current_location_result:
                current_coords = (
                    current_location_result[0]['geometry']['location']['lat'],
                    current_location_result[0]['geometry']['location']['lng']
                )
                
                # Filter profiles within preferred distance (e.g., 50km)
                max_distance_km = getattr(current_profile, 'max_distance', 50)  # Default 50km
                nearby_profiles = []
                
                for profile in potential_matches:
                    if profile.location:
                        try:
                            profile_location_result = gmaps.geocode(profile.location)
                            if profile_location_result:
                                profile_coords = (
                                    profile_location_result[0]['geometry']['location']['lat'],
                                    profile_location_result[0]['geometry']['location']['lng']
                                )
                                distance = geodesic(current_coords, profile_coords).kilometers
                                if distance <= max_distance_km:
                                    nearby_profiles.append(profile.id)
                        except Exception:
                            continue
                
                potential_matches = potential_matches.filter(id__in=nearby_profiles)
                # order by distance
                potential_matches = potential_matches.annotate(
                    distance=Sum(
                        Case(
                            When(id__in=nearby_profiles, then=Value(1)),
                            default=Value(0),
                            output_field=IntegerField()
                        )
                    )
                ).order_by('distance')
        except Exception:
            # If geocoding fails, continue without location filtering
            pass

    # Order potential matches based on distance, interests
    if interests:
        interest_cases = []
        for interest in interests:
            interest_cases.append(
                When(interests__icontains=interest.strip(), then=Value(1))
            )
        
        potential_matches = potential_matches.annotate(
            interest_match_score=Case(
            *interest_cases,
            default=Value(0),
            output_field=IntegerField()
            )
        ).order_by('-interest_match_score', '?')
    else:
        # If no interests, order by creation date or randomly
        potential_matches = potential_matches.order_by('?')

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
            
            match_data = None
            is_match = False
            if mutual_like:
                # Create a match
                match, match_created = Match.objects.get_or_create(
                    user1=min(request.user, liked_user, key=lambda u: u.id),
                    user2=max(request.user, liked_user, key=lambda u: u.id)
                )
                is_match = match_created
                
                if match_created:
                    # Get match data for popup
                    match_data = {
                        'match_id': match.id,
                        'other_user': {
                            'username': liked_user.username,
                            'name': liked_profile.name,
                            'profile_photo': liked_profile.profile_photo.url if liked_profile.profile_photo else None,
                            'age': liked_profile.age
                        }
                    }
            
            return JsonResponse({
                'success': True,
                'is_match': is_match,
                'liked_user': liked_user.username,
                'match_data': match_data
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
                'other_profile': other_profile,
                'is_new': match.is_new_for_user(current_user)
            })
        except Profile.DoesNotExist:
            continue
    
    # Mark all matches as seen when viewing the matches page
    for match in matches:
        match.mark_seen_by_user(current_user)
    
    context = {
        'matches': match_data
    }
    
    return render(request, 'matches.html', context)


@login_required
def get_new_matches_count(request):
    """Get count of new matches for the current user"""
    current_user = request.user
    
    # Get all matches where current user is either user1 or user2 and hasn't seen them
    new_matches_count = Match.objects.filter(
        Q(user1=current_user, user1_seen=False) | 
        Q(user2=current_user, user2_seen=False)
    ).count()
    
    return JsonResponse({'new_matches_count': new_matches_count})


@login_required
def mark_match_seen(request):
    """Mark a match as seen by the current user"""
    if request.method == 'POST':
        data = json.loads(request.body)
        match_id = data.get('match_id')
        
        try:
            match = Match.objects.get(id=match_id)
            match.mark_seen_by_user(request.user)
            
            return JsonResponse({'success': True})
        except Match.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Match not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def get_latest_match(request):
    """Get the latest unseen match for popup notification"""
    current_user = request.user
    
    # Get the most recent unseen match
    latest_match = Match.objects.filter(
        Q(user1=current_user, user1_seen=False) | 
        Q(user2=current_user, user2_seen=False)
    ).order_by('-created_at').first()
    
    if latest_match:
        # Get the other user's profile
        other_user = latest_match.user2 if latest_match.user1 == current_user else latest_match.user1
        try:
            other_profile = Profile.objects.get(user=other_user)
            return JsonResponse({
                'success': True,
                'match_id': latest_match.id,
                'other_user': {
                    'username': other_user.username,
                    'name': other_profile.name,
                    'profile_photo': other_profile.profile_photo.url if other_profile.profile_photo else None,
                    'age': other_profile.age
                }
            })
        except Profile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Profile not found'})
    
    return JsonResponse({'success': False, 'error': 'No new matches'})


@login_required
def get_profile_popup(request, profile_id):
    """Get profile details for popup display"""
    try:
        profile = Profile.objects.get(id=profile_id)
        
        # Check if current user has interacted with this profile
        current_user = request.user
        has_liked = Like.objects.filter(liker=current_user, liked=profile.user).exists()
        has_passed = Pass.objects.filter(passer=current_user, passed=profile.user).exists()
        
        # Check if there's a mutual match
        is_match = Match.objects.filter(
            Q(user1=current_user, user2=profile.user) | 
            Q(user1=profile.user, user2=current_user)
        ).exists()
        
        profile_data = {
            'id': profile.id,
            'name': profile.name,
            'age': profile.age,
            'location': profile.location,
            'height': profile.height,
            'bio': profile.bio,
            'interests': profile.interests,
            'profile_photo': profile.profile_photo.url if profile.profile_photo else None,
            'audio_bio': profile.audio_bio.url if profile.audio_bio else None,
            'has_liked': has_liked,
            'has_passed': has_passed,
            'is_match': is_match,
            'gender': profile.get_gender_display()
        }
        
        return JsonResponse({
            'success': True,
            'profile': profile_data
        })
        
    except Profile.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Profile not found'})
