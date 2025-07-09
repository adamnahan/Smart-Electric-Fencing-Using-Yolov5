from flask import Flask, render_template, Response
import cv2
from ultralytics import YOLO
from deterrence.sound import play_sound
from deterrence.flash import trigger_flash

app = Flask(__name__)
model = YOLO("yolov8n.pt")
monitored_animals = ["elephant", "bear"]

cap = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame, conf=0.7)[0]
        for box in results.boxes:
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = model.names[cls]
            if label not in monitored_animals:
                continue
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            color = (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 4)
            cv2.putText(frame, f"{label.upper()} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)

        # Stream frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/deterrent/sound')
def trigger_sound():
    play_sound()
    return "Sound triggered"

@app.route('/deterrent/flash')
def trigger_flash_deter():
    trigger_flash()
    return "Flash triggered"

if __name__ == '__main__':
    app.run(debug=True)
