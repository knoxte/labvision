from unittest import TestCase
from labvision import data_dir, images 
import os 


class TestCropPolygon(TestCase):
    def test_crop_image(self):
        filepath = os.path.join(data_dir, "SampleImage.jpg")
        im = images.read_img(filepath)
        result = images.crop_polygon(im)
        im = images.crop_and_mask(im, result.bbox, result.mask)
        print(images.width_and_height(im))
        images.display(im)
        result = input('Enter 1 if worked, 0 otherwise : ')
        self.assertTrue(result == str(1))