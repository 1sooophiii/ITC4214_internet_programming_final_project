from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin/change-role/<int:user_id>/', views.change_user_role, name='change_user_role'),
    path('wishlist/add/<int:track_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:track_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
