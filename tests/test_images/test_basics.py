import numpy as np
import os
import pytest

from labvision.images.basics import write_img, read_img
from tests import DATA_DIR


def test_read_jpg():
    """Test that a jpeg can be read"""
    filepath = os.path.join(DATA_DIR, "jpgs/SampleImage.jpg")
    im = read_img(filepath)
    assert type(im) == np.ndarray
    assert np.shape(im)[2] == 3

def test_read_jpg_grayscale():
    """Test that a jpeg can be read in as grayscale image"""
    filepath = os.path.join(DATA_DIR, "jpgs/SampleImage.jpg")
    im = read_img(filepath, grayscale=True)
    assert len(np.shape(im))==2

def test_write_img():
   """Test writing a jpeg to file"""
   filepath = os.path.join(DATA_DIR, "test.jpg")
   write_img(np.zeros((100,100,3)), filepath)
   assert os.path.exists(filepath)
   os.remove(filepath)

def test_write_img_exception_empty_img():
    filepath = os.path.join(DATA_DIR, "test.jpg")
    with pytest.raises(Exception):
        write_img(np.zeros(0),filepath)




