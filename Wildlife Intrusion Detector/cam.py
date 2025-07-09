import cv2

url = 'http://192.168.137.228:8080/video'  # Update this IP if needed
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print(" Failed to connect to the stream. Check IP, Wi-Fi, and if app is running.")
else:
    print(" Stream connected!")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Mobile Camera Stream", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
