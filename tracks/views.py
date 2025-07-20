from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Track
from .forms import TrackForm
from django.contrib import messages

# Displays all tracks, with filtering by genre, artist username, and price range
def track_list(request):
    # Retrieve filter values from URL query parameters
    genre = request.GET.get('genre', '')
    artist = request.GET.get('artist', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    # Apply filters
    tracks = Track.objects.all()
    if genre:
        tracks = tracks.filter(genre=genre)
    if artist:
        tracks = tracks.filter(artist__username__icontains=artist)
    if min_price:
        tracks = tracks.filter(price__gte=min_price)
    if max_price:
        tracks = tracks.filter(price__lte=max_price)

    # Pass choices to the template for filter dropdowns
    genres = Track.GENRE_CHOICES
    return render(request, 'tracks/tracks.html', {
        'tracks': tracks,
        'genres': genres,
        'selected_genre': genre,
        'selected_artist': artist,
        'min_price': min_price,
        'max_price': max_price,
    })

# Displays details for one track, or returns 404 if not found
def track_details(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    return render(request, 'tracks/track_details.html', {'track': track})

# Decorator: allows view access only for logged-in users with role "seller"
# source: https://dev.to/pymeister/how-to-create-decorators-in-django-2f8d
def seller_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Blocks access if user has no profile or isn't a seller
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'seller':
            # Django messaging system
            messages.error(request, "Only sellers can access this page.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Lets sellers upload a new track
@login_required
@seller_required
def upload_track(request):
    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES)
        if form.is_valid():
            track = form.save(commit=False)
            track.artist = request.user  # Ensure seller is the owner
            track.save()
            # Django messaging system
            messages.success(request, "Track uploaded!")
            return redirect('dashboard')
    else:
        form = TrackForm()
    return render(request, 'tracks/upload_track.html', {'form': form})

# Lets sellers edit a track they own
@login_required
@seller_required
def edit_track(request, track_id):
    # Ensures only the track owner (artist) can edit
    track = get_object_or_404(Track, id=track_id, artist=request.user)
    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES, instance=track)
        if form.is_valid():
            form.save()
            # Django messaging system
            messages.success(request, "Track updated!")
            return redirect('dashboard')
    else:
        form = TrackForm(instance=track)
    return render(request, 'tracks/edit_track.html', {'form': form, 'track': track})

# Lets sellers delete a track they own, with confirmation.
@login_required
@seller_required
def delete_track(request, track_id):
    # Ensures only the owner can delete their track.
    track = get_object_or_404(Track, id=track_id, artist=request.user)
    if request.method == 'POST':
        track.delete()
        # Django messaging system
        messages.success(request, "Track deleted!")
        return redirect('dashboard')
    return render(request, 'tracks/delete_track_confirm.html', {'track': track})
