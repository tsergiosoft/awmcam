#!/bin/bash
screen -dmS awm bash -c "sleep 1;cd /home/pi/awmcam;python3 /home/pi/awmcam/awm.py"
#screen -dmS cam bash -c "sleep 2;python3 /home/pi/awmcam/pyhello.py"
##### temp - call from dk!!!
#screen -S sshcam -d -m bash -c "/home/pi/awmcam/ssh/sshweb.sh"
#screen -S ssh22 -d -m bash -c "/home/pi/awm/ssh22.sh"
#screen -S mavproxy -d -m bash -c "/home/pi/awm/mavproxy_run.sh"
#screen -S cam -d -m bash -c "/home/pi/awm/cam_run.sh"
#screen -S sshmav -d -m bash -c "/home/pi/awm/ssh_mav.sh"

while true ; do sleep 120; done

