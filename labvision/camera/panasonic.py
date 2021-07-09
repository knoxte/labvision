from labvision.camera import CameraBase
import os
import cv2
import subprocess
import time
import numpy as np
from labvision.images import Displayer


class Panasonic(CameraBase):
    """
    This class is for Panasonic cameras. In order to take photos or movies, the camera must be far enough away from any
    objects so that it can autofocus or the code will hang.

    Parameters
    ----------
    duration : int or None  Recording length in seconds
    """
    def __init__(self, cam_type='Panasonic'):
        super(Panasonic, self).__init__(cam_type=cam_type)

    def kill_process(self):
        # kill the gphoto2 process at power on
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate()

        for line in out.splitlines():
            if b'gvfsd-gphoto2' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

    def get_filename(self, filename=None, time_stamp=False):
        if filename is None:
            time_stamp = True
            filename = ''
        else:
            filename = filename.split('.')[0]

        if time_stamp:
            filename = filename + self._timestamp()

        return filename

    def start_movie(self, duration=None, filename=None, time_stamp=False, not_started=True):
        filename = self.get_filename(filename=filename, time_stamp=time_stamp) + '.mp4'

        if not_started:
            a = subprocess.Popen('gphoto2 --capture-image', shell=True)

        if duration:
            time.sleep(duration)
            os.system('killall -9 gphoto2')
            os.system('gphoto2 --capture-image-and-download --filename ' + filename)

    def stop_movie(self, filename=None):
        self.start_movie(duration=0.1, filename=filename, not_started=False)

    def save_frame(self, filename=None, time_stamp=None):
        filename = self.get_filename(filename=filename, time_stamp=time_stamp) + '.jpg'
        os.system('gphoto2 --capture-image-and-download --filename ' + filename)
        return filename

    def get_frame(self, filename=None):
        filename = self.save_frame(filename)
        return cv2.imread(filename)

    def preview(self):
        window = Displayer('Camera')
        loop = True
        while loop:
            proc = subprocess.Popen(["gphoto2 --capture-preview --stdout"], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            frame = cv2.imdecode(np.frombuffer(out, np.uint8), -1)
            window.update_im(frame)
            if not window.active:
                loop = False


