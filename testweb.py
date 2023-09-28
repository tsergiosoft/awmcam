import argparse
import http.server
import socketserver
import threading
import time

class CustomHTTPServer(threading.Thread):
    def __init__(self, host="localhost", port=8081):
        super().__init__()
        self.host = host
        self.port = port
        self.stopped = threading.Event()

    def run(self):
        handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer((self.host, self.port), handler) as httpd:
            print(f"Serving on http://{self.host}:{self.port}/")

            while not self.stopped.is_set():
                print('handle request')
                httpd.handle_request()


def main():
    parser = argparse.ArgumentParser(description="Custom HTTP Server")
    parser.add_argument("--host", default="localhost", help="Host name to listen on (default: localhost)")
    parser.add_argument("--port", type=int, default=8081, help="Port number to listen on (default: 8081)")
    args = parser.parse_args()

    server = CustomHTTPServer(host=args.host, port=args.port)
    server.start()

    try:
        # Run the main code for 2 minutes
        time.sleep(2)
    except KeyboardInterrupt:
        pass

    # Stop the HTTP server gracefully
    server.stopped.set()
    server.join()

if __name__ == "__main__":
    main()
