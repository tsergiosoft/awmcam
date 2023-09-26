from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import glob
import numpy as np
import time
import configparser
import os
from webcam import webcamserver

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
glob.PICAM	    =int(config['DEFAULT']['PICAM'])

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

server = webcamserver('', 8080)
server.start()
frame_size = (800, 600)

# if (glob.PICAM==0):
#     server.start_stream()
#     while True:
#          buffer = np.random.randint(0, 255, size=(800, 600, 3), dtype=np.uint8)
#          _,jpeg_data = cv2.imencode('.jpg', buffer, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
#          server.output.write(jpeg_data)
#          time.sleep(1.0 / 12)

server.start_stream()
time.sleep(10)
# webcamserver.output2.fileoutput = "test.h264"
webcamserver.output2.start()
time.sleep(5)
webcamserver.output2.stop()
time.sleep(5)
# server.stop_stream()
# time.sleep(5)
# server.start_stream()
# time.sleep(15)
# server.stop_stream()

# try:
#     webcamserver.join()
# except:
#     pass

# if (PICAM):
#     picam2 = Picamera2()
#     picam2.configure(picam2.create_video_configuration(main={"size": (800, 600)}))
#     output = webcamserver.StreamingOutput()
#     picam2.start_recording(JpegEncoder(), FileOutput(output))

# try:
#     address = ('', 8080)
#     print("WEB PICAMERA HQ http://host:"+REMOTE_CAM_PORT)
#     server = webcam.StreamingServer(address, webcam.StreamingHandler)
#     server.serve_forever()
# finally:
#     picam2.stop_recording()


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
    

