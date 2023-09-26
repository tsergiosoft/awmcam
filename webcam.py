#!/usr/bin/python3

# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
# Run this script, then point a web browser at http:<this-ip-address>:8000
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).
import glob
import io
import time
import numpy as np

import logging
import socketserver
from http import server
from threading import Condition
import threading

#if (glob.PICAM == 1):
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput, FfmpegOutput

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
    def __init__(self, host="localhost", port=8081):
        super().__init__()
        self.host = host
        self.port = port
        self.address = (self.host, self.port)
        self.handler = self.StreamingHandler
        self.handler.outerclass = self
        self.server = self.StreamingServer(self.address, self.handler)


        # self.output = self.StreamingOutput()
        # self.encoder = H264Encoder(repeat=True, iperiod=15)
        self.encoder = JpegEncoder(q=40)
        # self.output1 = FfmpegOutput("-f mpegts udp://<ip-address>:8080")
        self.output1 = FileOutput(self.StreamingOutput())
        # self.output2 = FileOutput('test2.h264')
        self.encoder.output = self.output1
        # self.encoder.output = [self.output1, self.output2]

        # self.file_saving_thread = self.filesaver(self.output)
        # self.file_saving_thread.start()

        print("webcamserver: PICAM=", glob.PICAM)
        # if (glob.PICAM == 1):
        self.picam2 = Picamera2()

        """
        class filesaver(threading.Thread):
        def __init__(self, stream):
            super().__init__()
            self.stream = stream
            # self.video_writer = cv2.VideoWriter("/home/pi/awmcam/mjpeg.avi", cv2.VideoWriter_fourcc(*'MJPG'), 12, (800,600))
            self.video_writer = cv2.VideoWriter('/home/pi/awmcam/mjpeg.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 12, (800,600))

        def run(self):
            print("file_saving_process in...")
            fcnt = 0
            while True:
                # Check for new data in streaming_output.frame
                with self.stream.condition:
                    self.stream.condition.wait()
                    fcnt = fcnt + 1
                    print(fcnt)
                    data = self.stream.frame
                    #img1 = np.array(data)
                    self.video_writer.write(data)
                    print(len(data))
                    #cv2.rectangle(data, (100, 100), (200, 200), (0, 255, 0), 3)

                    if (fcnt>400):
                        self.video_writer.release()
                        break
        """

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
                        with self.outerclass.output1.condition:
                            self.outerclass.output1.condition.wait()
                            frame = self.outerclass.output1.frame
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

    def start_stream(self):
        print("Start CAMERA")
        # if (glob.PICAM == 1):
        self.picam2.create_video_configuration(main={"size": (800, 600)})
        self.picam2.video_configuration.controls.FrameRate = 1.0
        self.picam2.configure("video")
        # self.picam2.start_recording(encoder, FileOutput(self.output1))

        # Start streaming to the network.
        self.picam2.start_encoder(self.encoder)
        self.picam2.start()
        # time.sleep(5)



        # self.output2.fileoutput = "test.h264"
        # self.output2.start()
        # time.sleep(5)
        # self.output2.stop()
        # time.sleep(5)

    def stop_stream(self):
            # if (glob.PICAM == 1):
            print("Stop CAMERA")
            self.output2.stop()
            self.picam2.stop_recording()



