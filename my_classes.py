import threading
import time

class MyThread(threading.Thread):
    def __init__(self, paused=False):
        super().__init__()
        self.daemon = False
        self.paused = paused
        self.stopped = False
        if self.paused:
            print(f"Create {self.__class__.__name__} thread paused")
        else:
            print(f"Create {self.__class__.__name__} thread running")
        self.lock = threading.Lock()

    def run(self):
        while not self.stopped:
            time.sleep(0.001)  # DO NOT DELETE - OBLIGATORY!!!!!!
            if not self.paused:
                self.active_code()
            else:
                self.sleep_code()

    def active_code(self):
        pass

    def sleep_code(self):
        time.sleep(1)
        pass

    def pause(self):
        self.paused = True
        print(f"{self.__class__.__name__} thread paused")

    def resume(self):
        if self.paused:
            self.paused = False
            print(f"{self.__class__.__name__} thread resumed")

    def stop(self):
        # with self.lock:
        print(f"{self.__class__.__name__} thread STOP")
        self.stopped = True

class Target(object):
    def __init__(self, lat=None, lon=None, alt=None):
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.imx, self.imy = -1, -1 #AI coordinates on image
        self.cnt_detect = 0
        self.marker = None

    def __str__(self):
        return "Target:lat=%s,lon=%s,alt=%s" % (self.lat, self.lon, self.alt)

class Detections(object):
    def __init__(self, box, class_name, conf=0.5):
        self.box = box
        self.class_name = class_name

    def __str__(self):
        return f"Detection:box={self.box},class={self.class_name}"