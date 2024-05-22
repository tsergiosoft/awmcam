#sudo nano /etc/ssh/sshd_config 
#PubkeyAuthentication yes
#FOR Totalcommander comment
##PasswordAuthentication no

####   Raspberry Pi   ############################
#sudo raspi-config -> serial port enable, (autologin pi)
#$ git clone https://github.com/tsergiosoft/awmcam.git
#$ cd awmcam
#$ ./install.sh
# git pull origin main

#!/bin/sh
set -x

HOME=/home/j
echo "home folder is"=$HOME

#https://unix.stackexchange.com/questions/681379/usb-flash-drives-automatically-mounted-headless-computer
#sudo cp $HOME/awmcam/service/usb-mount@.service /etc/systemd/system/
#sudo cp $HOME/awmcam/service/99-local.rules /etc/udev/rules.d/
#sudo udevadm control --reload-rules
#sudo systemctl daemon-reload
####journalctl -xe

#echo "----------Remove Bluetooth service"
#sudo systemctl disable hciuart.service
#sudo systemctl disable bluealsa.service
#sudo systemctl disable bluetooth.service
#sudo apt-get purge bluez -y
#sudo apt-get autoremove -y
#
#sudo cp $HOME/awmcam/service/config.txt /boot/
#
#echo "----------SSH copy"
#mkdir $HOME/.ssh
#mkdir $HOME/mavlogs
#cp -R $HOME/awmcam/ssh/* $HOME/.ssh
#sudo chmod -R 400 $HOME/.ssh
#sudo chmod 755 $HOME/.ssh
#chmod 600 $HOME/.ssh/known_hosts
#sudo ssh-copy-id -i ~/.ssh/tunkey.pub pi@127.0.0.1
#echo "----------apt update"
##sudo apt update
##sudo apt upgrade
#echo "----------Install netcat"
#sudo apt-get install ncat -y
#echo "----------Install screen"
#sudo apt-get install screen -y
#echo "----------Remove modemmanager"
#sudo apt-get remove modemmanager -y
#echo "----------Install pip3"
#sudo apt-get install python3-pip -y
#echo "----------Install OpenCV"
#sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 python3-pyqt5 python3-dev -y
#sudo apt install python3-opencv
#
#echo "----------Install MAVProxy"
#sudo pip install MAVProxy
#echo "----------Install dronekit"
#sudo pip install dronekit
#echo "----------Install ZeroTier"
#curl -s https://install.zerotier.com | sudo bash
#sudo zerotier-cli join 1d71939404a9b1e4
#
#echo "----------Create service mav"
#sudo cp $HOME/awmcam/service/awm.service /etc/systemd/system
#sudo systemctl enable awm.service
#echo "----------Start service mav"
#sudo systemctl start awm.service
#echo "----------Install finish OK"
#echo -------------First ssh connect to cloud...
#echo "--------------------------------------------END----------------------------------------------"
#echo ................... execute test connect:
#echo ................... sudo ssh -v -i ~/.ssh/tunaws.pem ubuntu@13.50.210.14 -p 22

#????????pip install -U numpy

#on AWS\Google ->
# sudo nano /etc/ssh/sshd_config
#GatewayEnable yes ClientAliveInterval 15 ClientAliveCountMax 2
#AllowTcpForwarding yes
#GatewayPorts yes

##### for USB camera only
cd $HOME
#---------git clone https://github.com/jacksonliam/mjpg-streamer.git
git clone https://github.com/tsergiosoft/mjpg-streamer.git
sudo apt-get install cmake -y
#-----sudo apt-get install libjpeg8-dev -y
sudo apt-get install libjpeg62-turbo-dev -y
sudo apt-get install gcc g++ -y
sudo apt-get install cmake
cd $HOME/mjpg-streamer/mjpg-streamer-experimental
make
sudo make install
### Mission Planner -> Video->SetMJPEG source -> http://13.50.210.14:5000/?action=stream


#sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

#netstat -tuln