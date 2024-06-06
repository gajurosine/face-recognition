import cv2
import time
import sqlite3
import os

def generate_uid():
    current_millis = int(time.time() * 1000)
    current_seconds = current_millis // 1000
    return current_seconds

# Initialize face cascade
face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')

# Connect to SQLite database
conn = sqlite3.connect('customer_faces_data.db')
c = conn.cursor()

# Create a table to store face data if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS customers
             (id INTEGER PRIMARY KEY AUTOINCREMENT, customer_uid TEXT, customer_name TEXT, image_path TEXT)''')

customer_name = input('Enter the Customer Name: ')
customer_uid = generate_uid()

print("Please get your face ready!")
time.sleep(2)

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

start_time = time.time()
interval = 500  # Capture an image every 500 milliseconds
current_time = start_time
image_count = 0  # Total number of images captured

while True:
    ret, image = camera.read()
    if not ret:
        print("Failed to capture frame from the camera")
        break

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    if len(faces) > 0:
        break

    cv2.putText(image, "No face detected. Please position yourself in front of the camera.", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.imshow("Waiting for Face Detection...", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("User quit the program.")
        break

if len(faces) > 0:
    print("Face detected. Proceeding to capture images.")

    while True:
        ret, image = camera.read()
        if not ret:
            print("Failed to capture frame from the camera")
            break

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, f"Generating image {image_count+1}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            if (time.time() - current_time) * 1000 >= interval and image_count < 10:
                image_name = f"data.{customer_uid}_{image_count+1}.jpg"
                image_path = os.path.join('dataset', image_name)
                
                if not os.path.exists('dataset'):
                    os.makedirs('dataset')

                cv2.imwrite(image_path, gray[y:y + h, x:x + w])
                current_time = time.time()
                image_count += 1

                c.execute("INSERT INTO customers (customer_uid, customer_name, image_path) VALUES (?, ?, ?)", (customer_uid, customer_name, image_path))
                conn.commit()

        cv2.imshow("Dataset Generating...", image)

        if cv2.waitKey(1) & 0xFF == ord('q') or image_count >= 50:
            break

camera.release()
cv2.destroyAllWindows()
conn.close()
