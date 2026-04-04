import json
from datetime import timedelta

from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Pothole
from .detector import gen_frames
from .state import pop_trigger
from .email_utils import send_pothole_email


# ===============================
# Dashboard page (camera + map)
# ===============================
@login_required
def dashboard(request):
    return render(request, "detection/dashboard.html")


# ===============================
# Full map page (all potholes)
# ===============================
@login_required
def map_view(request):
    return render(request, "detection/map.html")


# ===============================
# Route map page (start journey)
# ===============================
@login_required
def route_map(request):
    """
    User selects start + destination, route will be shown,
    and potholes from DB are also displayed on map.
    """
    return render(request, "detection/route_map.html")


# ===============================
# Live webcam stream
# ===============================
@login_required
def video_feed(request):
    return StreamingHttpResponse(
        gen_frames(),
        content_type="multipart/x-mixed-replace; boundary=frame"
    )


# ===============================
# Return potholes for map markers
# ===============================
@login_required
def get_potholes(request):
    potholes = list(
        Pothole.objects.values(
            "id", "latitude", "longitude", "confidence", "detected_at"
        )
    )
    return JsonResponse(potholes, safe=False)


# ===============================
# Trigger GPS ONLY when pothole detected
# ===============================
@login_required
def trigger_location(request):
    """
    Frontend polls this endpoint.
    It returns capture_location ONLY when detector triggers.
    """
    triggered, conf = pop_trigger()

    if triggered:
        return JsonResponse({
            "status": "capture_location",
            "confidence": conf
        })

    return JsonResponse({"status": "idle"})


# ===============================
# Save pothole GPS location
# ===============================
@csrf_exempt
@login_required
def save_location(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            lat = data.get("latitude")
            lng = data.get("longitude")
            confidence = float(data.get("confidence", 0))

            if lat is None or lng is None:
                return JsonResponse({"status": "invalid data"}, status=400)

            lat = float(lat)
            lng = float(lng)

            # Avoid duplicate potholes in the same nearby location within 10 minutes
            recent_pothole = Pothole.objects.filter(
                latitude__range=(lat - 0.0001, lat + 0.0001),
                longitude__range=(lng - 0.0001, lng + 0.0001),
                detected_at__gte=timezone.now() - timedelta(minutes=10)
            ).first()

            if recent_pothole:
                pothole = recent_pothole
                created = False
                print(f"⚠️ Duplicate pothole skipped -> {lat}, {lng}")
            else:
                pothole = Pothole.objects.create(
                    latitude=lat,
                    longitude=lng,
                    confidence=confidence
                )
                created = True
                print(f"✅ Saved Pothole -> {lat}, {lng}, Conf: {confidence}")

                # Send automatic email only for newly created potholes
                try:
                    send_pothole_email(
                        pothole.latitude,
                        pothole.longitude,
                        pothole.confidence
                    )
                    print("📧 Pothole alert email sent successfully")
                except Exception as mail_error:
                    print("❌ Email sending failed:", str(mail_error))

            return JsonResponse({
                "status": "saved",
                "created": created,
                "pothole": {
                    "id": pothole.id,
                    "latitude": pothole.latitude,
                    "longitude": pothole.longitude,
                    "confidence": pothole.confidence
                }
            })

        except Exception as e:
            print("Save Location Error:", str(e))
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "failed"}, status=400)