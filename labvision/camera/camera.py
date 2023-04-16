from .camera_config import *
from labvision.images.basics import display, Displayer
import datetime
import cv2
import sys
import os



class CameraBase:
    """
    Camera is a simple base class that handles some of the operations common
    to different types of cameras. Its child classes are Camera which handles webcams.
    and DigitalCamera in digital_camera.py which handles digital cameras.
    """
    def __init__(self, cam_type):
        self.cam_type=cam_type

    def set_property(self, property=None, value=None):
        try:
            self.set(property, value)
        except:
            raise CamPropsError(property)

    def get_property(self, property=None):
        try:
            self.get(property)
        except:
            raise CamPropsError(property)

    def _timestamp(self):
        return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    def show_frame(self):
        # Base
        frame = self.get_frame()
        display(frame, 'Current frame')

    def preview(self):
        window = Displayer('Camera')
        while True:
            frame = self.get_frame()
            window.update_im(frame)
            if not window.active:
                break

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        if True:
            return self.get_frame()
        else:
            raise StopIteration

