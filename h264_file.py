#!/usr/bin/python3
import time

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder, H264Encoder

picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (320, 240)})
picam2.configure(video_config)

picam2.start_preview()
# encoder = JpegEncoder(q=70)
encoder = H264Encoder()
# self.output1 = FfmpegOutput("-f mpegts udp://<ip-address>:8080")

picam2.start_recording(encoder, 'test264.mjpeg')
time.sleep(10)
picam2.stop_recording()