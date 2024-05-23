#!/bin/bash
screen -dmS awm bash -c "sleep 1;cd /home/j/awmcam;python3 /home/j/awmcam/awm.py"

#screen -dmS cam bash -c "sleep 2;python3 /home/j/awmcam/pyhello.py"
##### temp - call from dk!!!
#screen -S sshcam -d -m bash -c "/home/j/awmcam/ssh/sshweb.sh"
#screen -S ssh22 -d -m bash -c "/home/j/awmcam/ssh22.sh"
#screen -S mavproxy -d -m bash -c "/home/j/awmcam/mavproxy_run.sh"
#screen -S cam -d -m bash -c "/home/j/awmcam/cam_run.sh"
#screen -S sshmav -d -m bash -c "/home/j/awmcam/ssh_mav.sh"

while true ; do sleep 120; done

