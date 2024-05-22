#!/bin/bash

#mavproxy.py --master=192.168.14.225:14550 --baudrate 921600 --state-basedir=/home/pi/mavlogs --out=tcpin:127.0.0.1:14550 --out=udp:127.0.0.1:5760 --out=udp:127.0.0.1:5678
#mavproxy.py --master=/dev/ttyAMA0 --baudrate 115200 --state-basedir=/home/pi/mavlogs --out=tcpin:127.0.0.1:14550 --out=udp:127.0.0.1:5760 --out=udp:127.0.0.1:5560

export LOCALAPPDATA="LOCALAPPDATA"

# Default values
master="/dev/serial0"
#master="192.168.14.225:14550" #local Windows simulator
dronekit="udp:127.0.0.1:5888"
baud="115200"

while getopts ":m:p:b:" opt; do
  case $opt in
    m)
      master="$OPTARG"
      ;;
    p)
      dronekit="$OPTARG"
      ;;
    b)
      baud="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Shift the positional arguments to the end
shift $((OPTIND-1))

set -x #echo on
while true; do
	#--state-basedir="~/mavlogs"
	#--force-connected
	#--out=udp:127.0.0.1:5777
	mavproxy.py --master=$master --baudrate $baud --state-basedir="/home/pi/mavlogs" --out=tcpin:127.0.0.1:14550 --out=udp:127.0.0.1:5760 --out=$dronekit --out=udp:10.243.0.1:14551
 	sleep 5
 	done
