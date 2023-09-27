#!/usr/bin/python3
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput

from websrv import webcamserver
import time
import configparser

config = configparser.ConfigParser()
config.read('params.ini')
TALON_SN	=config['DEFAULT']['SN']
CLOUD_IP	=config['DEFAULT']['CLOUD_IP']
CLOUD_USER	=config['DEFAULT']['CLOUD_USER']
REMOTE_SSH_PORT =config['DEFAULT']['REMOTE_SSH_PORT']
REMOTE_CAM_PORT =config['DEFAULT']['REMOTE_CAM_PORT']
REMOTE_MAV_PORT =config['DEFAULT']['REMOTE_MAV_PORT']
MAV_MASTER	=config['DEFAULT']['MAV_MASTER']
MAV_BAUD	=config['DEFAULT']['MAV_BAUD']
#MAVPROXY_IP_PORT=config['DEFAULT']['MAVPROXY_IP_PORT'] #may be delete and use 127.0.0.1:14550
MAV_DRONEKIT=config['DEFAULT']['MAV_DRONEKIT']

print("TALON_SN="+TALON_SN+" CLOUD_IP="+CLOUD_IP)


class cam():
    def __init__(self):
        self.picam2 = Picamera2()
        self.video_config = self.picam2.create_video_configuration(main={"size": (800, 600)})
        self.picam2.configure(self.video_config)

        # self.encoder = MJPEGEncoder(10000000)
        self.encoder = H264Encoder()
        self.output1 = FileOutput(wserver.streamout)
        self.output2 = FileOutput('testm2.mjpeg')
        self.encoder.output = [self.output1, self.output2]

    def start_stream(self):
        print("start_stream")
        self.picam2.start_encoder(self.encoder)
        self.picam2.start()

    def stop_stream(self):
        print("stop_stream")
        self.picam2.stop()
        self.picam2.stop_encoder(self.encoder)

    def start_file(self):
        pass

wserver = webcamserver(host="localhost", port=8080)
wserver.start() #Thread

pcam = cam()
pcam.start_stream()
time.sleep(5)
pcam.stop_stream()
time.sleep(5)
pcam.start_stream()
time.sleep(5)
pcam.stop_stream()

print("stop wserver")
wserver.stop() #Thread
wserver.join()
