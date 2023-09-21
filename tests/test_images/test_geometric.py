import pytest
import numpy as np
import cv2

from labvision.images.basics import display
from labvision.images.geometric import get_shape, resize, rotate, hstack, vstack, to_uint8

from tests import rgb_img_test, grayscale_img_test



#---------------------------------------------------------------
#   tests
#---------------------------------------------------------------
def test_get_shape():
    "Test get_shape correctly identifies colour depth"
    assert get_shape(rgb_img_test())[2] == 3
    assert get_shape(grayscale_img_test())[2] == 1

def test_resize():
    new_img = resize(rgb_img_test(), percent=25)
    assert np.shape(new_img)[0] == int(0.25*np.shape(rgb_img_test())[0])

def test_rotate():
    rot_img = rotate(rgb_img_test(), 90)
    assert np.sum(rot_img[:,10]) == 1218266

def test_hstack_colour():
    img = rgb_img_test()
    stacked_img = hstack(img,img)
    assert np.shape(stacked_img)[1] == 2*np.shape(img)[1]

def test_hstack_gray():
    img = grayscale_img_test()
    stacked_img = hstack(img,img)
    assert np.shape(stacked_img)[1] == 2*np.shape(img)[1]

def test_hstack_mixed():
    img1 = rgb_img_test()
    img2 = grayscale_img_test()
    stacked_img = hstack(img1,img2)
    assert np.shape(stacked_img)[1] == 2*np.shape(img1)[1]

def test_vstack_colour():
    """test vstack works with colour imgs"""
    img = rgb_img_test()
    stacked_img = vstack(img,img)
    assert np.shape(stacked_img)[0] == 2*np.shape(img)[0]

def test_vstack_gray():
    """test vstack works with grayscale imgs"""
    img = grayscale_img_test()
    stacked_img = vstack(img,img)
    assert np.shape(stacked_img)[0] == 2*np.shape(img)[0]

def test_vstack_mixed():
    """Test vstack works with mixed depth images"""
    img1 = rgb_img_test()
    img2 = grayscale_img_test()
    stacked_img = vstack(img1,img2)
    assert np.shape(stacked_img)[0] == 2*np.shape(img1)[0]

def test_convert_uint8():
    """Check to_uint8 converts array to uint8"""
    assert to_uint8(rgb_img_test()).dtype == np.dtype('uint8')