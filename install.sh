#!/bin/sh

HOME=/home/pi
echo "home folder is"=$HOME
echo "----------SSH copy"
mkdir $HOME/.ssh
mkdir $HOME/mavlogs
cp -R $HOME/awmcam/ssh/* $HOME/.ssh
sudo chmod -R 400 $HOME/.ssh
sudo chmod 755 $HOME/.ssh
sudo ssh-copy-id -i ~/.ssh/tunkey.pub pi@127.0.0.1 
echo "----------apt update"
#sudo apt update
#sudo apt upgrade
echo "----------Install netcat"
#sudo sudo apt-get install ncat -y
echo "----------Install screen"
#sudo apt-get install screen -y
echo "----------Remove modemmanager"
#sudo apt-get remove modemmanager -y
echo "----------Install pip3"
#sudo apt-get install python3-pip -y
echo "----------Install MAVProxy"
#sudo pip install MAVProxy
echo "----------Install dronekit"
#sudo pip install dronekit
echo "----------Install ZeroTier"
#curl -s https://install.zerotier.com | sudo bash
#sudo zerotier-cli join 1d71939404a9b1e4
echo "--------Install ffmpeg"
sudo apt-get install ffmpeg

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
#https://github.com/mustafa-gokce/ardupilot-software-development/blob/main/mavproxy/automated-forwarding-services.md
sudo cp $HOME/awmcam/service/awm.service /etc/systemd/system
sudo systemctl enable awm.service
echo "----------Start service mav"
sudo systemctl start awm.service
echo "----------Install finish OK"
echo "--------------------------------------------END----------------------------------------------"

 
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

