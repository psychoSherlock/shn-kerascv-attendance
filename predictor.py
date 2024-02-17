from time import sleep
import numpy as np
from keras.models import load_model
import cv2
import numpy as np
import os

# Load the model
# Load the cascade for face detection
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

model = load_model("data/keras_model.h5", compile=False)

# Load the labels
class_names = open("data/labels.txt", "r").readlines()


def predictStudent():
    # Read the image

    image = cv2.imread("data/capturedImage.png")

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Make the image a numpy array and reshape it to the model's input shape.
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predict the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    identifiedUser = class_name[2:]
    confidence_num = str(np.round(confidence_score * 100))[:-2]
    # Print prediction and confidence score
    confidence_percent = f'{confidence_num}%'
    return identifiedUser, confidence_percent


# Function to check if file has changed
def check_file_change():
    # Get the last modified time of the file
    last_modified_time = os.path.getmtime("data/capturedImage.png")

    # Check if the last modified time is different from the stored time
    if last_modified_time != check_file_change.last_modified_time:
        # Remove the contents of identifiedPerson.txt
        with open("./data/identifiedPerson.txt", "w") as file:
            file.write("")

        # Get the data from predictStudent()
        identified_user, confidence_percent = predictStudent()

        # Write the data to identifiedPerson.txt
        with open("./data/identifiedPerson.txt", "w") as file:
            file.write('1\n')
            file.write(f"{identified_user}")
            file.write(f"{confidence_percent}")

        # Update the stored last modified time
        check_file_change.last_modified_time = last_modified_time


# Initialize the last modified time
check_file_change.last_modified_time = os.path.getmtime(
    "data/capturedImage.png")

while True:
    check_file_change()
    sleep(1)
