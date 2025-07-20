from django.urls import path
from . import views

app_name = 'tracks'

urlpatterns = [
    path('', views.track_list, name='tracks'),  # Tracks home
    path('<int:track_id>/', views.track_details, name='track_details'),

    path('seller/upload/', views.upload_track, name='upload_track'),
    path('seller/edit/<int:track_id>/', views.edit_track, name='edit_track'),
    path('seller/delete/<int:track_id>/', views.delete_track, name='delete_track'),
]
