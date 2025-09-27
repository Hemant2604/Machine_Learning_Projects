import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load the trained model for emotion recognition
emotion_model = load_model('emotion_model.h5')

# Load the Haar Cascade for face detection
# Ensure the XML file is in the same directory or provide the full path
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Define the dictionary mapping emotion indices to labels
# NOTE: Make sure the order matches the training labels!
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break # Break the loop if there's an issue with the camera feed

    # Flip the frame horizontally (for a mirror-like view)
    frame = cv2.flip(frame, 1)

    # Convert the frame to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    # detectMultiScale(image, scaleFactor, minNeighbors)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

    # Process each face found in the frame
    for (x, y, w, h) in faces:
        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Crop the face region from the grayscale frame
        roi_gray = gray_frame[y:y + h, x:x + w]
        
        # Preprocess the cropped face for the model
        # 1. Resize to the model's expected input size (48x48)
        cropped_img = cv2.resize(roi_gray, (48, 48))
        # 2. Convert to a 4D tensor: (1, 48, 48, 1)
        #    - 1: A single image (batch size of 1)
        #    - 48, 48: Image dimensions
        #    - 1: Grayscale channel
        roi_processed = np.expand_dims(np.expand_dims(cropped_img, -1), 0)

        # Predict the emotion
        emotion_prediction = emotion_model.predict(roi_processed)
        
        # Find the emotion with the highest probability
        max_index = int(np.argmax(emotion_prediction))
        predicted_emotion = emotion_dict[max_index]

        # Put the predicted emotion label on the frame
        cv2.putText(frame, predicted_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    # Display the final frame with detections and predictions
    cv2.imshow('Real-Time Emotion Recognition', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()