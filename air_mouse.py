import cv2
import mediapipe as mp
from pynput.mouse import Controller, Button
from math import sqrt
import time

# Initialize Mediapipe and Pynput
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils
mouse = Controller()

# Parameters
smoothing_factor = 1.0
scaling_factor = 1.0
click_threshold = 0.05
screen_width, screen_height = 1920, 1080

# Scroll control
last_scroll_time = 0
scroll_delay = 0.3  # seconds

# Initialize previous finger position
prev_x, prev_y = None, None

# Helper: Check if all fingers except thumb are folded (closed)
def is_hand_closed(hand_landmarks):
    folded = 0
    for tip in [8, 12, 16, 20]:
        pip = tip - 2
        if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y:
            folded += 1
    return folded == 4

# Helper: Check if all fingers except thumb are extended (open)
def is_hand_open(hand_landmarks):
    extended = 0
    for tip in [8, 12, 16, 20]:
        pip = tip - 2
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            extended += 1
    return extended == 4

# Start video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame horizontally for mirror view
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get index tip and thumb tip landmarks
            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]

            # Get normalized coordinates (0 to 1)
            curr_x_norm = index_tip.x
            curr_y_norm = index_tip.y

            # Detect relative movement and apply it to mouse
            if prev_x is not None and prev_y is not None:
                dx = (curr_x_norm - prev_x) * screen_width * scaling_factor
                dy = (curr_y_norm - prev_y) * screen_height * scaling_factor

                # Get current mouse position
                curr_mouse_x, curr_mouse_y = mouse.position

                # Apply smoothed delta movement
                new_mouse_x = int(curr_mouse_x + dx * smoothing_factor)
                new_mouse_y = int(curr_mouse_y + dy * smoothing_factor)

                # Keep mouse within screen bounds
                new_mouse_x = max(0, min(new_mouse_x, screen_width - 1))
                new_mouse_y = max(0, min(new_mouse_y, screen_height - 1))

                # Move the mouse
                mouse.position = (new_mouse_x, new_mouse_y)

                # Print mouse movement
                print(f"Moved mouse to: ({new_mouse_x}, {new_mouse_y})")

            # Update previous index finger position
            prev_x, prev_y = curr_x_norm, curr_y_norm

            # Detect pinch (thumb and index close = click)
            distance = sqrt((index_tip.x - thumb_tip.x) ** 2 + (index_tip.y - thumb_tip.y) ** 2)
            if distance < click_threshold:
                mouse.click(Button.left)
                print("Mouse clicked")

            # Scroll detection
            current_time = time.time()
            if is_hand_closed(hand_landmarks):
                if current_time - last_scroll_time > scroll_delay:
                    mouse.scroll(0, -2)  # Scroll down
                    last_scroll_time = current_time
                    print("Scrolling down")
            elif is_hand_open(hand_landmarks):
                if current_time - last_scroll_time > scroll_delay:
                    mouse.scroll(0, 2)   # Scroll up
                    last_scroll_time = current_time
                    print("Scrolling up")

    # Display frame
    cv2.imshow('Air Mouse with Scroll', frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
