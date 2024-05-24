#!/usr/bin/python3
import logging
import io
import os, platform
import time
import socketserver
from http import server
from flask import Flask, Response
from threading import Condition
import threading
import cv2


class webserverjpg(threading.Thread):
    def __init__(self, host="0.0.0.0", port=5000):
        super().__init__()
        self.daemon = True
        self.stop_event = threading.Event()
        self.host = host
        self.port = port
        self.streamout = self.StreamingOutput()
        self.frame_cnt = 0
        self.app = Flask(__name__)

        @self.app.route('/')
        @self.app.route('/index.html')
        def video_feed():
            return Response(self.get_frames(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
    def get_frames(self):
        while True:
            with self.streamout.condition:
                self.streamout.condition.wait()
                frame = self.streamout.jpgframe
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def run(self):
        print('Web server thread running..')
        self.app.run(host=self.host, port=self.port)

    def stop(self):
        self.stop_event.set()

    class StreamingOutput(io.BufferedIOBase):
        def __init__(self):
            self.frame = None
            self.condition = Condition()
            self.clear_interval = 30  # Set the clear interval to 60 seconds
            self.last_clear_time = time.time()
            self.frame_cnt = 0

        def write(self, buf):
            with self.condition:
                img = buf.copy()

                # colour = (255, 10, 20)
                # origin = (0, 40)
                # font = cv2.FONT_HERSHEY_SIMPLEX
                # scale = 0.5
                # thickness = 1
                # self.frame_cnt += 1
                # timestamp = time.strftime("%Y-%m-%d %X")
                # timestamp = timestamp + f" frame={self.frame_cnt}"
                # cv2.putText(img, timestamp, origin, font, scale, colour, thickness)

                ret, buffer = cv2.imencode('.jpg', img)
                self.jpgframe = buffer.tobytes()

                # Check if it's time to clear the buffer
                current_time = time.time()
                if self.clear_interval > 0 and (current_time - self.last_clear_time >= self.clear_interval):
                    print("web -> clear buffer")
                    self.clear_buffer()
                    self.last_clear_time = current_time
                else:
                    self.condition.notify_all()

        def clear_buffer(self):
            with self.condition:
                self.frame = None

if __name__ == '__main__':
    print("websrv if __name__ == '__main__'")
    wserver = webserverjpg(host="0.0.0.0", port=8080)
    wserver.start()

    current_path = os.path.dirname(os.path.abspath(__file__))
    ROOT = os.path.dirname(current_path)
    if platform.system() == "Windows":
        logo_path = os.path.join(current_path, "camsimul", "logo.jpg")
    elif platform.system() == "Linux":
        logo_path = os.path.join(current_path, "camsimul", "logo.jpg")

    print(logo_path)
    frame_home = cv2.imread(logo_path)

    # video_capture = cv2.VideoCapture(0)
    i=0
    while True:
    # while i<200:
    #     ret, frame = video_capture.read()
    #     if not ret:
    #         frame = frame_home
        frame = frame_home
        wserver.streamout.write(buf=frame)
        time.sleep(0.01)

    wserver.stop()
    print("stop!!!!")
    wserver.join()
    print("join!!!!")
