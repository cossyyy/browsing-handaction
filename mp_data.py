import csv
import numpy as np
import mediapipe as mp
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
)
cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue
    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

#重畳描画
    results_hands = hands.process(image)
    if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            # print('Handedness:', results.multi_handedness)
            mp_drawing.draw_landmarks(image_blank, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            #データを蓄積
    with open('./hands/sample_hands.csv', 'a', newline='') as f:
        landmark_point = []
        writer = csv.writer(f)
        if results.multi_hand_landmarks:
            idx = 0
            idx += 1
            print('Handedness:', results.multi_handedness)
            for hand_landmarks in results.multi_hand_landmarks:
                for index, landmark in enumerate(hand_landmarks.landmark):
                    landmark_x = min(int(landmark.x * image_width), image_width - 1)
                    landmark_y = min(int(landmark.y * image_height), image_height - 1)

                    landmark_ = landmark_x, landmark_y
                    landmark_point.append(landmark_x)
                    landmark_point.append(landmark_y)

                    print(landmark_point)
                writer.writerow(np.array(landmark_point))

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image_width, image_height = image.shape[1], image.shape[0]
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            #print('Handedness:', results.multi_handedness)
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break
hands.close()
cap.release()