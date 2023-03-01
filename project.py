from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import av
import cv2
import os
import streamlit as st
from keras.models import load_model
import numpy as np
from pygame import mixer
import time
from datetime import datetime
from datetime import date

mixer.init()
sound = mixer.Sound('alarm.wav')

face = cv2.CascadeClassifier('haar cascade files/haarcascade_frontalface_alt.xml')
leye = cv2.CascadeClassifier('haar cascade files/haarcascade_lefteye_2splits.xml')
reye = cv2.CascadeClassifier('haar cascade files/haarcascade_righteye_2splits.xml')

lbl = ['Close', 'Open']

model = load_model("models/cnncat2.h5")
path = os.getcwd()
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
state = {"cnt": 0}
state2 = {"score": 0}
map_for_counter={'counter':10}
score = 0
thicc = 2
rpred = [99]
lpred = [99]


def get_state():
    return state


RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})


class VideoProcessor:
    def recv(self, frame):
        rpred = [99]
        lpred = [99]
        state = get_state()
        cnt = state["cnt"]
        score = state2["score"]
        img = frame.to_ndarray(format="bgr24")
        height, width = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face.detectMultiScale(gray, minNeighbors=5, scaleFactor=1.1, minSize=(25, 25))
        left_eye = leye.detectMultiScale(gray)
        right_eye = reye.detectMultiScale(gray)
        cv2.rectangle(img, (0, height - 50), (200, height), (0, 0, 0), thickness=cv2.FILLED)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (100, 100, 100), 1)

        for (x, y, w, h) in right_eye:
            r_eye = img[y:y + h, x:x + w]
            # global cnt
            cnt = cnt + 1
            r_eye = cv2.cvtColor(r_eye, cv2.COLOR_BGR2GRAY)
            r_eye = cv2.resize(r_eye, (24, 24))
            r_eye = r_eye / 255
            r_eye = r_eye.reshape(24, 24, -1)
            r_eye = np.expand_dims(r_eye, axis=0)
            rpred = np.argmax(model.predict(r_eye), axis=-1)
            if (rpred[0] == 1):
                lbl = 'Open'
            if (rpred[0] == 0):
                lbl = 'Closed'
            break

        for (x, y, w, h) in left_eye:
            l_eye = img[y:y + h, x:x + w]
            cnt = cnt + 1
            l_eye = cv2.cvtColor(l_eye, cv2.COLOR_BGR2GRAY)
            l_eye = cv2.resize(l_eye, (24, 24))
            l_eye = l_eye / 255
            l_eye = l_eye.reshape(24, 24, -1)
            l_eye = np.expand_dims(l_eye, axis=0)
            lpred = np.argmax(model.predict(l_eye), axis=-1)
            if (lpred[0] == 1):
                lbl = 'Open'
            if (lpred[0] == 0):
                lbl = 'Closed'
            break
        state["cnt"] = cnt
        if (rpred[0] == 0 and lpred[0] == 0):
            score = score + 1
            cv2.putText(img, "Closed", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        else:
            score = score - 1
            cv2.putText(img, "Open", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        if (score < 0):
            score = 0
        cv2.putText(img, 'Score:' + str(score), (100, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        if (score > 5):
            try:
                if score==6:
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    today = date.today()
                    current_date=today.strftime("%m/%d/%y")
                    file= open("timer.txt", "a")
                    file.write('\n')
                    file.write(current_date)
                    file.write(',')
                    file.write(current_time)
                    file.close()
                sound.play()
               # map_for_counter['counter']=map_for_counter['counter']+1
            except:  # isplaying = False
                pass
            # cv2.rectangle(img,(0,0),(width,height),(0,0,255),thicc)
        state2["score"] = score
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return av.VideoFrame.from_ndarray(img, format='bgr24')
        return av.VideoFrame.from_ndarray(img, format='bgr24')


def main():
    # Face Analysis Application #
    # print(cnt)
    webrtc_streamer(key="key", video_processor_factory=VideoProcessor,
                    rtc_configuration=RTCConfiguration(
                        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
                    )
                    )


if __name__ == "__main__":
    main()