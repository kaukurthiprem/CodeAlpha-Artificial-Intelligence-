import cv2
import torch
import numpy as np

# Load YOLOv5 model from PyTorch Hub
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Start video capture from webcam (0 = default)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Could not open webcam.")
    exit()

print("✅ Webcam opened. Press Q to exit.")

track_id = 0
trackers = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLOv5 inference
    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()

    new_trackers = []

    for *box, conf, cls in detections:
        x1, y1, x2, y2 = map(int, box)
        label = f"{model.names[int(cls)]} {conf:.2f}"
        color = (0, 255, 0)

        # Assign ID manually (for simple version)
        new_trackers.append(((x1, y1, x2, y2), track_id))
        track_id += 1

        # Draw box and label
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"ID {track_id-1}: {label}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    trackers = new_trackers  # very simple — no actual matching logic

    # Show the frame
    cv2.imshow("Webcam Object Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
