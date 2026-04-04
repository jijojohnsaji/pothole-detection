from django.core.mail import send_mail
from django.conf import settings


def send_pothole_email(latitude, longitude, confidence):
    subject = "Pothole Detected Alert"

    message = f"""
A pothole has been detected by the Pothole Detection System.

Location Details:
Latitude: {latitude}
Longitude: {longitude}
Confidence: {confidence:.2f}

Please inspect and take necessary action.

Google Maps Link:
https://www.google.com/maps?q={latitude},{longitude}

Regards,
Automated Pothole Detection System
"""

    recipient_list = [
        "enteramail@gmail.com",
        "enteramail@gmail.com",
    ]

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )