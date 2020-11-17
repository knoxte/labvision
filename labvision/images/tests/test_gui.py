from unittest import TestCase
from labvision import data_dir, images
import os


class TestCircleGui(TestCase):
    def test_crop_image(self):
        filepath = os.path.join(data_dir, "maxresdefault.jpg")
        im = images.read_img(filepath)
        images.CircleGui(im, scale=0.2)

class TestCircleGuiGray(TestCase):
    def test_crop_grayscale_image(self):
        print('GRAY')
        filepath = os.path.join(data_dir, "maxresdefault.jpg")
        im = images.read_img(filepath, True)
        images.CircleGui2(im)


class TestNewGUI(TestCase):
    def test(self):
        filepath = os.path.join(data_dir, "maxresdefault.jpg")
        im = images.read_img(filepath, grayscale=False)
        images.ParamGui2([im, im])
