import numpy as np
import cv2

from labvision.custom_exceptions import NotImageError

from .basics import *
from .colors import *

__all__ = ['resize', 'rotate', 'hstack', 'vstack', 'to_uint8']


def get_shape(img):
    """get_shape

    Returns width, height, depth for an image

    Parameters
    ----------
    img: Array containing an image

    Returns
    -------
    width: int
        Width of the image
    height: int
        Height of the image
    depth: int
       Color depth of the image
    Notes
    -----
    Width of an image is the first dimension for numpy arrays.
    Height of an image is the first dimension for openCV
    """
    shp = np.shape(img)
    if len(shp) == 2:
        d = 1
    elif len(shp) == 3:
        d = shp[2]
    else:
        raise NotImageError

    w = shp[0]
    h = shp[1]

    return w, h, d


def resize(img, percent=25.0):
    """
    Resizes an image to a given percentage

    Parameters
    ----------
    img: numpy array containing an image

    percent:
        the new size of the image as a percentage

    Returns
    -------
    resized_image:
        The image after it's been resized

    """
    w, h = np.shape(img)[1], np.shape(img)[0]
    dim = (int(w * percent / 100), int(h * percent / 100))
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


def rotate(img, angle):
    """
    Rotates an image without cropping it

    Parameters
    ----------
    img: input image
        Can have any number of channels

    angle: angle to rotate by in degrees
        Positive values mean clockwise rotation

    Returns
    -------
    out: output image
        May have different dimensions than the original image

    """
    # grab the dimensions of the image and then determine the
    # center
    img_shape = np.shape(img)
    (h, w) = img_shape[:2]
    (c_x, c_y) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    rot_matrix = cv2.getRotationMatrix2D((c_x, c_y), -angle, 1.0)
    cos = np.abs(rot_matrix[0, 0])
    sin = np.abs(rot_matrix[0, 1])

    # compute the new bounding dimensions of the image
    n_w = int((h * sin) + (w * cos))
    n_h = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    rot_matrix[0, 2] += (n_w / 2) - c_x
    rot_matrix[1, 2] += (n_h / 2) - c_y

    # perform the actual rotation and return the image
    out = cv2.warpAffine(img, rot_matrix, (n_w, n_h))
    return out


def hstack(*args):
    """
    Stacks images horizontally. 

    If all grayscale or all colour leaves depth unchanged. If image depths are mismatched 
    then converts grayscale images to bgr before stacking
    """
    num_imgs = len(args)
    sum_depths = sum([get_shape(im)[2] for im in args])
    all_colour = (sum_depths * num_imgs / 3) == num_imgs
    all_gray = (sum_depths * num_imgs) == num_imgs
    if not (all_colour | all_gray):
        # mixture of gray and colour
        args = [gray_to_bgr(im) if get_shape(im)[2] ==
                1 else im for im in args]
    return np.hstack(args)


def vstack(*args):
    """
    Stacks images vertically

    If image depths are mismatched then converts grayscale images to bgr before stacking
    """
    num_imgs = len(args)
    sum_depths = sum([get_shape(im)[2] for im in args])
    all_colour = (sum_depths * num_imgs / 3) == num_imgs
    all_gray = (sum_depths * num_imgs) == num_imgs
    if not (all_colour | all_gray):
        args = [gray_to_bgr(im) if get_shape(im)[2] == 1 else im for im in args]
    return np.vstack(args)


def to_uint8(im):
    """Convert image to 8 bit"""
    im = (im - np.min(im)) / (np.max(im) - np.min(im)) * 255
    return np.uint8(im)
