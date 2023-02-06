from unittest import TestCase
from labvision import data_dir, images
import os

class TestOpeningGui(TestCase):
    def test_circle_image(self):
        filepath = os.path.join(data_dir, "maxresdefault.jpg")
        im = images.read_img(filepath)
        images.OpeningGui(im)


class TestCircleGui(TestCase):
    def test_circle_image(self):
        filepath = os.path.join(data_dir, "maxresdefault.jpg")
        im = images.read_img(filepath)
        images.CircleGui(im)

class TestCircleGuiGray(TestCase):
    def test_circle_grayscale_image(self):
        print('GRAY')
        filepath = os.path.join(data_dir, "maxresdefault.jpg")
        im = images.read_img(filepath, True)
        images.CircleGui(im, rmax=500)
        print('Finished')


class TestThresholdGui(TestCase):
    def test(self):
        filepath = os.path.join(data_dir, "maxresdefault.jpg")
        im = images.read_img(filepath, True)
        images.ThresholdGui(im)


class TestAdaptiveThresholdGui(TestCase):
    def test(self):
        filepath = os.path.join(data_dir, "maxresdefault.jpg")
        im = images.read_img(filepath, True)
        images.AdaptiveThresholdGui(im)


class TestInRangeGui(TestCase):
    def test(self):
        filepath = os.path.join(data_dir, "maxresdefault.jpg")
        im = images.read_img(filepath, True)
        images.InrangeGui(im)

class TestContourGui(TestCase):
    def test(self):
        filepath = os.path.join(data_dir, "maxresdefault.jpg")
        im = images.read_img(filepath, True)
        images.ContoursGui(im)