#!/usr/bin/python3

# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
# Run this script, then point a web browser at http:<this-ip-address>:8000
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).

import io
import numpy as np
import logging
import socketserver
from http import server
from threading import Condition
import threading

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput



PAGE = """\
<html>
<head>
<title>picamera2 MJPEG streaming demo</title>
</head>
<body>
<h1>Picamera2 MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="1024" height="768" />
</body>
</html>
"""

class webcamserver(threading.Thread):
    def __init__(self, host="localhost", port=8081, pycam=False):
        super().__init__()
        self.host = host
        self.port = port
        self.pycam = pycam
        print("PICAM=", self.pycam)
        self.output = self.StreamingOutput()
        if (self.pycam):
            self.picam2 = Picamera2()

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
        # def __init__(self, myparent, *args):
        #     self.myparent = myparent
        #     super().__init__(*args)

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
                        with self.outerclass.output.condition:
                            self.outerclass.output.condition.wait()
                            frame = self.outerclass.output.frame
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
        address = (self.host, self.port)
        # server = self.StreamingServer(address, lambda *args, **kwargs: self.StreamingHandler(self,self, *args))
        handler = self.StreamingHandler
        handler.outerclass = self
        server = self.StreamingServer(address, handler)
        server.serve_forever()

        # file_saving_thread = threading.Thread(target=self.file_saving_process)
        # file_saving_thread.start()


    def file_saving_process(self):
        print("file_saving_process in...")
        fcnt = 0
        while True:
            # Check for new data in streaming_output.frame
            with self.output.condition:
                self.output.condition.wait()
                fcnt=fcnt+1
                print(fcnt)
                data = self.output.frame
                # Save data to a local file (implementation not shown)

    def start_stream(self):
        if self.pycam:
            print("Start stream")
            self.picam2.create_video_configuration(main={"size": (800, 600)})
            self.picam2.video_configuration.controls.FrameRate = 2.0
            self.picam2.configure("video")
            encoder = JpegEncoder(q=40)
            self.picam2.start_recording(encoder, FileOutput(self.output))

            # print("CREATE FILE SAVING THREAD")
            file_saving_thread = threading.Thread(target=self.file_saving_process)
            file_saving_thread.start()



    def stop_stream(self):
        if self.pycam:
            print("Stop stream")
            self.picam2.stop_recording()



