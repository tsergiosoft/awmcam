#!/usr/bin/python3
import time

from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput

picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (800, 600)})
picam2.configure(video_config)

encoder = MJPEGEncoder(10000000)
output1 = FileOutput('testm.mjpeg')
output2 = FileOutput('testm2.mjpeg')
encoder.output = [output1, output2]
picam2.start_encoder(encoder)
picam2.start()
time.sleep(10)
picam2.stop_recording()