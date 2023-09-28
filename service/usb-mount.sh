#!/bin/bash

USB_DIR="/mnt/usb"
#USB_DEV="/dev/sda1"  # Replace with the actual device path
USB_DEV=$1
echo "execute Action:$1 for:$2"
if [ -e "$USB_DEV" ]; then
    echo "USB drive detected. Mounting..."
    sudo mount "$USB_DEV" "$USB_DIR"
    echo "USB drive mounted."
else
    echo "USB drive not detected."
    if mount | grep -q "$USB_DIR"; then
        echo "Unmounting USB drive..."
        sudo umount "$USB_DIR"
        echo "USB drive unmounted."
    fi
fi
