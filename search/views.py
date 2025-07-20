from django.shortcuts import render
from django.db.models import Q
from tracks.models import Track

# Search functionality
def search_view(request):
    # Get the 'q' query parameter from the URL (e.g., ?q=sofia)
    query = request.GET.get('q', '').strip()

    # Initialize empty result and recommendations
    results = []
    recommendations = []

    if query:
        # Search with title, artist username, and genre fields
        results = Track.objects.filter(
            Q(title__icontains=query) |  # If query matches title                  
            Q(artist__username__icontains=query) |  # If query matches artist username        
            Q(genre__icontains=query)         # If query matches genre               
        )
    else:
        # If no search term is provided, show 5 newest tracks as recommendations
        recommendations = Track.objects.order_by('-created_at')[:5]

    # Build context dictionary for the template
    context = {
        'query': query,                 # The original search term
        'results': results,            # List of matching tracks
        'recommendations': recommendations,  # Recent tracks if no search query
    }

    return render(request, 'search/search_results.html', context)
