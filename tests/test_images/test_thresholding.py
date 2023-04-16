from tests import binary_single_circle, grayscale_img_test
from labvision.images.thresholding import adaptive_threshold, threshold, distance_transform
import numpy as np
import cv2
from labvision.images.basics import display


def test_threshold():
    """Check threshold of gray image"""
    assert np.sum(np.sum(threshold(grayscale_img_test(), 100))) == 1994091585 

def test_adaptive_threshold():
    """Check adaptive threshold"""
    assert np.sum(np.sum(adaptive_threshold(grayscale_img_test(), 11, 5))) == 2965494960

def test_distance_transform():
    """Tests distance transform. Draws single binary circle cx,cy = 50,50 of radius 30 on blank image (100,100) and tests value of central pixel in circle which should be the rad in pixels."""
    img = distance_transform(binary_single_circle())
    assert int(img[50,50]) == 29
    