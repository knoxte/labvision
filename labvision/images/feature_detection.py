import cv2
import numpy as np
import matplotlib.pyplot as plt

from .basics import *
from .thresholding import *

from labvision.images.gui import ConfigGui

__all__ = [
    "find_connected_components",
    "find_circles",
    "extract_biggest_object",
    "histogram_peak",
    "find_colour",
]



def find_circles(img: np.array, min_dist: int, p1: int, p2: int, min_rad: int, max_rad: int, dp: int=1, configure=False):
    """find_circles

    Finds circles in an image using OpenCV HoughCircles
    
    Parameters
    ----------
    img : nd.array
        _description_
    min_dist : int
        min distance between circle centres
    p1 : int
        accumulator param 1. Smaller leads to more circles
        For details - see https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d
    p2 : int
        accumulator param 2. Smaller gives more circles
    min_rad : int
        min radius of circle
    max_rad : int
        max radius of circle
    dp : int, optional
        , by default 1

    Returns
    -------
    List of circles like [[]]
    """
    if configure:
        param_dict = {
            'min_dist': [min_dist, 3, min_dist*10, 2],
            'p1': [p1, 1, 255, 1],
            'p2': [p2, 1, 255, 1],
            'min_rad': [min_rad, 3, min_rad*10, 1],
            'max_rad': [max_rad, 3, max_rad*10, 1],
            'dp':[dp,1,dp*10,1]
        }
        circles = ConfigGui(img, find_circles, **param_dict)
    else:
        circles = cv2.HoughCircles(
            img,
            cv2.HOUGH_GRADIENT, dp,
            min_dist,
            param1=p1,
            param2=p2,
            minRadius=min_rad,
            maxRadius=max_rad)
    return np.squeeze(circles)


def find_connected_components(thresh_img: np.ndarray, connectivity: int=4, option=cv2.CV_32S):
    """Find binary collections of pixels that are connected together.

    :param thresh_img: thresholded image
    :param connectivity: can be 4 or 8
    :param option:

    :return: labels, stats, centroids

    labels is a matrix the same size as the image where each element has a
    value equal to its label
    stats[label, COLUMN] where available columns are defined below.
    |    cv2.CC_STAT_LEFT The leftmost (x) coordinate which is the inclusive
    |    start of the bounding box in the horizontal direction.
    |    cv2.CC_STAT_TOP The topmost (y) coordinate which is the inclusive
    |    start of the bounding box in the vertical direction.
    |    cv2.CC_STAT_WIDTH The horizontal size of the bounding box
    |    cv2.CC_STAT_HEIGHT The vertical size of the bounding box
    |    cv2.CC_STAT_AREA The total area (in pixels) of the connected component
    centroids is a matrix with the x and y locations of each centroid.
    The row in this matrix corresponds to the label number.
    """

    output = cv2.connectedComponentsWithStats(thresh_img, connectivity, option)

    # num_labels = output[0]
    labels = output[1]
    stats = output[2]
    centroids = output[3]

    return labels, stats, centroids

def extract_biggest_object():
    return extract_nth_biggest_object(n=1)

def extract_nth_biggest_object(img, n=1):
    """
    Finds the object with the nth most pixels in an image. n=1 is the biggest
    n=0 will extract the black object left when the other bits are removed.

    Parameters
    ---------
    img: np.ndarray
    |   Image must be binary.

    Returns
    -------
    img: np.ndarray
    |    The returned image is binary with just the pixels of
    |    the nth largest object white

    """

    output = cv2.connectedComponentsWithStats(img, 4, cv2.CV_32S)
    labels = output[1]
    stats = output[2]
    #stats = stats[:][:]
    areas = stats[:,4]
    print(areas)
    sort_index = np.argsort(areas)
    #index = np.argmax(stats[:, cv2.CC_STAT_AREA]) + 1
    out = np.zeros(np.shape(img))
    print(sort_index[n])
    try:
        out[labels == sort_index[::-1][n]] = 255
    except:
        print(output[0])
        display(img)
    return out





#--------------------------------------------------------------------
# Historical code
#----------------------------------------------------------------------


def find_colour(image, col, t=8, disp=False):
    """
    LAB colorspace allows finding colours somewhat independent of
    lighting conditions.

    param

    https://www.learnopencv.com/color-spaces-in-opencv-cpp-python/
    """
    # Swap to LAB colorspace
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    b = lab[:, :, 2]
    if col == 'Blue':
        peak = histogram_peak(b, disp=disp)
        blue = threshold(b, thresh=peak - t, mode=cv2.THRESH_BINARY)
        return ~blue


def histogram_peak(im, disp=False):
    """

    :param im:
    :param disp:

    :return:

    """

    if len(np.shape(im)) == 2:
        data, bins = np.histogram(np.ndarray.flatten(im),
                                  bins=np.arange(20, 255, 1))
        peak = bins[np.argmax(data)]
    if disp:
        plt.figure()
        plt.plot(bins[:-1], data)
        plt.show()
    return peak