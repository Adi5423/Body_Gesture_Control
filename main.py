# Import necessary libraries
import mediapipe as mp
import cv2
import pyautogui
import math
import screeninfo

# Set up drawing utility
mp_drawing = mp.solutions.drawing_utils

# Initialize MediaPipe components
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands  # Add this line to import the mp_hands module

# Load holistic model
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize hand tracking model
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing.DrawingSpec((0,0,255) , thickness = 1 , circle_radius =2)
mp_drawing.draw_landmarks

# Get webcam feed
cap = cv2.VideoCapture(0)
with mp_holistic.Holistic(min_detection_confidence=0.5 , min_tracking_confidence=0.5 ) as holistic:

    # Get screen width and height
    screen_width, screen_height = pyautogui.size()
    while cap.isOpened():
        # Read feed
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        
        # Recolor image from BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process image with holistic model
        results = holistic.process(image)
        
        # Get frame height and width
        frame_height, frame_width, _ = frame.shape

        # Scale the frame to fit the screen
        scale_factor = min(screen_width / frame_width, screen_height / frame_height)
        frame = cv2.resize(frame, (int(frame_width * scale_factor), int(frame_height * scale_factor)))

        

        # Draw face landmarks
        mp_drawing.draw_landmarks(
            image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
            mp_drawing.DrawingSpec(color=(80,110,10), thickness = 1, circle_radius=1),
            mp_drawing.DrawingSpec(color=(80,256,121), thickness = 1, circle_radius=1),
            )

        # Draw pose landmarks
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(121,22,76), thickness = 2, circle_radius=4),
            mp_drawing.DrawingSpec(color=(121,44,250), thickness =2, circle_radius=2),
            )

        # Draw left hand landmarks
        mp_drawing.draw_landmarks(
            image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(121,20+2,10+66), thickness = 2, circle_radius=4),
            mp_drawing.DrawingSpec(color=(121,44,250), thickness =2, circle_radius=2),
            )

        # Draw right hand landmarks
        mp_drawing.draw_landmarks(
            image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(80,20,10), thickness = 2, circle_radius=4),
            mp_drawing.DrawingSpec(color=(80,44,121), thickness =2, circle_radius=2),
            )

            
        # if results.multi_hand_landmarks:
        #     for hand_landmarks in results.multi_hand_landmarks:
        #         # Get the landmarks for the index fingers and thumbs.
        #         index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        #         thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

        #         # Check if the index finger and thumb are close enough to form a "Namaste" shape.
        #         if index_finger_tip.y > thumb_tip.y and abs(index_finger_tip.x - thumb_tip.x) < 0.1:
        #             cv2.putText(frame, "Namaste!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Recolor image from RGB to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Display feed
        cv2.imshow('Raw Webcam Feed', image)

        # Exit loop when 'q' key is pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()