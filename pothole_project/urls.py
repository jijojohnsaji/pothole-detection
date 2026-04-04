"""
URL configuration for pothole_project project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


# Redirect root URL to login page
def home_redirect(request):
    return redirect('/users/login/')


urlpatterns = [
    path('', home_redirect, name='home'),          # http://127.0.0.1:8000/
    path('admin/', admin.site.urls),               # Admin panel
    path('users/', include('users.urls')),         # Login / Register
    path('detection/', include('detection.urls')), # Dashboard, Map, Detection APIs
]