from labvision.images.colors import bgr_to_gray, gray_to_bgr
from labvision.tests import *

import numpy as np


def test_bgr_to_gray():
    """Test bgr_to_gray converts to grayscale"""
    assert len(np.shape(bgr_to_gray(rgb_img_test()))) == 2


def test_gray_to_bgr():
    """Test gray_to_bgr converts to colour"""
    assert len(np.shape(gray_to_bgr(grayscale_img_test()))) == 3
