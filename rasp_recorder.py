#!/usr/bin/python3
#sudo cp $HOME/jwm/tr1.service /etc/systemd/system
#sudo systemctl enable tr1.service
#sudo systemctl start tr1.service
import time
import cv2
import copy
#from pprint import *
import libcamera
from picamera2 import MappedArray, Picamera2, Preview
from picamera2.encoders import H264Encoder

class wCam():
    def __init__(self):
        self.picam2 = Picamera2()
        #pprint(self.picam2.sensor_modes)
        
        # picam2.start_preview(Preview.QTGL)       
        #self.config = self.picam2.create_preview_configuration(main={"size": (1920, 1080)},
        #            lores={"size": (800, 600), "format": "YUV420"})
        
        self.tracker = cv2.TrackerCSRT_create()
        self.track_on = None
        self.reinit(False)

    def reinit(self, track = True):
        self.track_on = track
        self.frame_cnt = 0
        self.roi_img, self.roi_img2 = [], []
        
        if self.track_on:
            self.config = self.picam2.create_preview_configuration(main={"size": (800, 600), "format": "RGB888"})
            #1640, 1232    1920, 1080  960, 360
        else:
            self.config = self.picam2.create_preview_configuration(main={"size": (1640, 1232), "format": "RGB888"})

        self.config["transform"] = libcamera.Transform(hflip=0, vflip=1)
        self.picam2.configure(self.config)
        self.encoder = H264Encoder(10000000)
        (w0, h0) = self.picam2.stream_configuration("main")["size"]    
            
        self.w0, self.h0 = w0, h0
        self.cx, self.cy = int(self.w0 * 0.5), int(self.h0 * 0.5)
        self.boxsize = 240
        self.roisize = 40
        self.roisize_half = int(self.roisize*0.5)
        self.zoom = 2
        self.boxzoom = self.boxsize * self.zoom
        self.boxsize_half = int(self.boxsize*0.5)

    def draw(self, request):
        colour = (255, 255, 255)
        origin = (0, 40)
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.5
        thickness = 1
        self.frame_cnt += 1
        print(f"\r{wcam.frame_cnt}", end="")
        
        with MappedArray(request, "main") as m:
            timestamp = time.strftime("%Y-%m-%d %X")
            timestamp = timestamp + f" size={self.w0}x{self.h0} frame={self.frame_cnt}"
            cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)
            if self.track_on:
                #Blue box
                cv2.rectangle(m.array, (self.cx-self.boxsize_half, self.cy-self.boxsize_half),
                              (self.cx+self.boxsize_half, self.cy+self.boxsize_half), (0, 0, 255), 2)
                # self.roi_img = m.array[self.cy-self.boxsize_half:self.cy+self.boxsize_half,
                #                              self.cx-self.boxsize_half:self.cx+self.boxsize_half]
                self.roi_img = copy.copy(m.array[self.cy-self.boxsize_half:self.cy+self.boxsize_half,
                                         self.cx-self.boxsize_half:self.cx+self.boxsize_half])
                # self.roi_img2 = cv2.resize(self.roi_img, (self.boxzoom, self.boxzoom))

                self.roi_img = self.roi_img[:, :, :3]
                if self.frame_cnt == 1:
                    self.tracker.init(self.roi_img, (self.boxsize_half-self.roisize_half, self.boxsize_half-self.roisize_half,
                                                 self.roisize, self.roisize))
                else:
                    success = False
                    success, bbox = self.tracker.update(self.roi_img)
                    if success:
                        x, y, w, h = [int(i) for i in bbox]
                        z = self.zoom
                        # cv2.rectangle(self.roi_img2, (x*z, y*z), (x*z + w*z, y*z + h*z), (0, 255, 0), 2)

                        x1 = self.cx-self.boxsize_half+x
                        y1 = self.cy - self.boxsize_half + y
                        x2,y2 = x1+w, y1+h
                        cv2.rectangle(m.array, (x1,y1), (x2,y2), (0, 255, 0), 2)

                    if not success or self.frame_cnt % 30 == 0:
                        print("init tracker")
                        self.tracker.init(self.roi_img,
                                          (self.boxsize_half - self.roisize_half, self.boxsize_half - self.roisize_half,
                                           self.roisize, self.roisize))

                # m.array[100:100 + self.boxzoom, 20:20 + self.boxzoom] = self.roi_img2

            if self.frame_cnt % 10 == 0:
                cv2.imshow("Camera", m.array)

cv2.startWindowThread()
cv2.namedWindow("Camera")
cv2.moveWindow("Camera",0,50)
wcam = wCam()
wcam.picam2.post_callback = wcam.draw

while True:
    start_time = time.monotonic()
    timestamp = time.strftime("%Y%d%m_%H_%M_%S")
    wcam.reinit(track = True)
    fname = f"/media/tr1{timestamp}T.h264"
    print(fname)
    wcam.picam2.start_recording(wcam.encoder, fname)
    ## Run for 30 seconds.
    while time.monotonic() - start_time < 30:
        pass
    wcam.picam2.stop_recording()

    time.sleep(2)

    start_time = time.monotonic()
    timestamp = time.strftime("%Y%d%m_%H_%M_%S")
    wcam.reinit(track = False)
    fname = f"/media/tr1{timestamp}V.h264"
    print(fname)
    wcam.picam2.start_recording(wcam.encoder, fname)
    # Run for 30 seconds.
    while time.monotonic() - start_time < 30:
        pass
    wcam.picam2.stop_recording()

