from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from tracks.models import Track
from .models import CartItem, Purchase
from django.contrib import messages

# View to display all items in the current user's cart
@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)  # Get all cart items for this user
    return render(request, 'cart/cart.html', {'items': items})

# View to add a track to the cart
@login_required
def add_to_cart(request, track_id):
    # Get the track matching the given ID
    track = get_object_or_404(Track, id=track_id)

    # Get or create a CartItem. If it already exists, increase quantity
    item, created = CartItem.objects.get_or_create(user=request.user, track=track)
    if not created:
        item.quantity += 1
        item.save()

    messages.success(request, f'"{track.title}" was added to your cart.')

    return redirect('cart:cart')

# View to update the quantity of a cart item
@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        if quantity < 1:
            item.delete()  # Remove item if quantity is less than 1
            messages.info(request, f'"{item.track.title}" was removed from your cart.')
        else:
            item.quantity = quantity
            item.save()
            messages.success(request, f'Updated quantity for "{item.track.title}".')

    return redirect('cart:cart')

# View to remove a cart item
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, f'"{item.track.title}" was removed from your cart.')
    return redirect('cart:cart')


@login_required
def checkout_view(request):
    items = request.user.cart_items.all() 
    # Calculate total value
    total = sum(item.track.price * item.quantity for item in items)
    return render(request, 'cart/checkout.html', {'items': items, 'total': total})

@login_required
def confirm_purchase(request):
    cart_items = request.user.cart_items.all()
    for item in cart_items:
        # Create a purchase record for each track and user
        Purchase.objects.get_or_create(buyer=request.user, track=item.track)
    # Clear cart after purchase    
    cart_items.delete()   
    messages.success(request, 'Track purchased!')
    return redirect('dashboard')
