from unittest import TestCase
from labvision import data_dir, images
import os

class TestRotate(TestCase):

    def test(self):
        filepath = os.path.join(data_dir, "maxresdefault.jpg")
        im = images.read_img(filepath)
        im = images.rotate(im, 90)
        images.display(im)