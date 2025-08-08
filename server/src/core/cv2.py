import os
import numpy as np
import cv2



def temp():
    cap = cv2.VideoCapture('http://<ESP32-CAM-IP>/video')

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('ESP32-CAM', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()