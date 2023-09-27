#!/bin/sh
#[all]
#camera_auto_detect=0
#dtoverlay=imx477,media-controller=0
#gpu_mem=256
#dtoverlay=vc4-kms-v3d

HOME=/home/pi
echo "home folder is"=$HOME
echo "----------SSH copy"
mkdir $HOME/.ssh
mkdir $HOME/mavlogs
cp -R $HOME/awmcam/ssh/* $HOME/.ssh
sudo chmod -R 400 $HOME/.ssh
sudo chmod 755 $HOME/.ssh
chmod 600 $HOME/.ssh/known_hosts
sudo ssh-copy-id -i ~/.ssh/tunkey.pub pi@127.0.0.1
#echo "----------apt update"
#sudo apt update
#sudo apt upgrade
#echo "----------Install netcat"
#sudo sudo apt-get install ncat -y
#echo "----------Install screen"
#sudo apt-get install screen -y
#echo "----------Remove modemmanager"
#sudo apt-get remove modemmanager -y
#echo "----------Install pip3"
#sudo apt-get install python3-pip -y
#echo "----------Install MAVProxy"
#sudo pip install MAVProxy
#echo "----------Install dronekit"
#sudo pip install dronekit
#echo "----------Install ZeroTier"
#curl -s https://install.zerotier.com | sudo bash
#sudo zerotier-cli join 1d71939404a9b1e4


#echo "--------Install ffmpeg"
#sudo apt-get install ffmpeg

#cd $HOME
#git clone https://github.com/jacksonliam/mjpg-streamer.git
#git clone https://github.com/tsergiosoft/mjpg-streamer.git
#sudo apt-get install cmake -y
##sudo apt-get install libjpeg8-dev -y
#sudo apt-get install libjpeg62-turbo-dev -y
#sudo apt-get install gcc g++ -y
#sudo apt-get install cmake
#cd $HOME/mjpg-streamer/mjpg-streamer-experimental
#make
#sudo make install

echo "----------Create service mav"
sudo cp $HOME/awmcam/service/awm.service /etc/systemd/system
sudo systemctl enable awm.service
echo "----------Start service mav"
sudo systemctl start awm.service
echo "----------Install finish OK"
echo -------------First ssh connect to cloud...
echo DO COMMAND sudo ssh -v -i ~/.ssh/tunaws.pem ubuntu@13.50.210.14 -p 22
echo "--------------------------------------------END----------------------------------------------"

#raspivid -t 0 -s -b 987654 -sg 5000 -o -|tee ~/video1.h264 | cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8160}' :demux=h264
#
#raspivid -o - -t 0 -hf -w 800 -h 600 -fps 12 |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8160}' :demux=h264
#raspivid -t 0 -w 640 -h 480  -b 987654 -sg 5000 -o ~/video%03d.h264 | cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8160}' :demux=h264
#raspivid -t 0 -w 640 -h 480  -b 200000 -sg 5000 -wr 20 -o ~/test%03d.h264 | gst-launch-1.0 -v fdsrc !  h264parse ! gdppay ! udpsink host=127.0.0.1 port=8160
#raspivid -t 0 -w 640 -h 480  -b 200000 -sg 5000 -wr 20 -o ~/test%03d.h264 | gst-launch-1.0 -v fdsrc !  decodebin ! x264enc ! rtph264pay config-interval=1 pt=96 ! udpsink host=127.0.0.1 port=8160
#gst-launch-1.0 filesrc location=C:/Users/me/Desktop/big_buck_bunny.mp4 ! decodebin ! x264enc ! rtph264pay config-interval=1 pt=96 ! udpsink port=1234
#raspivid -t 0 | gst-launch-1.0 -v fdsrc ! video/x-raw,width=640,height=480,framerate=24/1 ! x264enc key-int-max=30 insert-vui=1 tune=zerolatency ! h264parse config-interval=1 ! mpegtsmux ! rtpmp2tpay ! udpsink host=127.0.0.1 port=8160
#raspivid -n -w 1280 -h 720 -fps 24 -b 4500000 -a 12 -t 0 -o - | gst-launch-1.0 -v fdsrc ! video/x-h264, width=1280, height=720, framerate=24/1 ! h264parse config-interval=1 ! mpegtsmux ! rtpmp2tpay ! udpsink host=127.0.0.1 port=8160
#raspivid -n -w 640 -h 480 -fps 24 -b 4500000 -a 12 -t 0 -o - | gst-launch-1.0 -v fdsrc ! video/x-h264, width=640, height=480, framerate=24/1 ! h264parse config-interval=-1 ! mpegtsmux ! udpsink host=127.0.0.1 port=8160


#on AWS\Google -> sudo nano /etc/ssh/sshd_config -> GatewayEnable yes ClientAliveInterval 15 ClientAliveCountMax 2

# Mission Planner -> Video->SetMJPEG source -> http://13.50.210.14:5000/?action=stream
#
# Connect from any to Raspi via SSh
# USER --pi---!!!!!
# ssh pi@13.50.210.14 -v -i C:\Users\Tarasenko_S\.ssh\tunaws.pem -p 5022
# Connect from AWS to Raspi via SSh
# ssh pi@13.50.210.14 -v -i ~\.ssh\authorized_keys -p 5022


####   Raspberry Pi   ############################
#sudo raspi-config -> serial port enable, (autologin pi)
#$ git clone https://github.com/tsergiosoft/arp.git
#$ cd arp
#$ ./install.sh
# git pull origin main

#/boot/config.txt entries to disable both Bluetooth and WiFi.
#dtoverlay=disable-bt
#dtoverlay=imx477 ##FOR HQ Camera 

################################
#on GitHub create repo tsergiosoft/arp.git
#$ git clone git@github.com:tsergiosoft/arp.git
#$ git config alias.acp '! git add . && git commit -a -m "commit" && git push'
#	Usage!!!!: git acp

#ssh-keygen -t ed25519 -C "sergtarasenko76@gmail.com"
# .git\config [alias]	acp = ! git add . && git commit -a -m \"commit\" && git push
# chmod 400 ~/.ssh/id_rsa
# ssh-add

#sudo nano /etc/wpa_supplicant/wpa_supplicant.conf


#sudo nano ./wpa_supplicant/wpa_supplicant.conf 
#ON Cygwin ./tools/autotest/sim_vehicle.py -v ArduPlane -N -L KSFO --map --console --out 192.168.14.225:14550
#-------------------------
#put line to /etc/rc.local for autorun: 
#sudo sed -i "\$i sh ~/arp/mavrun.sh &" /etc/rc.local
#sudo chmod +x /etc/rc.local
#sudo systemctl enable rc-local.service
#sudo nano /etc/rc.local

