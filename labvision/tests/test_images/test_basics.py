import labvision.images as images
import numpy as np
import os

data_dir = 'labvision/labvision/data'

def test_read_jpg():
    """Test that a jpeg can be read"""
    filepath = os.path.join(data_dir, "jpgs/SampleImage.jpg")
    im = images.read_img(filepath)
    assert type(im) == np.ndarray
    assert np.shape(im)[2] == 3

def test_read_jpg_grayscale():
    """Test that a jpeg can be read in as grayscale image"""
    filepath = os.path.join(data_dir, "jpgs/SampleImage.jpg")
    im = images.read_img(filepath, grayscale=True)
    assert len(np.shape(im))==2



