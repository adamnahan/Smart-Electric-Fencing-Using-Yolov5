from flask import Flask, render_template, Response, request
import cv2
from ultralytics import YOLO
import threading
from deterrence import sound, flash

app = Flask(__name__)

# Load YOLOv8n model
model = YOLO("yolov8n.pt")

# List of wild animals to monitor
monitored_animals = ["elephant", "bear"]  # Add more as needed

# Initialize webcam
cap = cv2.VideoCapture(0)

# Flag to avoid repeated triggering
triggered = False

def run_deterrence():
    global triggered
    triggered = True
    print("WILD ANIMAL DETECTED! Triggering deterrence...")
    sound.play_sound()
    flash.trigger_flash()
    print("Deterrence complete.")
    # Reset after a delay to allow re-triggering
    threading.Timer(5.0, lambda: globals().update(triggered=False)).start()

def generate_frames():
    global triggered
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Run object detection on the frame
            results = model(frame, conf=0.7)[0]
            
            detected = False
            
            # Process detection results
            for box in results.boxes:
                if box is None:
                    continue
                    
                conf = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                label = model.names[cls]

                # Check if detected animal is in our monitored list
                if label in monitored_animals:
                    print(f"Detected: {label} with confidence {conf:.2f}")
                    
                    # Draw bounding box and label
                    color = (0, 0, 255)  # Red for wild animals
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                    cv2.putText(frame, f"{label.upper()} {conf:.2f}", 
                              (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                              0.9, color, 2)
                    
                    detected = True
                else:
                    # Draw other detections in green (optional)
                    color = (0, 255, 0)  # Green for other animals
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f"{label} {conf:.2f}", 
                              (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                              0.7, color, 2)
            
            # Trigger deterrent if wild animal detected and not already triggered
            if detected and not triggered:
                print("Starting deterrence thread...")
                threading.Thread(target=run_deterrence).start()
            
            # Add status text to frame
            status_text = "ALERT: WILD ANIMAL DETECTED!" if detected else "Monitoring..."
            status_color = (0, 0, 255) if detected else (0, 255, 0)
            cv2.putText(frame, status_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
            
            # Encode frame
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/trigger_sound', methods=['POST'])
def trigger_sound():
    print("Manual sound trigger activated")
    sound.play_sound()
    return ('', 204)

@app.route('/trigger_flash', methods=['POST'])
def trigger_flash():
    print("Manual flash trigger activated")
    flash.trigger_flash()
    return ('', 204)

@app.route('/status')
def get_status():
    """API endpoint to get current detection status"""
    return {
        'monitoring': True,
        'triggered': triggered,
        'monitored_animals': monitored_animals
    }

if __name__ == '__main__':
    print("Starting Wildlife Detection Web App...")
    print(f"Monitoring for: {monitored_animals}")
    app.run(debug=True, threaded=True)