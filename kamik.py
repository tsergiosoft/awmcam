from my_classes import MyThread

from dronekit import connect, mavutil, VehicleMode, LocationGlobal, LocationGlobalRelative
import time
import copy
from math import sin, cos, atan2, asin, sqrt, atan, radians, degrees, pi

class Kamikaze(MyThread):
    def __init__(self, conn, paused):
        super().__init__(paused=paused)
        self.daemon = False
        self.conn = conn
        self.stopSignal = False

        self.stat_time = time.time()
        self.tot_updates = 0
        self.att_updates = 0
        self.att_fps = 0

        self.vehicle = None
        self.alive = False
        self.linkOK = False
        self.hearbeat = False
        self.last_attitude_cache = None
        self.roll, self.yaw, self.pitch = None, None, None
        self.velocity = None
        self.channels = [0] * 16
        self.mode = 'Initialize'
        self.AGL = 0
        self.att_timing = 0
        self.homeLocation = None
        self.currentLocation = None
        self.flytoLocation = None
        self.gps_use = False

    def active_code(self):
        if self.stopSignal:
            return False

        if not self.hearbeat:
            if self.alive:
                print("\033[91m" + "no MAVlink heartbit" + "\033[0m")
            self.alive = False
            self.linkOK = False
            self.homeLocation = None
            self.connect()
        else:
            if not self.linkOK:
                print("MAVLink heartbeats OK!")
            self.linkOK = True
            if self.gps_use:
                if self.vehicle.home_location is None:
                    print("Waiting for home location ...")
                    cmds = self.vehicle.commands
                    cmds.download()
                    cmds.wait_ready(timeout=5)
                    time.sleep(3)
                else:
                    if self.homeLocation is None:
                        print("\n Home location: %s" % self.vehicle.home_location)
                    self.homeLocation = self.vehicle.home_location


        if self.linkOK and ((not self.gps_use) or (self.gps_use and self.homeLocation is not None)):
            dt = time.time() - self.att_timing
            # print(f"dt={dt}")
            if dt > 8:
                if self.alive:
                    print("\033[91m"+"link NOT Alive:(("+"\033[0m")
                    self.alive = False
            else:
                if not self.alive:
                    print("\033[92m"+"link Alive!!!"+"\033[0m")
                    self.alive = True
        else:
            self.alive = False

        self.hearbeat = False  # reset and wait from listener
        # go to sleep and wait new heartbeat from listener
        time.sleep(1)

    def stop(self):
        self.stopSignal = True
        super().stop()

    def connect(self):
        # Connect to the Vehicle.
        #   Set `wait_ready=True` to ensure default attributes are populated before `connect()` returns.
        try:
            print("\nConnecting to vehicle on: %s" % self.conn)
            self.vehicle = connect(self.conn, wait_ready=False, timeout=10, heartbeat_timeout=5, baud=921600)
            # self.vehicle.add_attribute_listener('attitude', self.attitude_callback)
            # self.vehicle.add_attribute_listener('mode', self.mode_callback)
            # self.vehicle.add_attribute_listener('last_heartbeat', self.last_heartbeat_listener)
            @self.vehicle.on_attribute('last_heartbeat')
            def last_heartbeat(veh, name, msg):
                # print("last_heartbeat")
                self.hearbeat = True

            @self.vehicle.on_attribute('mode')
            def decorated_mode_callback(veh, attr_name, value):
                self.mode = value
                print("Mode changed to", value)

            @self.vehicle.on_message('RC_CHANNELS')
            def chin_listener(veh, name, message):
                # print('%s attribute is: %s' % (name, message))
                self.channels[1] = message.chan1_raw
                self.channels[2] = message.chan2_raw
                self.channels[3] = message.chan3_raw
                self.channels[4] = message.chan4_raw
                self.channels[5] = message.chan5_raw
                self.channels[6] = message.chan6_raw
                self.channels[7] = message.chan7_raw
                self.channels[8] = message.chan8_raw

            @self.vehicle.on_message('SERVO_OUTPUT_RAW')
            def listener(veh, name, message):
                self.ch1out = message.servo1_raw
                # print(f"self.ch1out={self.ch1out}")

            @self.vehicle.on_attribute('location')
            def location_listener(veh, name, msg):
                self.currentLocation = self.vehicle.location.global_frame
                self.velocity = self.vehicle.velocity

            @self.vehicle.on_attribute('velocity')
            def velocity_listener(veh, name, msg):
                self.velocity = self.vehicle.velocity

            @self.vehicle.on_attribute('attitude')
            def attitude_listener(veh, name, msg):
                # print("attitude_listener")
                self.att_timing = time.time()
                # if value != self.last_attitude_cache:
                # self.last_attitude_cache = value
                # Calculate statistic every 5 seconds
                self.att_updates += 1
                self.tot_updates += 1
                if time.time() - self.stat_time >= 5:
                    elapsed_time = time.time() - self.stat_time
                    self.att_fps = self.att_updates / elapsed_time
                    self.stat_time = time.time()
                    self.att_updates = 0

                self.pitch = degrees(self.vehicle.attitude.pitch)
                self.yaw = degrees(self.vehicle.attitude.yaw)
                self.roll = degrees(self.vehicle.attitude.roll)
        except:
            print("Exception when Connecting to vehicle ")

