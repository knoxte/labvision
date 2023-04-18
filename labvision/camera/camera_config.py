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
    'res': ((1920, 1080, 3), (640, 480, 3), (1280, 720, 3), (480, 360, 3)),
    'fps': ((30.0),)
    }

    PANASONICHCX1000= {
    'res': (1920, 1080, 3),
    'fps': ((60.0),)
    }

    PANASONICG9={
    'res': ((1920, 1080, 3), (640, 480, 3), (1280, 720, 3), (480, 360, 3)),
    'fps': ((60.0),)
    }

    PHILIPS3 = {
    'res': ((640, 480, 3), (1280, 1080, 3)),
    'fps': ((20.0),)
    }


class CameraProperty(Enum):

    width = cv2.CAP_PROP_FRAME_WIDTH
    height = cv2.CAP_PROP_FRAME_HEIGHT
    fps = cv2.CAP_PROP_FPS
    format = cv2.CAP_PROP_FORMAT
    mode = cv2.CAP_PROP_MODE
    saturation = cv2.CAP_PROP_SATURATION
    gain = cv2.CAP_PROP_GAIN
    hue = cv2.CAP_PROP_HUE
    contrast = cv2.CAP_PROP_CONTRAST
    brightness = cv2.CAP_PROP_BRIGHTNESS
    exposure = cv2.CAP_PROP_EXPOSURE
    auto_exposure = cv2.CAP_PROP_AUTO_EXPOSURE
