import signal
import subprocess
from sh import gphoto2
import time
import cv2
import os

from .camera import CameraBase

class DigitalCamera(CameraBase):
    def __init__(self, cam_type='NIKON_DSCOOLPIX_9600'):
        super(DigitalCamera, self).__init__(cam_type=cam_type)

    def kill_process(self):
        #kill the gphoto2 process at power on
        p = subprocess.Popen(['ps','-A'],stdout=subprocess.PIPE)
        out, err = p.communicate()

        for line in out.splitlines():
            if b'gvfsd-gphoto2' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

    def get_frame(self):
        filename = self.save_frame()
        return cv2.imread(filename)

    def save_frame(self, filename=None, time_stamp=True):
        if filename is None:
            time_stamp = True
            filename = '.jpg'

        if time_stamp:
            filename, ext = filename.split('.')
            filename + self._timestamp() + '.' + ext

        gphoto2('--capture-image-and-download --filename ' + filename)

        return filename

    def camera_settings(self):
        settings_script = self.cam_type['script']
        time.sleep(1)
        p = subprocess.Popen([settings_script], stdout=subprocess.PIPE)
        time.sleep(2)