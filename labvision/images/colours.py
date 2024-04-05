import cv2
import numpy as np

__all__ = [
    'BLUE',
    'LIME',
    'RED',
    'YELLOW',
    'ORANGE',
    'BLACK',
    'WHITE',
    'MAGENTA',
    'PINK',
    'CYAN',
    'NAVY',
    'TEAL',
    'PURPLE',
    'GREEN',
    'MAROON',
    'bgr_to_gray',
    'gray_to_bgr',
]

BLUE = (255, 0, 0)
LIME = (0, 255, 0)
RED = (0, 0, 255)
YELLOW = (0, 255, 255)
ORANGE = (0, 128, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MAGENTA = (255, 0, 255)
PINK = MAGENTA
CYAN = (255, 255, 0)
NAVY = (128, 0, 0)
TEAL = (128, 128, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 128, 0)
MAROON = (0, 0, 128)


def bgr_to_gray(img):
    if _colour(img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def gray_to_bgr(img):
    if not _colour(img):
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img


def _colour(img):
    if np.size(np.shape(img)) == 3:
        return True
    else:
        return False

