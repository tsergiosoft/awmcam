#!/usr/bin/python3
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
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

wserver = webcamserver(host="localhost", port=8080)
wserver.start()

picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (800, 600)})
picam2.configure(video_config)

encoder = MJPEGEncoder(10000000)
output1 = FileOutput(wserver.streamout)
output2 = FileOutput('testm2.mjpeg')
encoder.output = [output1, output2]
picam2.start_encoder(encoder)
picam2.start()
time.sleep(5)
print("stop picam")
picam2.stop()
picam2.stop_encoder(encoder)
print("stop wserver")
wserver.stop()
print("join")
wserver.join()
