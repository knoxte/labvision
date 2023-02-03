from unittest import TestCase
from labvision import images, data_dir
import numpy as np
import pkg_resources
import os


class TestReadImg(TestCase):
    def test_read_jpg(self):
        filepath = os.path.join(data_dir, "SampleImage.jpg")
        # filepath = pkg_resources.resource_filename(__name__, path)
        im = images.read_img(filepath)
        self.assertTrue(type(im) == np.ndarray)
        self.assertTrue(np.shape(im)[2] == 3)

    def test_read_jpg_grayscale(self):
        filepath = os.path.join(data_dir, "SampleImage.jpg")
        im = images.read_img(filepath, grayscale=True)
        self.assertTrue(len(np.shape(im))==2)

