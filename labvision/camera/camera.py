from .settings import *
from ..images import Displayer, display, save
import datetime
import time
import cv2
import sys
import os
import signal
import subprocess
from sh import gphoto2



class CameraBase:
    """
    Camera is a simple base class that handles some of the operations common
    to different types of cameras. The things it does are relatively minimal.

    """
    def __init__(self, cam_type):
        self.cam_type= cam_type


    def set_property(self, property=None, value=None):
        try:
            self.set(property, value)
        except:
            raise CamPropsError(property)

    def get_property(self, property=None):
        try:
            self.get(property)
        except:
            raise CamPropsError(property)

    def _timestamp(self):
        shot_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        return shot_time

    def show_frame(self):
        # Base
        frame = self.get_frame()
        display(frame, 'Current frame')

    def preview(self):
        # Base
        window = Displayer('Camera')
        loop = True
        while loop:
            frame = self.get_frame()
            window.update_im(frame)
            if not window.active:
                loop = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        if True:
            return self.get_frame()
        else:
            raise StopIteration


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

    def camera_settings(self, settings_script='nikon_config.sh'):
        time.sleep(1)
        p = subprocess.Popen([settings_script], stdout=subprocess.PIPE)
        time.sleep(2)



class Camera(CameraBase):
    def __init__(self, cam_num=None, cam_type=LOGITECH_HD_1080P, frame_size=None, fps=None, ):

        if cam_num is None:
            cam_num = guess_camera_number()

        self.cam = cv2.VideoCapture(cam_num)
        self.set = self.cam.set
        self.get = self.cam.get
        super(WebCamera, self).__init__(cam_type)

        frame_sizes = cam_type['res']
        frame_rates = cam_type['fps']

        if frame_size is None:
            self.width, self.height = frame_sizes[0][:2]
        elif frame_size in frame_sizes:
            self.width, self.height = frame_size[:2]
        else:
            raise Exception('Frame shape not possible')

        if fps is None:
            frame_rate = frame_rates[0]
        elif fps in frame_rates:
            frame_rate = fps
        else:
            raise Exception('Frame rate not possible')

        self.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.set(cv2.CAP_PROP_FPS, frame_rate)

        ret, frame = self.cam.read()
        assert ret, 'Frame Reading Error'

    def get_frame(self):
        ret, frame = self.cam.read()
        return frame

    def save_frame(self, filename, time_stamp=True):
        frame = self.get_frame()
        fname, ext = filename.split('.')
        if time_stamp:
            save(frame, fname + self._timestamp() + '.' + ext)
        else:
            save(frame, filename)
        return filename

    def close(self):
        self.cam.release()

    def get_props(self, show=False):
        self.width = self.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.fps = self.get(cv2.CAP_PROP_FPS)
        self.format = self.get(cv2.CAP_PROP_FORMAT)
        self.mode = self.get(cv2.CAP_PROP_MODE)
        self.saturation = self.get(cv2.CAP_PROP_SATURATION)
        self.gain = self.get(cv2.CAP_PROP_GAIN)
        self.hue = self.get(cv2.CAP_PROP_HUE)
        self.contrast = self.get(cv2.CAP_PROP_CONTRAST)
        self.brightness = self.get(cv2.CAP_PROP_BRIGHTNESS)
        self.exposure = self.get(cv2.CAP_PROP_EXPOSURE)
        self.auto_exposure = self.get(cv2.CAP_PROP_AUTO_EXPOSURE)

        if show:
            print('----------------------------')
            print('List of Video Properties')
            print('----------------------------')
            print('width : ', self.width)
            print('height : ', self.height)
            print('fps : ', self.fps)
            print('format : ', self.format)
            print('mode : ', self.mode)
            print('brightness : ', self.brightness)
            print('contrast : ', self.contrast)
            print('hue : ', self.hue)
            print('saturation : ', self.saturation)
            print('gain : ', self.gain)
            print('exposure :', self.exposure)
            print('auto_exposure:', self.auto_exposure)
            print('')
            print('unsupported features return 0')
            print('-----------------------------')

    def save_settings(self, filename):
        # Base refactor settings to dict
        self.get_props()
        settings = (
            self.brightness,
            self.contrast,
            self.gain,
            self.saturation,
            self.hue,
            self.exposure
        )
        with open(filename, "w") as f:
            for item in settings:
                f.write("%s\n" % item)

    def load_settings(self, filename):
        with open(filename, 'r') as f:
            settings = f.read().splitlines()
        self.brightness, self.contrast, self.gain, \
        self.saturation, self.hue, self.exposure = settings
        self.set_property('brightness', self.brightness)
        self.set_property('contrast', self.contrast)
        self.set_property('gain', self.gain)
        self.set_property('hue', self.hue)
        self.set_property('exposure', self.exposure)


def guess_camera_number():
    try:
        assert ('linux' in sys.platform), "guess_camera_number only implemented for linux"
        items = os.listdir('/dev/')
        newlist = []
        for names in items:
            if names.startswith("video"):
                newlist.append(names)
        cam_num = int(newlist[0][5:])
    except AssertionError as error:
        print(error)
        print("Camera number set to 0")
        cam_num = 0

    return cam_num


class CamPropsError(Exception):
    def __init__(self, property_name):
        assert property_name in self.properties.keys(), 'property name does not exist'
        print('Error setting camera property')


