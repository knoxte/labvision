from labvision.images.draw import draw_circle
from labvision.images.feature_detection import find_circles, find_connected_components
from tests import binary_single_circle, grayscale_img_test2, rgb_img_test2
from labvision.images.feature_detection import extract_nth_biggest_object
import numpy as np

def test_find_circles():
    """Test that find_circles finds 121 circles and one circle of radius 68.3"""
    img = rgb_img_test2()
    circles = find_circles(grayscale_img_test2(), 50, 70, 10, 40, 70)
    for circle in circles:
        img = draw_circle(img, circle[0], circle[1], circle[2])
    assert len(circles) == 121
    assert int(circles[0][2]) == int(68.3)


def test_find_connected_components():
    """Test find connected components finds circle with centre at x=50 """
    labels, stats, centroids = find_connected_components(
        binary_single_circle())
    assert int(centroids[1][0]) == 50


def test_extract_nth_biggest_object():
    """Test can extract biggest object and second biggest object"""
    img = binary_single_circle()
    img[2:4, 2:4] = 255  # create a second small object
    assert int(np.sum(np.sum(extract_nth_biggest_object(img, n=2)))) == int(1020.0)
    assert int(np.sum(np.sum(extract_nth_biggest_object(img, n=1)))) == int(719355.0) 
