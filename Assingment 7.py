import cv2
import mediapipe as mp

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

# Finger tip landmarks
finger_tips = [8, 12, 16, 20]
thumb_tip = 4

# Webcam capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Draw center box (300x300)
    cx, cy = w // 2, h // 2
    box_size = 300
    top_left = (cx - box_size // 2, cy - box_size // 2)
    bottom_right = (cx + box_size // 2, cy + box_size // 2)
    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

    # Process image for hand detection
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    left_count = 0
    right_count = 0

    if result.multi_hand_landmarks and result.multi_handedness:
        for idx, (hand_landmarks, handedness) in enumerate(zip(result.multi_hand_landmarks, result.multi_handedness)):
            label = handedness.classification[0].label  # 'Left' or 'Right'
            landmarks = hand_landmarks.landmark

            # Convert to pixel coords
            x_list = [lm.x * w for lm in landmarks]
            y_list = [lm.y * h for lm in landmarks]

            # Draw landmarks if hand is in center box
            if all(top_left[0] < x < bottom_right[0] and top_left[1] < y < bottom_right[1]
                   for x, y in zip(x_list, y_list)):
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                count = 0

                # Other 4 fingers
                for tip in finger_tips:
                    if landmarks[tip].y < landmarks[tip - 2].y:
                        count += 1
                # Thumb check
                if label == "Right":
                    if landmarks[thumb_tip].x < landmarks[thumb_tip - 1].x:
                        count += 1
                else:  # Left
                    if landmarks[thumb_tip].x > landmarks[thumb_tip - 1].x:
                        count += 1

                

                # Assign to left or right count
                if label == "Right":
                    right_count = count
                else:
                    left_count = count

               

    total_count = left_count + right_count

    # Display count
    cv2.putText(frame, f'Left: {left_count}', (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)
    cv2.putText(frame, f'Right: {right_count}', (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 100), 2)
    cv2.putText(frame, f'Total: {total_count}', (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)

    # Show frame
    cv2.imshow("Finger Counter (Both Hands)", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
