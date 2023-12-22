import cv2
from deepface import DeepFace
import tempfile
import os

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open a video capture object (0 corresponds to the default camera)
cap = cv2.VideoCapture(0)

prev_emotion = "Neutral"  # Initialize with a neutral emotion

while True:
    # Read a frame from the video capture
    ret, frame = cap.read()

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces and perform emotion detection
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Extract the face region
        face_roi = gray[y:y + h, x:x + w]

        # Save the face region as a temporary image file
        temp_file_path = os.path.join(tempfile.gettempdir(), "temp_face_image.jpg")
        cv2.imwrite(temp_file_path, face_roi)

        # Perform emotion detection using the saved image file
        emotion_predictions = DeepFace.analyze(temp_file_path, actions=['emotion'], enforce_detection=False)

        # Check if a face was detected before accessing the results
        if 'emotion' in emotion_predictions:
            current_emotion = emotion_predictions['emotion']['dominant']
        else:
            current_emotion = "Unknown"

        # Check if the emotion has changed significantly
        if current_emotion != "Unknown" and current_emotion != prev_emotion:
            prev_emotion = current_emotion

        # Display the emotion text
        cv2.putText(frame, f'Emotion: {prev_emotion}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('Face Tracker', frame)

    # Break the loop when 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the video capture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
