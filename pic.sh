#!/bin/bash

echo "rebuild camera..."
cd ~/picamera2
git pull
sudo python3 setup.py install
cd ~/awmcam/
git pull
python3 awm.py