#!/usr/bin/python3
import time
import io

from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput

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
    output2 = None
    streamout = None
    def __init__(self, host="localhost", port=8080):
        super().__init__()
        self.stop_event = threading.Event()

        self.host = host
        self.port = port
        self.address = (self.host, self.port)
        self.handler = self.StreamingHandler
        self.handler.outerclass = self
        self.server = self.StreamingServer(self.address, self.handler)

        self.streamout = self.StreamingOutput()

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
        self.server.serve_forever()
        # while not self.stop_event.is_set():
        #     self.server.handle_request()  # Handle a single request
        #     time.sleep(1/24)  # Adjust the sleep duration as needed

    def stop(self):
        self.server.shutdown()
        self.stop_event.set()

srv = webcamserver()
srv.start()

picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (800, 600)})
picam2.configure(video_config)

encoder = MJPEGEncoder(10000000)
output1 = FileOutput(srv.streamout)
output2 = FileOutput('testm2.mjpeg')
encoder.output = [output1, output2]
picam2.start_encoder(encoder)
picam2.start()
time.sleep(10)
picam2.stop_recording()