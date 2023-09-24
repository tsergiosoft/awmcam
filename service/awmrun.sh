#!/bin/bash
screen -S ssh22 -d -m bash -c "/home/pi/awmcam/ssh/ssh_22.sh"


#screen -S mavproxy -d -m bash -c "/home/pi/awmcam/mavproxy_run.sh"
#screen -S cam -d -m bash -c "/home/pi/awmcam/cam_run.sh"
#screen -S sshmav -d -m bash -c "/home/pi/awmcam/ssh_mav.sh"

screen -dmS pystream python3 /home/pi/awmcam/pystream.py
screen -S sshcam -d -m bash -c "/home/pi/awmcam/ssh_cam.sh"

while true ; do sleep 120; done

