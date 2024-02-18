import cv2
import os
import random
import string

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

# Ask the user for their name
name = input("Enter your name: ")

# Create the dataset folder if it doesn't exist
dataset_folder = f"./Dataset/{name}"
os.makedirs(dataset_folder, exist_ok=True)

# Initialize the face counter
face_counter = 0

# Start capturing video from the default camera
cap = cv2.VideoCapture(2)

while True:
    # Read the current frame
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw a green box around each detected face and save it
    for (x, y, w, h) in faces:
        # Increase the size of the face region by 10 pixels on each side
        x -= 10
        y -= 10
        w += 20
        h += 20

        # Crop the region covered by the box (excluding the green box)
        face = frame[y:y + h, x:x + w]

        # Generate a random string for the image filename
        random_string = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=10))

        # Save the face image without the green box
        try:
            cv2.imwrite(f"{dataset_folder}/{name}_{random_string}.png", face)
        except:
            continue
        # Increment the face counter
        face_counter += 1

        # Break the loop if 100 photos have been captured
        # if face_counter == 100:
        #     break

    # Display the face counter on the video window
    cv2.putText(frame, f"Faces saved: {face_counter}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow("Face Recognition", frame)

    # Break the loop if 'q' is pressed or 100 photos have been captured
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()
