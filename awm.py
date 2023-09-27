#!/usr/bin/python3
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from picamera2.outputs import FfmpegOutput

from websrv import webcamserver
import time, os
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
#os.system('pkill screen')
#os.system('screen -S awm -X kill') #SELF KILLER!!!!

os.system('screen -S ssh22 -X kill')
os.system('screen -S sshweb -X kill')
os.system('screen -S sshmav -X kill')
os.system('screen -S mav -X kill')
os.system('screen -S web -X kill')
time.sleep(1)
os.system('screen -dmS ssh22 bash -c "/home/pi/awmcam/ssh_rev_tunnel.sh -cloud_ip='+CLOUD_IP+' -cloud_user='+CLOUD_USER+' -cloud_port='+REMOTE_SSH_PORT+' -local_port=22"')
os.system('screen -dmS sshweb bash -c "/home/pi/awmcam/ssh_rev_tunnel.sh -cloud_ip='+CLOUD_IP+' -cloud_user='+CLOUD_USER+' -cloud_port='+REMOTE_CAM_PORT+' -local_port=8080"')
os.system('screen -dmS sshmav bash -c "/home/pi/awmcam/ssh_rev_tunnel.sh -cloud_ip='+CLOUD_IP+' -cloud_user='+CLOUD_USER+' -cloud_port='+REMOTE_MAV_PORT+' -local_port=MAV_DRONEKIT"')
os.system('screen -dmS mav bash -c "/home/pi/awmcam/mavproxy.sh -m '+MAV_MASTER+' -p '+MAV_DRONEKIT+' -b '+MAV_BAUD+'"')
#os.system('screen -dmS web bash -c "python3 /home/pi/awmcam/webhello.py --port 8080"')
os.system('screen -dmS web bash -c "python3 /home/pi/awmcam/webcam.py --port 8080"')

class cam():
    def __init__(self,stream=None):
        self.picam2 = Picamera2()
        self.video_config = self.picam2.create_video_configuration(main={"size": (800, 600)})
        self.picam2.configure(self.video_config)

        # self.encoder = MJPEGEncoder()
        self.encoder = H264Encoder(10000000)
        self.webstream = stream
        #self.output1 = FileOutput(self.webstream)
        self.output1 = FfmpegOutput("-f mpegts udp://127.0.0.1:8081")
        # self.output1 = FfmpegOutput("-f hls -hls_time 4 -hls_list_size 5 -hls_flags delete_segments -hls_allow_cache 0 stream.m3u8")

        self.output2 = FileOutput('test.mjpeg')
        self.encoder.output = [self.output1, self.output2]
        # self.encoder.output = self.output1

    def start_stream(self):
        print("start_stream")
        self.picam2.start_encoder(self.encoder)
        self.picam2.start()

    def stop_stream(self):
        print("stop_stream")
        self.picam2.stop_encoder(self.encoder)
        self.picam2.stop()

    def start_file(self):
        pass

wserver = webcamserver(host="localhost", port=8080)
wserver.start() #Thread

pcam = cam(wserver.streamout)
# pcam = cam()
pcam.start_stream()
time.sleep(20)
pcam.stop_stream()

print("stop wserver")
wserver.stop() #Thread
wserver.join()

