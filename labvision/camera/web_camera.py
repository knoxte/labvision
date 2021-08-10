from .camera_config import *
from .camera import CameraBase
from ..images import Displayer, display, save
import datetime
import cv2
import sys
import os



class WebCamera(CameraBase):
    '''
    This class is called WebCamera but can also be called
    as Camera for historical reasons.
    This class handles webcameras. The supported webcams
    are described in camera_config.py. Each camera has a
    dictionary of basic settings. If you use a new camera add
    it to that file and give it a name in capitals.

    Parameters
    ----------
    cam_num : int or None   Defines the camera to which the instance points
    cam_type : Dict   Dictionaries for each camera are defined in camera_config.py
    frame_size : tuple   Only needs to be defined if you want a non-default value. Default
    Values are in position Zero in the Dict['frame_size']
    fps : int    Only needs to be defined if you want a non-default value. Default
    Values are in position Zero in the Dict['fps']


    Examples
    --------
    webcam = Camera(cam_type=EXAMPLE_CAMERA)

    img = webcam.get_frame()

    webcam.save_frame(filename, time_stamp=True)


    '''
    def __init__(self, cam_num=None, cam_type=LOGITECH_HD_1080P, frame_size=None, fps=None, ):

        if cam_num is None:
            cam_num = guess_camera_number()

        self.cam = cv2.VideoCapture(cam_num)
        self.set = self.cam.set
        self.get = self.cam.get
        super(Camera, self).__init__(cam_type)

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
        """Get a frame from the camera and return"""

        ret, frame = self.cam.read()
        return frame

    def save_frame(self, filename, time_stamp=True):
        """
        Get a frame from camera and save with filename. By
        default a timestamp is added to the end of the filename.
        Set time_stamp=False to prevent this behaviour."""

        frame = self.get_frame()
        fname, ext = filename.split('.')
        if time_stamp:
            save(frame, fname + self._timestamp() + '.' + ext)
        else:
            save(frame, filename)
        return filename

    def close(self):
        """Release the OpenCV camera instance"""

        self.cam.release()

    def get_props(self, show=False):
        """Retrieve a complete list of camera property values.
        Set show=True to print to the terminal"""

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
        """Save current settings to a file"""

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
        """Load current settings from file"""

        with open(filename, 'r') as f:
            settings = f.read().splitlines()
        self.brightness, self.contrast, self.gain, \
        self.saturation, self.hue, self.exposure = settings
        self.set_property('brightness', self.brightness)
        self.set_property('contrast', self.contrast)
        self.set_property('gain', self.gain)
        self.set_property('hue', self.hue)
        self.set_property('exposure', self.exposure)

Camera = WebCamera

def guess_camera_number():
    """Function to find camera number assigned to webcam by computer"""

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
