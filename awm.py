#!/usr/bin/python3

import time, os
import configparser
from websrv_mjpeg import webserverjpg
from camera import cam
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

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
CAM_EXISTS =int(config['DEFAULT']['CAM_EXISTS'])

print("TALON_SN="+TALON_SN+" CLOUD_IP="+CLOUD_IP)
#os.system('pkill screen')
#os.system('screen -S awm -X kill') #SELF KILLER!!!!

os.system('screen -S ssh22 -X kill')
os.system('screen -S sshweb -X kill')
os.system('screen -S sshmav -X kill')
os.system('screen -S mav -X kill')
#os.system('screen -S web -X kill')
time.sleep(1)
os.system('screen -dmS ssh22 bash -c "/home/pi/awmcam/ssh_rev_tunnel.sh -cloud_ip='+CLOUD_IP+' -cloud_user='+CLOUD_USER+' -cloud_port='+REMOTE_SSH_PORT+' -local_port=22"')
os.system('screen -dmS sshweb bash -c "/home/pi/awmcam/ssh_rev_tunnel.sh -cloud_ip='+CLOUD_IP+' -cloud_user='+CLOUD_USER+' -cloud_port='+REMOTE_CAM_PORT+' -local_port=8080"')
os.system('screen -dmS sshmav bash -c "/home/pi/awmcam/ssh_rev_tunnel.sh -cloud_ip='+CLOUD_IP+' -cloud_user='+CLOUD_USER+' -cloud_port='+REMOTE_MAV_PORT+' -local_port=14550"')
os.system('screen -dmS mav bash -c "/home/pi/awmcam/mavproxy.sh -m '+MAV_MASTER+' -p '+MAV_DRONEKIT+' -b '+MAV_BAUD+'"')

wserver = webserverjpg(host="localhost", port=8080)
wserver.start() #Thread

pcam = cam(stream=wserver.streamout, cam_exist=bool(CAM_EXISTS))

pcam.start_stream(webbitrate=40000000)

# while True:
#     time.sleep(10)
#     print('Streaming...')

# print("stop wserver")
# wserver.stop() #Thread
# wserver.join()


LinkOK=False
vehicle = connect(MAV_DRONEKIT,baud=MAV_BAUD, wait_ready=True, heartbeat_timeout=100,timeout=100)
@vehicle.on_attribute('last_heartbeat')
def listener(self, attr_name, value):
    global LinkOK
    if value > 3 and LinkOK:
        print("Pausing script due to bad link")
        LinkOK=False;
    if value < 1 and not LinkOK:
        print("LinkOK")
        LinkOK=True;

while True:
    time.sleep(2)
    info1 = "Loc:[%s, %s] alt %s" % (vehicle.location.global_frame.lat,vehicle.location.global_frame.lon,vehicle.location.global_frame.alt)
    info1 = info1 +" GPS: fix=%s, vis=%s" % (vehicle.gps_0.fix_type, vehicle.gps_0.satellites_visible)
    # print(info)
    VID_ON = int(vehicle.parameters['VID_ON'])
    VID_TIME = int(vehicle.parameters['VID_TIME'])
    VID_WEB_MODE = int(vehicle.parameters['VID_WEB_MODE'])
    info2 = "VID_ON=%s VID_TIME=%s VID_WEB_MODE=%s" % (VID_ON,VID_TIME,VID_WEB_MODE)
    # print(info2)
    pcam.info1 = info1
    pcam.info2 = info2
    if (VID_ON):
        pcam.start_file()
    else:
        pcam.stop_file()

    if (VID_WEB_MODE==1):
        pcam.start_stream(webbitrate=VID_WEB_MODE*1000000)
    else:
        pcam.stop_stream()
    # print(LinkOK)
    # print("Alt="+str(vehicle.location.global_relative_frame.alt))
    # print(vehicle.parameters['VID_WEB_MODE'])
    # print(vehicle.mode.name)
    # print("Loc:[%s, %s] alt %s" % (vehicle.location.global_frame.lat,vehicle.location.global_frame.lon,vehicle.location.global_frame.alt))
    # print(" Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
    # print(" Local Location: %s" % vehicle.location.local_frame)
    # print(" Attitude: %s" % vehicle.attitude)
    # print(" Velocity: %s" % vehicle.velocity)
    # print(" GPS: fix=%s, vis=%s" % (vehicle.gps_0.fix_type, vehicle.gps_0.satellites_visible))
    # print(" Gimbal status: %s" % vehicle.gimbal)
    # print(" Battery: %s" % vehicle.battery)
    # print(" EKF OK?: %s" % vehicle.ekf_ok)
    # print(" Last Heartbeat: %s" % vehicle.last_heartbeat)
    # print(" Heading: %s" % vehicle.heading)
    # print(" Is Armable?: %s" % vehicle.is_armable)
    # print(" System status: %s" % vehicle.system_status.state)
    # print(" Groundspeed: %s" % vehicle.groundspeed)  # settable
    # print(" Airspeed: %s" % vehicle.airspeed)  # settable
    # print(" Mode: %s" % vehicle.mode.name)  # settable
    # print(" Armed: %s" % vehicle.armed)  # settable

