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
class virtcam():
    def start(self):
        pass
    def stop(self):
        pass
    def start_encoder(self, file='', name='main'):
        pass
    def stop_encoder(self, file='', name='main'):
        pass

class cam():
    def apply_timestamp(self,request):
        colour = (255, 255, 255)
        origin = (0, 30)
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 1
        thickness = 2
        timestamp = time.strftime("%Y-%m-%d %X")
        with MappedArray(request, "main") as m:
            cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)
            cv2.putText(m.array, self.info1, (0, 80), font, 0.5, colour, 1)
            cv2.putText(m.array, self.info1, (0, 100), font, 0.5, colour, 1)

        with MappedArray(request, "lores") as m:
            cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)
            cv2.putText(m.array, self.info1, (0, 80), font, 0.5, colour, 1)
            cv2.putText(m.array, self.info1, (0, 100), font, 0.5, colour, 1)

    def __init__(self,stream=None, cam_exist=False):
        self.camera_on = False
        self.fileout_on = False
        self.webout_on = False
        self.info1 = ''
        self.info2 = ''
        self.cam_exist = cam_exist
        self.bitrate = 4000000
        if not self.cam_exist: #Create fake objects
            self.picam2 = virtcam()
            self.encoderfile='encoderfile'
            self.encoderweb='encoderweb'

        if self.cam_exist:
            self.picam2 = Picamera2() #2028x1520-pBCC
            self.video_config = self.picam2.create_video_configuration(main={"size": (1600, 1200)},lores={"size": (800, 600)},
                                                                       controls={"FrameDurationLimits": (80000, 80000)})
            # self.video_config.controls.FrameRate = 25.0
            # picam2.set_controls({"ExposureTime": 10000, "AnalogueGain": 1.0})

            self.picam2.configure(self.video_config)
            self.picam2.pre_callback = self.apply_timestamp

            # self.encoderweb = MJPEGEncoder(bitrate    =10000000)
            self.encoderfile = H264Encoder(bitrate    =4000000)
            self.webstream = stream
            # self.outputweb = FileOutput(self.webstream)
            # self.encoderweb.output = self.outputweb
            # self.outputfile = FileOutput('/media/video.h264')
            # self.encoderfile.output = self.outputfile

    def start_file(self):
        if not self.fileout_on:
            self.fileout_on = True
            sname= '/media/'+time.strftime("%Y_%m_%d_%X")+'.h264'
            sname = sname.replace(":","_")
            print("FILE NAME: " + sname)
            if self.cam_exist:
                self.outputfile = FileOutput(sname)
                self.encoderfile.output = self.outputfile
            if (not self.camera_on):
                self.picam2.start()
                print("CAM_ON_HEAT")
                self.camera_on = True
                time.sleep(2) #Heat camera
            print("start_file:",sname)
            self.picam2.start_encoder(self.encoderfile, name='main')

    def start_stream(self, webbitrate = self.bitrate):
        if not self.webout_on or self.bitrate!=webbitrate:
            self.webout_on = True
            if (not self.camera_on):
                self.picam2.start()
                print("CAM_ON_HEAT")
                self.camera_on = True
            if self.bitrate!=webbitrate:
                self.picam2.stop_encoder(self.encoderweb, name='lores')
            if self.cam_exist:
                print("start_stream with "+str(self.bitrate)+" Mbit/s")
                self.encoderweb = MJPEGEncoder(bitrate=self.bitrate)
                self.outputweb = FileOutput(self.webstream)
                self.encoderweb.output = self.outputweb
                self.picam2.start_encoder(self.encoderweb, name='lores')

    def stop_file(self):
        if self.fileout_on:
            self.fileout_on = False
            print("stop_file")
            self.picam2.stop_encoder(self.encoderfile)
        if not self.webout_on:
            self.picam2.stop()

    def stop_stream(self):
        if self.webout_on:
            self.webout_on = False
            print("stop_stream")
            self.picam2.stop_encoder(self.encoderweb)
        if not self.fileout_on:
            self.stop_cam()

    def stop_cam(self):
        if self.camera_on:
            self.fileout_on = False
            self.webout_on = False
            print("CAM_OFF")
            self.picam2.stop_encoder(self.encoderweb)
            self.picam2.stop_encoder(self.encoderfile)
            self.camera_on = False
            self.picam2.stop()
