#!/bin/sh
set -x
sudo mount -o uid=pi,gid=pi /dev/sda1 ~/usb/
sudo cp test*.* ~/usb
sudo ls -l ~/usb
sudo umount ~/usb