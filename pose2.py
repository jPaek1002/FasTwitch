# MediaPipe pose detection test - debugged mostly
import tensorflow
import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)
i=0
while cap.isOpened():
    i+=1
    _, frame = cap.read()
    RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(RGB)
    mp_drawing.draw_landmarks(frame,results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imshow('Overlay', frame)
    #cv2.imwrite('Overlay'+str(i)+'.png',frame)
    if(cv2.waitKey(1)==ord('q')):
        break
cap.release()
cv2.destroyAllWindows()
