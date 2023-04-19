from types import NoneType
import cv2
import sys
import os

from .camera_config import CameraType, CameraProperty
from typing import Optional, Tuple

if os.name == 'nt':
    import win32com.client


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



  

    def __init__(self, cam_num=None, cam_type : CameraType = CameraType.LOGITECH_HD_1080P, frame_size : Tuple[int, int, int] = None, fps : Optional[float] = None, ):
        if cam_num is None:
            cam_num = guess_camera_number()

        self.cam = cv2.VideoCapture(cam_num, apiPreference=cam_type.value['apipreference'])#cv2.CAP_DSHOW # cv2.CAP_MSMF seems to break camera
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

    def get_property(self, property : CameraProperty=CameraProperty.WIDTH):
        if property in CameraProperty:
            setattr(self, property.name.lower(),self.get(property.value))
            return getattr(self, property.name.lower())
        else:
            raise CamPropsError(property)      

    def set_property(self, property: CameraProperty = CameraProperty.WIDTH, value=None):
        try:
            self.set(property.value, value)
            setattr(self, property.name.lower(),self.get(property.value))
        except:
            raise CamPropsError(property)      

    def get_props(self, show=False):
        """Retrieve a complete list of camera property values.
        Set show=True to print to the terminal"""
        properties = {}
        for property in CameraProperty:
            cam_value = self.get(property.value)
            setattr(self, property.name.lower(), cam_value)
            properties[property.name.lower()]= cam_value

        if show:
            print('----------------------------')
            print('List of Video Properties')
            print('----------------------------')
            for property in CameraProperty:
                print(property.name.lower() + ' : {}'.format(getattr(self, property.name.lower())))
            print('')
            print('unsupported features return 0')
            print('-----------------------------')
        
        return properties
        
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
        self.set(CameraProperty.BRIGHTNESS, self.brightness)
        self.set(CameraProperty.CONTRAST, self.contrast)
        self.set(CameraProperty.GAIN, self.gain)
        self.set(CameraProperty.HUE, self.hue)
        self.set(CameraProperty.EXPOSURE, self.exposure)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

WebCamera = Camera

def get_cameras_windows(camera : CameraType):
    wmi = win32com.client.GetObject("winmgmts:")
    for usb in wmi.InstancesOf("Win32_USBHub"):
        if usb.Name == CameraType.LOGITECH_HD_1080P.value['name']:
            print('Found Logitech')


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
        print('Frame size: {}'.format(frame_size))
        if not cam.isOpened():
            print('Camera instance not open')
        if type(frame_size) is NoneType:
            print('No frame returned')

class CamPropsError(Exception):
    def __init__(self, property_name):
        print('Error setting camera property: {}'.format(property_name))

