import cv2
import serial
import time

# Load pre-trained face recognition model
faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
faceRecognizer.read("models/trained_lbph_face_recognizer_model.yml")

# Load Haarcascade for face detection
faceCascade = cv2.CascadeClassifier("models/haarcascade_frontalface_default.xml")

fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.6
fontColor = (255, 255, 255)
fontWeight = 2
fontBottomMargin = 30

nametagColor = (255, 0, 0)
nametagHeight = 50

faceRectangleBorderColor = nametagColor
faceRectangleBorderSize = 2

# Open a connection to the Arduino
ser = serial.Serial('COM3', 9600)  # Change port to your Arduino's port
time.sleep(2)  # Allow time for Arduino to initialize

# Define VIP IDs
vip_ids = [5, 6]  # Modify with the IDs of VIP individuals

# Open a connection to the first webcam
camera = cv2.VideoCapture(0)

# Start looping
while True:
    # Capture frame-by-frame
    ret, frame = camera.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Control flag for LED
    is_access_granted = False

    # For each face found
    for (x, y, w, h) in faces:

        # Recognize the face
        ID, Confidence = faceRecognizer.predict(gray[y:y + h, x:x + w])
        # Confidence normalization to a 0-100 scale
        Confidence = 100 - Confidence

        # Determine person's name based on ID
        if ID in vip_ids:
            Person = "VIP"
        else:
            Person = "Regular"

        if Confidence > 50:
            # Send data to Arduino
            if ID in vip_ids:
                ser.write(b'2')  # Sending '2' to Arduino for VIP
            else:
                ser.write(b'1')  # Sending '1' to Arduino for regular

            is_access_granted = True

        # Create rectangle around the face
        cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), faceRectangleBorderColor, faceRectangleBorderSize)

        # Display name tag
        cv2.rectangle(frame, (x - 22, y - nametagHeight), (x + w + 22, y - 22), nametagColor, -1)
        cv2.putText(frame, str(Person) + ": " + str(round(Confidence, 2)) + "%", (x, y-fontBottomMargin), fontFace, fontScale, fontColor, fontWeight)

    # Control
    if is_access_granted:
        ser.write(b'1')  # Sending '1' to Arduino to turn on LED
    else:
        ser.write(b'0')  # Sending '0' to Arduino to turn off LED

    # Display the resulting frame
    cv2.imshow('Detecting Faces...', frame)

    # Exit loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera
camera.release()

# Close the serial connection to the Arduino
ser.write(b'0')  # Sending '0' to Arduino to turn off LED
ser.close()

# Close all OpenCV windows
cv2.destroyAllWindows()
