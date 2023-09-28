#!/usr/bin/python3

import time, os
import configparser
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
NO_CAM =int(config['DEFAULT']['NO_CAM'])
REMOTE_SIM_PORT = config['DEFAULT']['REMOTE_SIM_PORT']
SIM_PORT = config['DEFAULT']['SIM_PORT']

print("TALON_SN="+TALON_SN+" CLOUD_IP="+CLOUD_IP)
#os.system('pkill screen')
#os.system('screen -S awm -X kill') #SELF KILLER!!!!

os.system('screen -S ssh22 -X kill')
os.system('screen -S sshweb -X kill')
os.system('screen -S sshmav -X kill')
os.system('screen -S mav -X kill')
os.system('screen -S web -X kill')
#os.system('screen -S sshsim -X kill')
time.sleep(1)
os.system('screen -dmS ssh22 bash -c "/home/pi/awmcam/ssh_rev_tunnel.sh -cloud_ip='+CLOUD_IP+' -cloud_user='+CLOUD_USER+' -cloud_port='+REMOTE_SSH_PORT+' -local_port=22"')
os.system('screen -dmS sshweb bash -c "/home/pi/awmcam/ssh_rev_tunnel.sh -cloud_ip='+CLOUD_IP+' -cloud_user='+CLOUD_USER+' -cloud_port='+REMOTE_CAM_PORT+' -local_port=8080"')
os.system('screen -dmS sshmav bash -c "/home/pi/awmcam/ssh_rev_tunnel.sh -cloud_ip='+CLOUD_IP+' -cloud_user='+CLOUD_USER+' -cloud_port='+REMOTE_MAV_PORT+' -local_port=14550"')
os.system('screen -dmS mav bash -c "/home/pi/awmcam/mavproxy.sh -m '+MAV_MASTER+' -p '+MAV_DRONEKIT+' -b '+MAV_BAUD+'"')

#os.system('screen -dmS sshsim bash -c "/home/pi/awmcam/ssh_rev_tunnel.sh -cloud_ip='+CLOUD_IP+' -cloud_user='+CLOUD_USER+' -cloud_port='+REMOTE_SIM_PORT+' -local_port='+SIM_PORT+'"')

wserver = webserverjpg(host="localhost", port=8080)
wserver.start() #Thread

if (not NO_CAM):
    pcam = cam(wserver.streamout)

if (not NO_CAM):
    pcam.start_stream()
    time.sleep(300)
    pcam.stop_stream()

print("stop wserver")
wserver.stop() #Thread
wserver.join()


# LinkOK=False
# vehicle = connect(MAV_DRONEKIT,baud=MAV_BAUD, wait_ready=True, heartbeat_timeout=100,timeout=100)
# @vehicle.on_attribute('last_heartbeat')
# def listener(self, attr_name, value):
#     global LinkOK
#     if value > 3 and LinkOK:
#         print("Pausing script due to bad link")
#         LinkOK=False;
#     if value < 1 and not LinkOK:
#         LinkOK=True;
#
# while True:
#     time.sleep(2)
#     print(LinkOK)
#     print(vehicle.parameters['AFS_ENABLE'])
#     #print(vehicle.mode.name)

