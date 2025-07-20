from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

# Simple pages
def index(request):
    return render(request, 'frontend/index.html')

def about(request):
    return render(request, 'frontend/about.html')

def contact(request):
    return render(request, 'frontend/contact.html')

def studio(request):
    return render(request, 'frontend/studio/studio.html')

def tasks(request):
    return render(request, 'frontend/tasks/tasks.html')

def tracks(request):
    return render(request, 'frontend/tracks.html')

def search(request):
    return render(request, 'frontend/search.html')

def cart(request):
    return render(request, 'frontend/cart.html')

# Only for authenticated users
@login_required
def profile(request):
    return render(request, 'frontend/profile.html')

@login_required
def dashboard(request):
    return render(request, 'frontend/dashboard.html')
