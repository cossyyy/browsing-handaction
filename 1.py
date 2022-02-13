import mediapipe as mp
from PIL import Image
import cv2
import csv
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
)
idx = 0
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

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image_width, image_height = image.shape[1], image.shape[0]
    with open('./hands/sample_hands6.csv',  'a', newline='') as f:
        list_landmarks = []
        landmark_point = []
        writer = csv.writer(f)
        if results.multi_hand_landmarks:
            idx += 1
            print('Handedness:', results.multi_handedness)
            for hand_landmarks in results.multi_hand_landmarks:
                for index, landmark in enumerate(hand_landmarks.landmark):
                    landmark_x = min(int(landmark.x * image_width), image_width - 1)
                    landmark_y = min(int(landmark.y * image_height), image_height - 1)

                    landmark_ = landmark_x,landmark_y #[idx,index, np.array((landmark_x, landmark_y))]
                    landmark_point.append(landmark_x)
                    landmark_point.append(landmark_y)

                    print(landmark_point)
                writer.writerow(np.array(landmark_point))
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            cv2.imshow('MediaPipe Hands', image)
            #cv2.imwrite('./image/annotated_image' + str(idx) + '.png', cv2.flip(image, 1))
            cv2.imwrite('./image/annotated_image' + str(idx) + '.png', image)

    #cos類似度の計算
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt


    def cos_sim(v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


    df = pd.read_csv('./hands/sample_hands9.csv', sep=',')
    # print(df.head(3)) #データの確認
    df = df.astype(int)

    print(df.iloc[0, :])

    # 以下のfor文で原点0(df.iloc[i,0], df.iloc[i,1])からの座標とするかどうかを決めている
    for i in range(1, len(df), 1):
        for j in range(0, 21, 2):
            df.iloc[i, 2 * j + 1] = df.iloc[i, 2 * j + 1] - df.iloc[i, 1]
            df.iloc[i, 2 * j] = df.iloc[i, 2 * j] - df.iloc[i, 0]

    cs_sim = []
    for i in range(1, len(df), 1):
        cs = cos_sim(df.iloc[30, :], df.iloc[i, :])
        # print(df.iloc[i,:]-df.iloc[i,0])
        print('cos similarity: {}-{}'.format(30, i), cs)
        cs_sim.append(cs)

    plt.figure(figsize=(12, 6))
    plt.plot(cs_sim)
    plt.ylim(0.9, )
    plt.savefig('./hands/cos_sim_hands_plot9.png')
    plt.show()

    if cv2.waitKey(5) & 0xFF == 27:
        break
hands.close()
cap.release()