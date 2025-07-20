from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import UserForm, UserProfileForm
from .forms import TailwindAuthenticationForm, TailwindUserCreationForm
from django.shortcuts import redirect, get_object_or_404
from .models import Track, Wishlist
from django.views.decorators.http import require_POST


def register_view(request):
    if request.method == 'POST':
        form = TailwindUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Role setting 
            is_seller = form.cleaned_data.get('is_seller', False)
            role = 'seller' if is_seller else 'user'
            UserProfile.objects.create(user=user, role=role)
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TailwindUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = TailwindAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = TailwindAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')


@login_required
def profile_view(request):
    user = request.user
    profile = user.profile  # via related_name on OneToOneField
    return render(request, 'accounts/profile.html', {'user': user, 'profile': profile})


@login_required
def profile_edit_view(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

# Dashboard view that adapts to the user role (user, seller, or admin)
@login_required
def dashboard_view(request):
    user = request.user
    profile = user.profile  # Access the extended profile via OneToOneField

    # If the user is a seller, show their uploaded tracks
    tracks = Track.objects.filter(artist=user) if profile.role == 'seller' else None

    # Get purchased tracks if the user has made any purchases
    purchased_tracks = [purchase.track for purchase in user.purchases.select_related('track')] if hasattr(user, 'purchases') else []

    # Get tracks added to the user's wishlist
    wishlist_tracks = [w.track for w in user.wishlist.select_related('track')] if hasattr(user, 'wishlist') else []

    # If the user is an admin, load all other user profiles for management
    users = UserProfile.objects.select_related('user').all() if profile.role == 'admin' else None

    # Render the dashboard with all context variables appropriate to the user role
    return render(request, 'accounts/dashboard.html', {
        'profile': profile,
        'user': user,
        'tracks': tracks,
        'purchased_tracks': purchased_tracks,
        'wishlist_tracks': wishlist_tracks,
        'user_profiles': users,  # For admin
    })

# View to allow an admin to change another user's role (POST-only for security)
# https://stackoverflow.com/questions/74981938/usage-of-require-post-in-django
@require_POST
@login_required
def change_user_role(request, user_id):
    # Only admins can access this functionality
    if request.user.profile.role != 'admin':
        messages.error(request, "Permission denied.")
        return redirect('dashboard')

    # Get the profile of the target user by user ID
    target_profile = get_object_or_404(UserProfile, user__id=user_id)
    new_role = request.POST.get('role')  # Get the new role from the form

    # If the role is valid, update it
    if new_role in dict(UserProfile.ROLE_CHOICES).keys():
        target_profile.role = new_role
        target_profile.save()
        messages.success(request, f"{target_profile.user.username}'s role updated to {new_role}.")
    else:
        messages.error(request, "Invalid role.")

    return redirect('dashboard')

# Add a track to the current user's wishlist
@login_required
def add_to_wishlist(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    Wishlist.objects.get_or_create(user=request.user, track=track)  # Avoid duplicates
    messages.success(request, "Added to your wishlist!")
    # Redirect back to the referring page or fallback to tracks list
    return redirect(request.META.get('HTTP_REFERER', 'tracks:tracks'))

# Remove a track from the current user's wishlist
@login_required
def remove_from_wishlist(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    Wishlist.objects.filter(user=request.user, track=track).delete()
    messages.info(request, "Removed from your wishlist.")
    # Redirect back to the page the user came from
    return redirect(request.META.get('HTTP_REFERER', 'tracks:tracks'))
