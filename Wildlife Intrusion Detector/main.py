import cv2
from ultralytics import YOLO
import threading
from deterrence import sound, flash  # Import deterrent methods

# Load YOLOv8n model
model = YOLO("yolov8n.pt")

# List of wild animals to monitor
monitored_animals = ["elephant", "bear"]  # Add more as needed

# Flag to avoid repeated triggering
triggered = False

def run_deterrence():
    global triggered
    triggered = True
    sound.play_sound()
    flash.trigger_flash()
    triggered = False

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run object detection
    results = model(frame, conf=0.7)[0]

    detected = False

    for box in results.boxes:
        conf = float(box.conf[0])

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls = int(box.cls[0])
        label = model.names[cls]

        if label not in monitored_animals:
            continue

        # Draw bounding box and label (same color for all)
        color = (0, 0, 255)  # Red
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 4)
        cv2.putText(frame, f"{label.upper()} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)

        detected = True

    # Trigger deterrent if needed
    if detected and not triggered:
        threading.Thread(target=run_deterrence).start()

    # Show the frame
    cv2.imshow("Live Object Detection", frame)

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
