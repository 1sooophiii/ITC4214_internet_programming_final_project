from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/<int:track_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/complete', views.confirm_purchase, name='confirm_purchase'),
]
