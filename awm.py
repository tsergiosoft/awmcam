#!/usr/bin/python3
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput

import io
import time
import configparser
import logging
import socketserver
from http import server
from threading import Condition
import threading

PAGE = """\
<html>
<head>
<title>picamera2 MJPEG streaming demo</title>
</head>
<body>
<h1>Picamera2 MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="800" height="600" />
</body>
</html>
"""





class webcamserver(threading.Thread):
    streamout = None

    def __init__(self, host="localhost", port=8080):
        super().__init__()
        self.stop_event = threading.Event()

        self.host = host
        self.port = port
        self.address = (self.host, self.port)

        self.streamout = self.StreamingOutput()
        self.handler = self.StreamingHandler
        self.handler.outerclass = self
        self.server = self.StreamingServer(self.address, self.handler)

    class StreamingOutput(io.BufferedIOBase):
        def __init__(self):
            self.frame = None
            self.condition = Condition()

        def write(self, buf):
            with self.condition:
                self.frame = buf
                self.condition.notify_all()

    class StreamingHandler(server.BaseHTTPRequestHandler):
        outerclass = None

        def do_GET(self):
            if self.path == '/':
                self.send_response(301)
                self.send_header('Location', '/index.html')
                self.end_headers()
            elif self.path == '/index.html':
                content = PAGE.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
            elif self.path == '/stream.mjpg':
                self.send_response(200)
                self.send_header('Age', 0)
                self.send_header('Cache-Control', 'no-cache, private')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
                self.end_headers()
                try:
                    while True:
                        with self.outerclass.streamout.condition:
                            self.outerclass.streamout.condition.wait()
                            frame = self.outerclass.streamout.frame
                        self.wfile.write(b'--FRAME\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', len(frame))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b'\r\n')
                except Exception as e:
                    logging.warning(
                        'Removed streaming client %s: %s',
                        self.client_address, str(e))
            else:
                self.send_error(404)
                self.end_headers()

    class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
        allow_reuse_address = True
        daemon_threads = True

    ################## own class definitions  #############################
    def run(self):
        # self.server.serve_forever()
        while not self.stop_event.is_set():
            self.server.handle_request()  # Handle a single request
            time.sleep(1 / 24)  # Adjust the sleep duration as needed

    def stop(self):
        self.stop_event.set()

config = configparser.ConfigParser()
config.read('params.ini')
TALON_SN	=config['DEFAULT']['SN']
CLOUD_IP	=config['DEFAULT']['CLOUD_IP']
CLOUD_USER	=config['DEFAULT']['CLOUD_USER']
REMOTE_SSH_PORT =config['DEFAULT']['REMOTE_SSH_PORT']
REMOTE_CAM_PORT =config['DEFAULT']['REMOTE_CAM_PORT']
REMOTE_MAV_PORT =config['DEFAULT']['REMOTE_MAV_PORT']
MAV_MASTER	=config['DEFAULT']['MAV_MASTER']
MAV_BAUD	=config['DEFAULT']['MAV_BAUD']
#MAVPROXY_IP_PORT=config['DEFAULT']['MAVPROXY_IP_PORT'] #may be delete and use 127.0.0.1:14550
MAV_DRONEKIT=config['DEFAULT']['MAV_DRONEKIT']

print("TALON_SN="+TALON_SN+" CLOUD_IP="+CLOUD_IP)

wserver = webcamserver(host="localhost", port=8080)
wserver.start()

picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (800, 600)})
picam2.configure(video_config)

encoder = MJPEGEncoder(10000000)
output1 = FileOutput(wserver.streamout)
output2 = FileOutput('testm2.mjpeg')
encoder.output = [output1, output2]
picam2.start_encoder(encoder)
picam2.start()
time.sleep(5)
print("stop picam")
picam2.stop()
picam2.stop_encoder(encoder)
print("stop wserver")
wserver.stop()
print("join")
wserver.join()
