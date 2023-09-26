import cv2
import numpy as np
from io import BufferedIOBase

class VideoStreamWriter(BufferedIOBase):
    def __init__(self, file_name, frame_rate, frame_size):
        self.file_name = file_name
        self.frame_rate = frame_rate
        self.frame_size = frame_size
        self.video_writer = cv2.VideoWriter(file_name, cv2.VideoWriter_fourcc(*'MJPG'), frame_rate, frame_size)
        self.buffer = bytearray()

    def write(self, data):
        # Append video frame data to the internal buffer
        self.buffer += data

    def flush(self):
        if self.buffer:
            # Convert the buffer data into a video frame
            frame = np.frombuffer(self.buffer, dtype=np.uint8).reshape(self.frame_size)
            # Write the frame to the video file
            self.video_writer.write(frame)
            self.buffer = bytearray()  # Clear the buffer

    def close(self):
        # Make sure to flush any remaining data and close the video writer
        self.flush()
        self.video_writer.release()

# Usage
import time

# Create a VideoStreamWriter instance
video_writer = VideoStreamWriter("output.avi", 30.0, (640, 480))

# Generate and send random noise frames to the video writer
for _ in range(300):
    frame_data = np.random.randint(0, 255, size=(480, 640, 3), dtype=np.uint8).tobytes()
    video_writer.write(frame_data)
    time.sleep(1.0 / 30)  # Simulate a frame rate of 30 frames per second

# Close the video writer to finalize the output video
video_writer.close()
