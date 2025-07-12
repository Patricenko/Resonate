from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
# Create your views here.
@login_required
def create_profile_view(request):
    print('activated')
    # If profile already exists, redirect to edit or view
    if hasattr(request.user, 'tinder_profile'):
        pass
        #return redirect('profile_detail')  # Replace with your actual view name

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            #return redirect('profile_detail')  # Replace with your actual view
    else:
        form = ProfileForm()

    return render(request, 'create_profile.html', {'form': form})


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
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})
