from django.db import models
from django.contrib.auth.models import User
from tracks.models import Track

# Model to represent items added to a user's cart
class CartItem(models.Model):
    # Link to the user who owns this cart item
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    
    # The track this cart item refers to
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    
    # Quantity of the track in the cart (default 1)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        # Prevent duplicate entries of the same track per user
        unique_together = ('user', 'track')

    def __str__(self):
        # Friendly string representation (e.g., "billy - Oceania")
        return f"{self.user.username} - {self.track.title}"

# Model to represent a successful track purchase by a user
class Purchase(models.Model):
    # The user who bought the track
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    
    # The track being purchased
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
