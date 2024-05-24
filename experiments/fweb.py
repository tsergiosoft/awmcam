from flask import Flask, Response
import cv2
import os, platform, time
from threading import Thread
# import tkinter as tk
# from tkinter import ttk

class MJPEGServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        ROOT = os.path.dirname(self.current_path)

        #if platform.system() == "Windows":
        self.logo_path = os.path.join(self.current_path, "camsimul", "logo.jpg")
        # self.cap = cv2.VideoCapture(0)
        self.frame_home = cv2.imread(self.logo_path)

        # @self.app.route('/video_feed')
        @self.app.route('/')
        def video_feed():
            return Response(self.generate_frames(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

    def generate_frames(self):
        while True:
            time.sleep(0.1)
        # success, frame = self.cap.read()
        # if not success:
        #     break
        # else:
            # ret, buffer = cv2.imencode('.jpg', frame)
            ret, buffer = cv2.imencode('.jpg', self.frame_home)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def run(self):
        self.app.run(host='0.0.0.0', port=5000)

    def stop(self):
        self.cap.release()

def start_server():
    server = MJPEGServer()
    server_thread = Thread(target=server.run)
    server_thread.daemon = True
    server_thread.start()
    return server

def stop_server(server):
    server.stop()

if __name__ == '__main__':

    server = start_server()
    while True:
        time.sleep(0.1)
    # root = tk.Tk()
    # root.title("MJPEG Stream Server Control")
    #
    # server = None
    #
    # def on_start():
    #     global server
    #     if server is None:
    #         server = start_server()
    #         status_label.config(text="Server running...")
    #
    # def on_stop():
    #     global server
    #     if server is not None:
    #         stop_server(server)
    #         server = None
    #         status_label.config(text="Server stopped")
    #
    # start_button = ttk.Button(root, text="Start Server", command=on_start)
    # start_button.pack(pady=10)
    #
    # stop_button = ttk.Button(root, text="Stop Server", command=on_stop)
    # stop_button.pack(pady=10)
    #
    # status_label = ttk.Label(root, text="Server stopped")
    # status_label.pack(pady=10)
    #
    # root.mainloop()
