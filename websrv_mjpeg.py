#!/usr/bin/python3
import logging
import io
import time
import socketserver
from http import server
from threading import Condition
import threading

# <meta http-equiv="refresh" content="15">

PAGE = """\
<html>
<head>
<title>MJPEG streaming</title>
</head>
<body>
<h1>MJPEG streaming</h1>
<img src="stream.mjpg" width="800" height="600" />
</body>
</html>
"""

class webserverjpg(threading.Thread):
    streamout = None

    def __init__(self, host="localhost", port=8080):
        super().__init__()
        self.stop_event = threading.Event()

        self.host = host
        self.port = port
        self.address = (self.host, self.port)

        self.streamout = self.StreamingOutput()
        self.handler = self.StreamingHandler
        self.handler.outerstream = self.streamout
        self.server = self.StreamingServer(self.address, self.handler)

    class StreamingOutput(io.BufferedIOBase):
        def __init__(self):
            self.frame = None
            self.condition = Condition()
            self.clear_interval = 5  # Set the clear interval to 60 seconds
            self.last_clear_time = time.time()


        def write(self, buf):
            with self.condition:
                self.frame = buf
                self.condition.notify_all()
                # Check if it's time to clear the buffer
                current_time = time.time()
                if current_time - self.last_clear_time >= self.clear_interval:
                    self.clear_buffer()
                    self.last_clear_time = current_time

        def clear_buffer(self):
            with self.condition:
                self.frame = None

    class StreamingHandler(server.BaseHTTPRequestHandler):
        outerstream = None

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
                        with self.outerstream.condition:
                            self.outerstream.condition.wait()
                            frame = self.outerstream.frame
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

    def run(self):
        print('Web server thread running..')
        self.server.serve_forever()
        # while not self.stop_event.is_set():
        #     self.server.handle_request()  # Handle a single request
        #     time.sleep(1/5)  # Adjust the sleep duration as needed

    def stop(self):
        self.stop_event.set()