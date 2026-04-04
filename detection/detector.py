from ultralytics import YOLO
import cv2
import torch
import time
import os
from django.conf import settings
from detection.state import set_trigger  # ⭐ NEW

# Global model variable
model = None

def load_model():
    """
    Load YOLO model once and reuse for performance.
    """
    global model
    if model is None:
        print("🚀 Loading YOLO model...")

        model_path = os.path.join(
            settings.BASE_DIR,
            "detection",
            "yolov8_models",
            "modell_20.pt"   # keep exact filename
        )

        if not os.path.exists(model_path):
            print(f"❌ Model not found: {model_path}")
            return None

        model = YOLO(model_path)

        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        print(f"🧠 Model running on: {device}")

    return model


def gen_frames():
    """
    Stream webcam frames with YOLO pothole detection.
    """
    print("📷 Opening Webcam...")

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("⚠️ Trying camera index 1...")
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("❌ Camera not accessible")
        return

    print("✅ Camera started successfully!")

    model_instance = load_model()

    last_detection_time = 0
    cooldown = 5  # seconds between GPS triggers
    prev_time = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        annotated = frame.copy()

        if model_instance is not None:
            try:
                results = model_instance(frame, conf=0.70)

                if results and len(results[0].boxes) > 0:
                    for box in results[0].boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        conf = float(box.conf[0])
                        cls = int(box.cls[0])
                        label = model_instance.names[cls]

                        # Draw bounding box
                        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 0, 255), 2)

                        text = f"{label} {conf:.2f}"

                        (w, h), _ = cv2.getTextSize(
                            text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
                        )

                        cv2.rectangle(
                            annotated,
                            (x1, y1 - h - 10),
                            (x1 + w, y1),
                            (0, 0, 255),
                            -1
                        )

                        cv2.putText(
                            annotated,
                            text,
                            (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (255, 255, 255),
                            2
                        )

                    # ⭐ Trigger GPS capture ONLY when pothole detected
                    curr_time = time.time()
                    if curr_time - last_detection_time > cooldown:
                        last_detection_time = curr_time
                        confidence = float(results[0].boxes.conf[0])
                        print(f"⚠️ Pothole Detected: {confidence:.2f}")

                        # 🔥 notify frontend
                        set_trigger(confidence)

            except Exception as e:
                print("Detection error:", e)

        # FPS Counter
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time else 0
        prev_time = curr_time

        cv2.putText(
            annotated,
            f"FPS: {int(fps)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # Stream frame
        ret, buffer = cv2.imencode('.jpg', annotated)
        frame_bytes = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame_bytes +
            b'\r\n'
        )

        time.sleep(0.03)

    cap.release()
    print("🛑 Camera stream stopped")