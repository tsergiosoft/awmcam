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
    # outerstream = None
    def __init__(self, host="0.0.0.0", port=5000):
        super().__init__()
        self.daemon = True
        self.stop_event = threading.Event()
        self.host = host
        self.port = port
        self.streamout = self.StreamingOutput()
        self.frame_cnt = 0
        self.app = Flask(__name__)
        # self.app.outerstream = self.streamout

        @self.app.route('/')
        @self.app.route('/index.html')
        def video_feed():
            return Response(self.generate_frames(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
    def generate_frames(self):
        while True:
            with self.streamout.condition:
                self.streamout.condition.wait()
                print("new cond")
                colour = (255, 10, 20)
                origin = (0, 40)
                font = cv2.FONT_HERSHEY_SIMPLEX
                scale = 0.3
                thickness = 1
                self.frame_cnt += 1
                # print(f"\r{wcam.frame_cnt}", end="")
                timestamp = time.strftime("%Y-%m-%d %X")
                timestamp = timestamp + f" frame={self.frame_cnt}"
                img = self.streamout.imgframe.copy()
                cv2.putText(img, timestamp, origin, font, scale, colour, thickness)

                ret, buffer = cv2.imencode('.jpg', img)
                frame = buffer.tobytes()
                # ret, buffer = cv2.imencode('.jpg', self.frame_home)
                # frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    def run(self):
        print('Web server thread running..')
        self.app.run(host=self.host, port=self.port)

    def stop(self):
        self.stop_event.set()
        print("shutdown_web")
        # shutdown_url = f"http://127.0.0.1:8080/shutdown"
        # try:
        #     requests.get(shutdown_url)
        # except requests.RequestException as e:
        #     print(f"Error while shutting down server: {e}")
        # finally:
        #     self.server.shutdown()
        self.server.shutdown()

    # class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    #     allow_reuse_address = True
    #     daemon_threads = True

    # class StreamingHandler(server.BaseHTTPRequestHandler):
    #     outerstream = None
    #
    #     def do_GET(self):
    #         if self.path == '/':
    #             print("self.path == '/'")
    #             self.send_response(301)
    #             self.send_header('Location', '/index.html')
    #             self.end_headers()
    #         elif self.path == '/index.html':
    #             print("self.path == '/index.html'")
    #             content = PAGE.encode('utf-8')
    #             self.send_response(200)
    #             self.send_header('Content-Type', 'text/html')
    #             self.send_header('Content-Length', len(content))
    #             self.end_headers()
    #             self.wfile.write(content)
    #         elif self.path == '/stream.mjpg':
    #             print("self.path == '/stream'")
    #             self.send_response(200)
    #             self.send_header('Age', 0)
    #             self.send_header('Cache-Control', 'no-cache, private')
    #             self.send_header('Pragma', 'no-cache')
    #             self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
    #             self.end_headers()
    #             try:
    #                 while True:
    #                     with self.outerstream.condition:
    #                         self.outerstream.condition.wait()
    #                         frame = self.outerstream.frame
    #                     self.wfile.write(b'--FRAME\r\n')
    #                     self.send_header('Content-Type', 'image/jpeg')
    #                     self.send_header('Content-Length', len(frame))
    #                     self.end_headers()
    #                     self.wfile.write(frame)
    #                     self.wfile.write(b'\r\n')
    #             except Exception as e:
    #                 logging.warning(
    #                     'Removed streaming client %s: %s',
    #                     self.client_address, str(e))
    #         else:
    #             self.send_error(404)
    #             self.end_headers()

    class StreamingOutput(io.BufferedIOBase):
        def __init__(self):
            self.frame = None
            self.condition = Condition()
            self.clear_interval = 30  # Set the clear interval to 60 seconds
            self.last_clear_time = time.time()

        def write(self, buf):
            with self.condition:
                # print("new frame")
                # ret, buffer = cv2.imencode('.jpg', buf)
                # self.frame = buffer.tobytes()
                self.imgframe = buf

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
        time.sleep(0.1)
        i+=1

    wserver.stop()
    print("stop!!!!")
    wserver.join()
    print("join!!!!")
