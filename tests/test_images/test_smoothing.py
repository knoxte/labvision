from ast import Assert
import pytest
from labvision.images.blurs import gaussian_blur, median_blur
from tests import binary_single_circle


def test_gaussian_blur():
    """Test a gaussian blur. Circle has radius 30 and centre 50,50"""
    img = gaussian_blur(binary_single_circle(), kernel=(11, 11))
    assert img[17, 50] > 0


def test_median_blur():
    """Test a median blur. Circle has radius 30 and centre 50,50"""
    img = median_blur(binary_single_circle(), kernel=11)
    print(img)
    assert img[21, 50] > 0
    with pytest.raises(AssertionError):
        assert img[19, 50] > 0
