#!/usr/bin/python3
import logging
import io
import time
import socketserver
from http import server
from threading import Condition
import threading


PAGE = """\<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Streaming</title>
</head>
<body>
    <!-- Video Element -->
    <video id="videoPlayer" controls autoplay>
        <!-- Provide the video source URL here -->
        <source src="YOUR_VIDEO_STREAM_URL_HERE" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</body>
</html>
"""

PAGE = """\
<html>
<head>
    <title>MPEG-2 Transport Stream Viewer</title>
</head>
<body>
    <video width="640" height="480" controls>
        <source src="http://localhost:8081/stream.mpegts" type="video/mp2t">
        Your browser does not support the video tag.
    </video>
</body>
</html>
"""

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

class webserver_experim(threading.Thread):
    def __init__(self, host="localhost", port=8080):
        super().__init__()
        self.stop_event = threading.Event()

        self.host = host
        self.port = port
        self.address = (self.host, self.port)

        self.handler = self.StreamingHandler

        # Create an HTTP server with the custom handler
        self.server = socketserver.TCPServer(("", self.port), self.handler)

    class StreamingHandler(server.BaseHTTPRequestHandler):
        print('Client calls...')
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
            elif self.path == '/stream.mpegts':
                # Set the appropriate content type for MPEG-2 transport stream
                self.send_response(200)
                self.send_header('Content-type', 'video/mpeg')
                self.end_headers()

                # Open and stream the video file
                # with open('your_stream_file.ts', 'rb') as video_stream:
                #     self.wfile.write(video_stream.read())

            else:
                self.send_error(404)
                self.end_headers()

    ################## own class definitions  #############################
    def run(self):
        print('Web server thread running..')
        # try:
        #     self.server.serve_forever()
        # except KeyboardInterrupt:
        #     pass
        # self.server.serve_forever()
        while not self.stop_event.is_set():
            self.server.handle_request()  # Handle a single request
            time.sleep(1 / 24)  # Adjust the sleep duration as needed

    def stop(self):
        self.stop_event.set()