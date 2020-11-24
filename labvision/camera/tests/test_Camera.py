from unittest import TestCase

from labvision import camera

import numpy as np


class TestCamera(TestCase):
    def test_can_open(self):
        cam = camera.Camera(cam_type=camera.LOGITECH_HD_1080P)
        self.assertTrue(cam.cam.isOpened())

    def test_can_get_frame(self):
        cam = camera.Camera(cam_type=camera.LOGITECH_HD_1080P)
        frame = cam.get_frame()
        self.assertTrue(type(frame) == np.ndarray)