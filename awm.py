#!/usr/bin/python3

import time, os, platform
import configparser
#from websrv_mjpeg import webserverjpg
from websrv_flask import webserverjpg
from camera import cam
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import cv2
from kamik import Kamikaze

class Awm():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('params.ini')
        self.TALON_SN	=self.config['DEFAULT']['SN']
        self.CLOUD_IP	=self.config['DEFAULT']['CLOUD_IP']
        self.CLOUD_USER	=self.config['DEFAULT']['CLOUD_USER']
        self.REMOTE_SSH_PORT =self.config['DEFAULT']['REMOTE_SSH_PORT']
        self.REMOTE_CAM_PORT =self.config['DEFAULT']['REMOTE_CAM_PORT']
        self.REMOTE_MAV_PORT =self.config['DEFAULT']['REMOTE_MAV_PORT']
        self.MAV_MASTER	=self.config['DEFAULT']['MAV_MASTER']
        self.MAV_BAUD	=self.config['DEFAULT']['MAV_BAUD']
        self.MAV_USE = int(self.config['DEFAULT']['MAV_USE'])
        #MAVPROXY_IP_PORT=config['DEFAULT']['MAVPROXY_IP_PORT'] #may be delete and use 127.0.0.1:14550
        self.MAV_DRONEKIT=self.config['DEFAULT']['MAV_DRONEKIT']
        self.CAM_EXISTS =int(self.config['DEFAULT']['CAM_EXISTS'])
        self.HQ_CAM =int(self.config['DEFAULT']['HQ_CAM'])
        self.USB_CAM =int(self.config['DEFAULT']['USB_CAM'])

        print("TALON_SN="+self.TALON_SN+" CLOUD_IP="+self.CLOUD_IP)
        #os.system('pkill screen')
        #os.system('screen -S awm -X kill') #SELF KILLER!!!!
        self.current_platform = platform.system()
        print(f"Running on {self.current_platform}")
        self.closing = False
        if self.current_platform == 'Linux':
            os.system('screen -S ssh22 -X kill')
            os.system('screen -S sshweb -X kill')
            os.system('screen -S sshmav -X kill')
            os.system('screen -S mav -X kill')
            os.system('screen -S usbcam -X kill')
            os.system('sudo ~/awmcam/service/usb_remove.sh')
            time.sleep(1)
            os.system('sudo ~/awmcam/service/usb_add.sh')

            if self.MAV_USE:
                os.system('screen -dmS mav bash -c "/home/j/awmcam/service/mavproxy.sh -m '+self.MAV_MASTER+' -p '+self.MAV_DRONEKIT+' -b '+self.MAV_BAUD+'"')
            
            #os.system('screen -dmS ssh22 bash -c "/home/j/awmcam/service/ssh_rev_tunnel.sh -cloud_ip='+CLOUD_IP+' -cloud_user='+CLOUD_USER+' -cloud_port='+REMOTE_SSH_PORT+' -local_port=22"')
            #os.system('screen -dmS sshweb bash -c "/home/j/awmcam/service/ssh_rev_tunnel.sh -cloud_ip='+CLOUD_IP+' -cloud_user='+CLOUD_USER+' -cloud_port='+REMOTE_CAM_PORT+' -local_port=8080"')
            #os.system('screen -dmS sshmav bash -c "/home/j/awmcam/service/ssh_rev_tunnel.sh -cloud_ip='+CLOUD_IP+' -cloud_user='+CLOUD_USER+' -cloud_port='+REMOTE_MAV_PORT+' -local_port=14550"')
            # if HQ_CAM == 0: #mjpeg_streamer variance
            #     os.system('screen -dmS usbcam bash -c "/home/j/awmcam/service/cam_run.sh"')

        self.wserver = None
        self.wserver = webserverjpg(host="0.0.0.0", port=8080)
        self.wserver.start()  # Thread
        self.pcam = None
        self.pcam = cam(stream=self.wserver.streamout, cam_exist=bool(self.CAM_EXISTS), usb_cam=bool(self.USB_CAM))
        self.pcam.start_stream(webbitrate=4000000)
        if self.MAV_USE:
            self.kamik = Kamikaze(conn=self.MAV_DRONEKIT, paused=False)
            self.kamik.start()
        print("AWM APP STARTED")


    def old_ardupilot(self):
        LinkOK = False
        print("try MAV_DRONEKIT connect")
        # vehicle = connect(MAV_DRONEKIT,baud=MAV_BAUD, wait_ready=True, heartbeat_timeout=100,timeout=100)
        vehicle = connect(self.MAV_DRONEKIT, wait_ready=False, timeout=3, heartbeat_timeout=3, baud=921600)

        @vehicle.on_attribute('last_heartbeat')
        def listener(self, attr_name, value):
            global LinkOK
            if value > 3 and LinkOK:
                print("Pausing script due to bad link")
                LinkOK = False;
            if value < 1 and not LinkOK:
                print("LinkOK")
                LinkOK = True;

        # while True:
        #     time.sleep(1)
        #     info1 = "Loc:[%s, %s] alt %s" % (
        #     vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, vehicle.location.global_frame.alt)
        #     info1 = info1 + " GPS: fix=%s, vis=%s" % (vehicle.gps_0.fix_type, vehicle.gps_0.satellites_visible)
        #     print(info1)
        #
        #     # VID_ON = int(vehicle.parameters['VID_ON'])
        #     # VID_TIME = int(vehicle.parameters['VID_TIME'])
        #     # VID_WEB_MODE = int(vehicle.parameters['VID_WEB_MODE'])
        #     # info2 = "file:"+str(pcam.fileout_on)+" "+"VID_ON=%s VID_TIME=%s VID_WEB_MODE=%s" % (VID_ON,VID_TIME,VID_WEB_MODE)
        #     # print(info2)
        #     pcam.info1 = info1
        #     # pcam.info2 = info2
        #     # try:
        #     #    if (VID_ON):
        #     #        pcam.start_file()
        #     #    else:
        #     #        pcam.stop_file()
        #     # except:
        #     #    print("Exception if file output")
        #
        #     # try:
        #     #    if (VID_WEB_MODE>0):
        #     #        pcam.start_stream(webbitrate=VID_WEB_MODE*1000000)
        #     #    else:
        #     #        pcam.stop_stream()
        #     # except:
        #     #    print("Exception if WEB output")

    def run(self):
        if not self.pcam.cam_exist:
            current_path = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(current_path, "camsimul", "logo.jpg")
            # print(logo_path)
            frame_home = cv2.imread(logo_path)

            if self.USB_CAM:
                self.video_capture = cv2.VideoCapture(0)

        while True:
            try:
                if self.MAV_USE:
                    self.pcam.info1 = "Loc:[%s, %s] alt %s" % (
                        self.kamik.vehicle.location.global_frame.lat, self.kamik.vehicle.location.global_frame.lon,
                        self.kamik.vehicle.location.global_frame.alt)
                    self.pcam.info1 = self.pcam.info1 + " GPS: fix=%s, vis=%s" % (self.kamik.vehicle.gps_0.fix_type,
                                                                                  self.kamik.vehicle.gps_0.satellites_visible)
                if self.USB_CAM:
                    result, video_frame = self.video_capture.read()  # read frames from the video
                    if result is False:
                        print("\033[91m" + "Exception video_capture.read" + "\033[0m")
                        break
                    else:
                        self.pcam.apply_timestamp(video_frame)
                        self.wserver.streamout.write(buf=video_frame)
                else:
                    frame = frame_home.copy()
                    self.pcam.apply_timestamp(frame)
                    self.wserver.streamout.write(buf=frame)
                    time.sleep(0.05)
            except:
                print("\033[91m" + "Exception in run" + "\033[0m")
                time.sleep(2)

if __name__ == "__main__":
    try:
        my_app = Awm()
        my_app.run()
    finally:
        # Stop the thread and wait for it to finish
        print("\033[91m" + "AWM END:((" + "\033[0m")