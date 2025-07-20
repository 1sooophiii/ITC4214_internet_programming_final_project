from django.db import models
from django.contrib.auth.models import User

from tracks.models import Track

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    ]

    # OneToOneField means each user has exactly one profile
    # One-to-one relationship with built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    full_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    music_background = models.CharField(max_length=255, blank=True)
    favorite_genres = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.user.username}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'track')