from tests import grayscale_img_test
from labvision.images.thresholds import adaptive_threshold, threshold
import numpy as np



def test_threshold():
    """Check threshold of gray image"""
    assert np.sum(np.sum(threshold(grayscale_img_test(), 100))) == 1994091585


def test_adaptive_threshold():
    """Check adaptive threshold"""
    assert np.sum(np.sum(adaptive_threshold(
        grayscale_img_test(), 11, 5))) == 2965494960



