from datetime import datetime
from time import sleep
import streamlit as st
import cv2

st.title("Motion Detector")
start = st.button("Start Camera")


if start:
    streamlit_image = st.image([])
    camera = cv2.VideoCapture(0)

    while True:
        sleep(1)
        now = datetime.now()

        current_time = now.strftime("%d-%m-%Y %H:%M:%S")

        check, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cv2.putText(img=frame, text=current_time,
                    org=(50, 50), fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=1, color=(20, 100, 200), thickness=2, 
                    lineType=cv2.LINE_AA)
        
        streamlit_image.image(frame)
