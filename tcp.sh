#!/bin/sh
sudo mount -o uid=pi,gid=pi /dev/sda1 ~/usb/
sudo cp test*.* ~/usb
sudo umount ~/usb