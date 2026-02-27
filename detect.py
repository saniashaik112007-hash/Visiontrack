import cv2
from ultralytics import YOLO
import os

model = YOLO("yolov8n.pt")

def detect_objects(video_path):

    cap = cv2.VideoCapture(video_path)

    violation_detected = False
    violation_type = None
    saved_image_path = None

    frame_count = 0
    os.makedirs("static/results", exist_ok=True)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % 10 != 0:
            continue

        results = model(frame)

        persons = 0
        motorcycles = 0
        cars = 0

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                if cls == 0:
                    persons += 1
                elif cls == 3:
                    motorcycles += 1
                elif cls == 2:
                    cars += 1

        if motorcycles > 0 and persons > 0:
            violation_detected = True
            violation_type = "No Helmet"

        elif cars > 0:
            violation_detected = True
            violation_type = "No Seatbelt"

        if violation_detected:
            saved_image_path = f"static/results/frame_{frame_count}.jpg"
            cv2.imwrite(saved_image_path, frame)
            cap.release()
            return violation_detected, violation_type, saved_image_path

    cap.release()
    return False, None, None