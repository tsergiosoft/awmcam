from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import configparser
import os

#import argparse  
#parser = argparse.ArgumentParser()
#parser.add_argument('--connect', default='127.0.0.1:5160')

#args = parser.parse_args()
      
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
MAV_DRONEKIT	=config['DEFAULT']['MAV_DRONEKIT']
print("TALON_SN="+TALON_SN+" CLOUD_IP="+CLOUD_IP)

#os.system('pkill screen')
#os.system('screen -S awm -X kill') #SELF KILLER!!!!

os.system('screen -S mavproxy -X kill')
os.system('screen -S ssh22 -X kill')
os.system('screen -S web -X kill')
time.sleep(1)
os.system('screen -S ssh22 -d -m bash -c "/home/pi/awmcam/ssh/ssh22.sh -cloud_ip='+CLOUD_IP+' -cloud_user='+CLOUD_USER+' -cloud_port='+REMOTE_SSH_PORT+'"')
os.system('screen -S mavproxy -d -m bash -c "/home/pi/awmcam/mavproxy.sh -m '+MAV_MASTER+' -p '+MAV_DRONEKIT+' -b '+MAV_BAUD+'"')
#os.system('screen -dmS web bash -c "sleep 2;python3 /home/pi/awmcam/webhello.py --port 8080"')
os.system('screen -dmS web bash -c "sleep 2;python3 /home/pi/awmcam/webcam.py --port 8080"')

LinkOK=False
vehicle = connect(MAV_DRONEKIT,baud=MAV_BAUD, wait_ready=True, heartbeat_timeout=100,timeout=100)
@vehicle.on_attribute('last_heartbeat')
def listener(self, attr_name, value):
    global LinkOK
    if value > 3 and LinkOK:
        print("Pausing script due to bad link")
        LinkOK=False;
    if value < 1 and not LinkOK:
        LinkOK=True;

while True:
    time.sleep(2)
    print(LinkOK)
    print(vehicle.parameters['AFS_ENABLE'])
    #print(vehicle.mode.name)
    
print ('Connecting ON')
# Function to arm and then takeoff to a user specified altitude
def arm_and_takeoff(aTargetAltitude):

  print("Basic pre-arm checks")
  # Don't let the user try to arm until autopilot is ready
  while not vehicle.is_armable:
    print (" Waiting for vehicle to initialise...")
    time.sleep(1)
        
  print("Arming motors")
  # Copter should arm in GUIDED mode
  vehicle.mode    = VehicleMode("GUIDED")
  vehicle.armed   = True

  while not vehicle.armed:
    print(" Waiting for arming...")
    time.sleep(1)

  print("Taking off!")
  vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

  # Check that vehicle has reached takeoff altitude
  while True:
    #print (" Altitude: ", vehicle.location.global_relative_frame.alt)
    #Break and return from function just below target altitude.        
    if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
      print ("Reached target altitude")
      break
    time.sleep(1)

# Initialize the takeoff sequence to 20m
arm_and_takeoff(20)

print("Take off complete")

# Hover for 10 seconds
time.sleep(10)

print("Now let's land")
vehicle.mode = VehicleMode("LAND")

# Close vehicle object
vehicle.close()
