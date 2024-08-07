import cv2
import mediapipe as mp
from pynput.mouse import Controller,Button 
from math import sqrt

# Initialize Mediapipe and Pynput
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils
mouse = Controller()

# Parameters
smoothing_factor = 0.5  # Adjust this for smoothing
scaling_factor = 1.0    # Adjust this for scaling (start with 1.0)
click_threshold = 0.05  # Threshold for detecting click (distance between thumb and index finger)


# Initialize previous position
prev_x, prev_y = None, None

# Start video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Track the tip of the index finger (landmark 8) and thumb (landmark 4)
            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]
            h, w, _ = frame.shape
            x, y = int(index_tip.x * w), int(index_tip.y * h)
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)

            # Print debug information
            print(f"Finger Coordinates: x={x}, y={y}")
            print(f"Thumb Coordinates: thumb_x={thumb_x}, thumb_y={thumb_y}")

            # Smooth cursor movement
            if prev_x is None or prev_y is None:
                prev_x, prev_y = x, y
            else:
                # Smooth the movement
                x = int(prev_x * (1 - smoothing_factor) + x * smoothing_factor)
                y = int(prev_y * (1 - smoothing_factor) + y * smoothing_factor)

            # Scale cursor movement
            x = int(x * scaling_factor)
            y = int(y * scaling_factor)

            # Print debug information for scaled coordinates
            print(f"Scaled Coordinates: x={x}, y={y}")

            # Ensure cursor is within screen bounds
            screen_width, screen_height = 1920, 1080  # Example resolution
            x = max(0, min(x, screen_width - 1))
            y = max(0, min(y, screen_height - 1))

            # Move mouse
            mouse.position = (x, y)

            # Update previous position
            prev_x, prev_y = x, y

            # Check distance between index finger and thumb to determine click
            distance = sqrt((index_tip.x - thumb_tip.x) ** 2 + (index_tip.y - thumb_tip.y) ** 2)
            if distance < click_threshold:
                mouse.click(Button.left)  # Perform left click

    # Display the frame
    cv2.imshow('Air Mouse', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
