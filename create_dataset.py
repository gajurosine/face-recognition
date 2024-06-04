import cv2
import time

# Function to capture face images and save them to the dataset folder
def capture_face_images(ID, images_to_capture=30):
    # Initialize the camera
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    # Initialize Haarcascade for face detection
    face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')

    # Initialize variables for image counting
    image_count = 0

    # Start looping
    while True:
        ret, image = camera.read()
        if not ret:
            break

        # Convert frame to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        # Loop through detected faces
        for (x, y, w, h) in faces:
            # Draw rectangle around the face
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Check if image count reaches the desired number
            if image_count >= images_to_capture:
                break

            # Save the captured face image
            cv2.imwrite(f"dataset/data.{ID}.{int(time.time() * 1000)}.jpg", gray[y:y + h, x:x + w])
            image_count += 1

        # Display the video frame with rectangle
        cv2.imshow("Dataset Generating...", image)

        # To stop taking video, press 'q' key or if image count reaches the desired number
        if cv2.waitKey(1) & 0xFF == ord('q') or image_count >= images_to_capture:
            break

    # Release the camera and close all windows
    camera.release()
    cv2.destroyAllWindows()

# Prompt user for ID
ID = input('Enter your ID: ')

# Inform user about the data collection process
print("Please get your face ready!")

# Wait for 2 seconds to allow user to position themselves
time.sleep(2)

# Capture face images and save them to the dataset folder
capture_face_images(ID)
