from labvision.images.contours import center_of_mass, contour_to_xy, cut_out_object, find_contours, contour_props, bounding_rectangle, rotated_bounding_rectangle, sort_contours
from labvision.tests import binary_img_test, contour_test, contour_test2, grayscale_img_test2
import numpy as np


def test_find_contours():
    """Test find_contours finds contours"""
    contours = find_contours(binary_img_test())
    assert len(contours) == 366


def test_find_contours_hierarchy():
    """Test the hierarchy feature of contour finding"""
    contours, hier = find_contours(binary_img_test(), hierarchy=True)
    assert hier[0][10][1] == 9


def test_contour_to_xy():
    x, y = contour_to_xy(contour_test())
    assert x[5] == 117


def test_center_of_mass():
    """Test center of mass of contour found correctly"""
    cx, cy = center_of_mass(contour_test())
    assert cx == 109


def test_contour_props():
    """Test contour props returns area"""
    _, _, area = contour_props(contour_test())
    assert area == 172.0


def test_bounding_rectangle():
    """Test bounding rectangle"""
    x, y, w, h = bounding_rectangle(contour_test())
    assert w == 15

def test_sort_contours():
    cnts = tuple([contour_test(), contour_test2()])
    sorted_contours = sort_contours(cnts)
    assert len(sorted_contours[0]) == 6


def test_cut_out_object():
    cut_im = cut_out_object(grayscale_img_test2(), contour_test())
    assert np.shape(cut_out_object(
        grayscale_img_test2(), contour_test())[0])[0] == 29
