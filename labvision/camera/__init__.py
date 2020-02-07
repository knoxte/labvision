from .settings import *
from ..images import Displayer, display, save
import cv2
import sys
import os


class Camera:
    def __init__(
            self,
            cam_num,
            cam_type=LOGITECH_HD_1080P,
            frame_size=None,
            fps=None,
    ):
        self.cam = cv2.VideoCapture(cam_num)
        cam_type = cam_type

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

        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cam.set(cv2.CAP_PROP_FPS, frame_rate)

        ret, frame = self.cam.read()
        assert ret, 'Frame Reading Error'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def preview(self):
        window = Displayer('Camera')
        loop = True
        while loop:
            ret, frame = self.cam.read()
            window.update_im(frame)
            if not window.active:
                loop = False

    def set_property(self, property, value):
        properties = {
            'brightness':cv2.CAP_PROP_BRIGHTNESS,
            'contrast': cv2.CAP_PROP_CONTRAST,
            'gain': cv2.CAP_PROP_GAIN,
            'saturation': cv2.CAP_PROP_SATURATION,
            'hue': cv2.CAP_PROP_HUE,
            'exposure': cv2.CAP_PROP_EXPOSURE,
            'auto_exposure': cv2.CAP_PROP_AUTO_EXPOSURE
        }
        try:
            assert property in properties.keys(), 'Property not possible'
            try:
                self.cam.set(properties[property], value)
            except:
                raise CamPropsError(property, True)
        except AssertionError:
            raise CamPropsError(property, False)

    def get_frame(self):
        ret, frame = self.cam.read()
        return frame

    def save_frame(self, filename):
        ret, frame = self.cam.read()
        save(frame, filename)

    def show_frame(self):
        ret, frame = self.cam.read()
        display(frame, 'Current frame')

    def get_props(self, show=False):
        self.width = self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.fps = self.cam.get(cv2.CAP_PROP_FPS)
        self.format = self.cam.get(cv2.CAP_PROP_FORMAT)
        self.mode = self.cam.get(cv2.CAP_PROP_MODE)
        self.saturation = self.cam.get(cv2.CAP_PROP_SATURATION)
        self.gain = self.cam.get(cv2.CAP_PROP_GAIN)
        self.hue = self.cam.get(cv2.CAP_PROP_HUE)
        self.contrast = self.cam.get(cv2.CAP_PROP_CONTRAST)
        self.brightness = self.cam.get(cv2.CAP_PROP_BRIGHTNESS)
        self.exposure = self.cam.get(cv2.CAP_PROP_EXPOSURE)
        self.auto_exposure = self.cam.get(cv2.CAP_PROP_AUTO_EXPOSURE)

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


    def close(self):
        self.cam.release()


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
    def __init__(self, property_name, property_exists):
        if property_exists:
            print('Error setting camera property')
        else:
            print(property_name, 'does not exist')