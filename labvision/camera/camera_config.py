from enum import Enum
import cv2

class CameraType(Enum):
    """Camera settings.

    For the panasonic cameras these are accessed using a VideoCapture card.
    Panasonic.py enables you to use GPhoto2 on a Linux system to fully control Panasonic G9.
    Windows there is official software but not automated.

    Parameters
    ----------
    Enum : _type_
        _description_
    """
    LOGITECH_HD_1080P = {
        'apipreference': cv2.CAP_DSHOW,
        'name': 'Logi USB Camera (C615 HD WebCam)',
        'res': ((1920, 1080, 3), (640, 480, 3), (1280, 720, 3), (480, 360, 3)),
        'fps': ((30.0),)
    }

    PANASONICHCX1000 = {
        'apipreference': cv2.CAP_MSMF,
        'res': (1920, 1080, 3),
        'fps': ((60.0),)
    }

    PANASONICG9 = {
        'apipreference': cv2.CAP_MSMF,
        'res': ((1920, 1080, 3), (640, 480, 3), (1280, 720, 3), (480, 360, 3)),
        'fps': ((60.0),)
    }

    PHILIPS3 = {
        'apipreference': cv2.CAP_DSHOW,
        'res': ((640, 480, 3), (1280, 1080, 3)),
        'fps': ((20.0),)
    }


class CameraProperty(Enum):

    WIDTH = cv2.CAP_PROP_FRAME_WIDTH
    HEIGHT = cv2.CAP_PROP_FRAME_HEIGHT
    FPS = cv2.CAP_PROP_FPS
    FORMAT = cv2.CAP_PROP_FORMAT
    MODE = cv2.CAP_PROP_MODE
    SATURATION = cv2.CAP_PROP_SATURATION
    GAIN = cv2.CAP_PROP_GAIN
    HUE = cv2.CAP_PROP_HUE
    CONTRAST = cv2.CAP_PROP_CONTRAST
    BRIGHTNESS = cv2.CAP_PROP_BRIGHTNESS
    EXPOSURE = cv2.CAP_PROP_EXPOSURE
    AUTO_EXPOSURE = cv2.CAP_PROP_AUTO_EXPOSURE
