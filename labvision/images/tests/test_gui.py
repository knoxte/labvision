from unittest import TestCase
from labvision import data_dir, images
import os


class TestCircleGui(TestCase):
    def test_crop_image(self):
        filepath = os.path.join(data_dir, "SampleImage.jpg")
        im = images.read_img(filepath)
        images.CircleGui(im, scale=0.2)