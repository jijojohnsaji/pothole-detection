from django.urls import path
from django.shortcuts import redirect
from . import views


# Redirect /detection/ → dashboard
def detection_home(request):
    return redirect('dashboard')


urlpatterns = [

    # ======================
    # Home redirect
    # ======================
    path('', detection_home, name='detection_home'),

    # ======================
    # Pages
    # ======================
    path('dashboard/', views.dashboard, name='dashboard'),
    path('map/', views.map_view, name='map'),

    # ⭐ NEW → Journey page after login
    path('route-map/', views.route_map, name='route_map'),

    # ======================
    # Live webcam stream
    # ======================
    path('video-feed/', views.video_feed, name='video_feed'),

    # ======================
    # API endpoints
    # ======================
    path('get-potholes/', views.get_potholes, name='get_potholes'),
    path('save-location/', views.save_location, name='save_location'),
    path('trigger-location/', views.trigger_location, name='trigger_location'),
]