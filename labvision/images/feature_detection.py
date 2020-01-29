import cv2
import numpy as np
import matplotlib.pyplot as plt

from .basics import *
from .thresholding import *

__all__ = [
    "find_connected_components",
    "find_circles",
    "extract_biggest_object",
    "histogram_peak",
    "find_colour",
]


def find_connected_components(thresh_img, connectivity=4, option=cv2.CV_32S):
    """

    :param thresh_img: thresholded image
    :param connectivity: can be 4 or 8
    :param option:
    :return: labels, stats, centroids
    labels is a matrix the same size as the image where each element has a
    value equal to its label
    stats[label, COLUMN] where available columns are defined below.
        cv2.CC_STAT_LEFT The leftmost (x) coordinate which is the inclusive
        start of the bounding box in the horizontal direction.
        cv2.CC_STAT_TOP The topmost (y) coordinate which is the inclusive
        start of the bounding box in the vertical direction.
        cv2.CC_STAT_WIDTH The horizontal size of the bounding box
        cv2.CC_STAT_HEIGHT The vertical size of the bounding box
        cv2.CC_STAT_AREA The total area (in pixels) of the connected component
    centroids is a matrix with the x and y locations of each centroid.
    The row in this matrix corresponds to the label number.
    """
    output = cv2.connectedComponentsWithStats(thresh_img, connectivity, option)

    # num_labels = output[0]
    labels = output[1]
    stats = output[2]
    centroids = output[3]

    return labels, stats, centroids


def extract_biggest_object(img):
    output = cv2.connectedComponentsWithStats(img, 4, cv2.CV_32S)
    labels = output[1]
    stats = output[2]
    centroids = output[3]
    stats = stats[1:][:]
    index = np.argmax(stats[:, cv2.CC_STAT_AREA]) + 1
    out = np.zeros(np.shape(img))
    try:
        out[labels == index] = 255
    except:
        print(output[0])
        display(img)
    return out


def find_circles(img, min_dist, p1, p2, min_rad, max_rad, dp=1):
    circles = cv2.HoughCircles(
        img,
        cv2.HOUGH_GRADIENT, dp,
        min_dist,
        param1=p1,
        param2=p2,
        minRadius=min_rad,
        maxRadius=max_rad)
    return np.squeeze(circles)


def histogram_peak(im, disp=False):
    if len(np.shape(im)) == 2:
        data, bins = np.histogram(np.ndarray.flatten(im),
                                  bins=np.arange(20, 255, 1))
        peak = bins[np.argmax(data)]
    if disp:
        plt.figure()
        plt.plot(bins[:-1], data)
        plt.show()
    return peak


def find_colour(image, col, t=8, disp=False):
    """
    LAB colorspace allows finding colours somewhat independent of
    lighting conditions.

    https://www.learnopencv.com/color-spaces-in-opencv-cpp-python/
    """
    # Swap to LAB colorspace
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    b = lab[:, :, 2]
    if col == 'Blue':
        peak = histogram_peak(b, disp=disp)
        blue = threshold(b, thresh=peak - t, mode=cv2.THRESH_BINARY)
        return ~blue
