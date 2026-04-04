from django.contrib import admin
from .models import Pothole

@admin.register(Pothole)
class PotholeAdmin(admin.ModelAdmin):
    list_display = ('latitude', 'longitude', 'confidence', 'detected_at')