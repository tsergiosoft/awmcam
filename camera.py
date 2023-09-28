#!/usr/bin/python3
try:
    from picamera2 import Picamera2
    from picamera2.encoders import MJPEGEncoder, H264Encoder, Quality
    from picamera2.outputs import FileOutput
    from picamera2 import MappedArray, Picamera2
except:
    pass

import time
import cv2

class cam():
    def apply_timestamp(self,request):
        colour = (0, 255, 0)
        origin = (0, 30)
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 1
        thickness = 2
        timestamp = time.strftime("%Y-%m-%d %X")
        with MappedArray(request, "main") as m:
            cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)
        print(timestamp)

    def __init__(self,stream=None):
        self.picam2 = Picamera2()
        # self.video_config = self.picam2.create_video_configuration(main={"size": (320, 200)})
        #2028x1520-pBCC
        self.video_config = self.picam2.create_video_configuration(main={"size": (1600, 1200)},
                                                          lores={"size": (800, 600)})
        self.picam2.configure(self.video_config)
        self.picam2.pre_callback = self.apply_timestamp

        self.encoder1 = MJPEGEncoder(bitrate    =5000000)
        self.encoder2 = H264Encoder(bitrate     =3000000)
        self.webstream = stream
        self.output1 = FileOutput(self.webstream)
        #self.output1 = FfmpegOutput("-f mpegts udp://127.0.0.1:8081")
        #self.output1 = FfmpegOutput("test.ts")

        # self.output1 = FfmpegOutput("-f hls -hls_time 4 -hls_list_size 5 -hls_flags delete_segments -hls_allow_cache 0 stream.m3u8")

        self.output2 = FileOutput('test.h264')
        #self.encoder.output = [self.output1, self.output2]
        self.encoder1.output = self.output1
        self.encoder2.output = self.output2

    def start_stream(self):
        print("start_stream")
        #self.picam2.start_encoder(self.encoder1, width=800, height=600)
        #self.picam2.start_encoder(self.encoder2, width=2028, height=1520)
        self.picam2.start_encoder(self.encoder1, name='lores')
        self.picam2.start_encoder(self.encoder2, name='main')
        self.picam2.start()

    def stop_stream(self):
        print("stop_stream")
        self.picam2.stop_encoder(self.encoder1)
        self.picam2.stop_encoder(self.encoder2)
        self.picam2.stop()

    def start_file(self):
        pass


