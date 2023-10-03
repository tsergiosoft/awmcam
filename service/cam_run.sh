#cd ~/mjpg-streamer/mjpg-streamer-experimental
#export LD_LIBRARY_PATH=.

mjpg_streamer -i '/usr/local/lib/mjpg-streamer/input_uvc.so -d /dev/video0 -n' -o '/usr/local/lib/mjpg-streamer/output_http.so -w /home/pi/mjpg-streamer/mjpg-streamer-experimental/www -p 8080'

#YUVU format (f param) - better pic slower stream
#mjpg_streamer -i '/usr/local/lib/mjpg-streamer/input_uvc.so -d /dev/video0  -f 2 -n' -o '/usr/local/lib/mjpg-streamer/output_http.so -w /home/pi/mjpg-streamer/mjpg-streamer-experimental/www -p 8080'

#   file simulation without CAM
#mjpg_streamer -i '/usr/local/lib/mjpg-streamer/input_file.so -e -f /home/pi/awm/camsimul' -o '/usr/local/lib/mjpg-streamer/output_http.so -w /home/pi/mjpg-streamer/mjpg-streamer-experimental/www -p 8080'

#raspivid -n -t 0 -w 1024 -h 768 -s -b 1000000 -o -|tee ~/video1.h264 | cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8080}' :demux=h264
