#!/bin/bash
screen -S mavproxy -d -m bash -c "/home/pi/awm/mavproxy_run.sh"
screen -S cam -d -m bash -c "/home/pi/awm/cam_run.sh"
screen -S sshcam -d -m bash -c "/home/pi/awm/ssh_cam.sh"
screen -S sshmav -d -m bash -c "/home/pi/awm/ssh_mav.sh"
screen -S ssh22 -d -m bash -c "/home/pi/awm/ssh_22.sh"
while true ; do sleep 120; done

