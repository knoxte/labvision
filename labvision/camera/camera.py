from types import NoneType
from ..images import save
import cv2
import sys
import os

import datetime

from camera_config import CameraType, CameraProperty
from typing import Optional, Tuple


class Camera:
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
    cam = Camera(cam_type=EXAMPLE_CAMERA)

    img = cam.get_frame()


    '''

    def __init__(self, cam_num=None, cam_type : CameraType = CameraType('LOGITECH_HD_1080P'), frame_size : Tuple[int, int, int] = None, fps : Optional[float] = None, ):
        if cam_num is None:
            cam_num = guess_camera_number()

        self.cam = cv2.VideoCapture(cam_num, apiPreference=cv2.CAP_DSHOW)#cv2.CAP_DSHOW # cv2.CAP_MSMF seems to break camera
        self.set = self.cam.set
        self.get = self.cam.get

        if not self.cam.isOpened():
            raise CamReadError(self.cam, None)

    def get_frame(self):
        """Get a frame from the camera and return"""
        ret, frame = self.cam.read()
        if not ret:
            raise CamReadError(cam, frame)
        return frame

    def close(self):
        """Release the OpenCV camera instance"""
        self.cam.release()

    def get_property(self, property: str):
        try:
            return self.get(CameraProperty(property))
        except:
            raise CamPropsError(property)

    
    def set_property(self, property: str = 'width', value=None):
        try:
            self.set(CameraProperty(property), value)
        except:
            raise CamPropsError(property)      

    def get_props(self, show=False):
        """Retrieve a complete list of camera property values.
        Set show=True to print to the terminal"""

        self.width = self.get(CameraProperty('width'))
        self.height = self.get(CameraProperty('height'))
        self.fps = self.get(CameraProperty('fps'))
        self.format = self.get(CameraProperty('format'))
        self.mode = self.get(CameraProperty('mode'))
        self.saturation = self.get(CameraProperty('saturation'))
        self.gain = self.get(CameraProperty('gain'))
        self.hue = self.get(CameraProperty('hue'))
        self.contrast = self.get(CameraProperty('contrast'))
        self.brightness = self.get(CameraProperty('brightness'))
        self.exposure = self.get(CameraProperty('exposure'))
        self.auto_exposure = self.get(CameraProperty('auto_exposure'))

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
        self.set(CameraProperty('brightness'), self.brightness)
        self.set(CameraProperty('contrast'), self.contrast)
        self.set(CameraProperty('gain'), self.gain)
        self.set(CameraProperty('hue'), self.hue)
        self.set(CameraProperty('exposure'), self.exposure)

    def _timestamp(self):
        return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

WebCamera = Camera


def guess_camera_number():
    """Function to find camera number assigned to cam by computer"""

    try:
        assert (
            'linux' in sys.platform), "guess_camera_number only implemented for linux"
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

#--------------------------------------------------------------------------------------------------------
# Exceptions
#--------------------------------------------------------------------------------------------------------

class CamReadError(Exception):
    def __init__(self, cam, frame_size):
        if not cam.isOpened():
            print('Camera instance not open')
        if type(frame_size) is NoneType:
            print('No frame returned')

class CamPropsError(Exception):
    def __init__(self, property_name):
        assert property_name in self.properties.keys(), 'property name does not exist'
        print('Error setting camera property')

