from django.db import models
from django.contrib.auth.models import User

class Track(models.Model):
    GENRE_CHOICES = [
        ('hiphop', 'Hip-Hop'),
        ('rock', 'Rock'),
        ('pop', 'Pop'),
        ('jazz', 'Jazz'),
        ('classical', 'Classical'),
        ('edm', 'EDM'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='other')
    audio_file = models.FileField(upload_to='tracks/audio/', blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='tracks/images/', blank=True, null=True)

    def __str__(self):
        return self.title
