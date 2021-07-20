import sys

from labvision import camera
from sh import gphoto2
import time
import subprocess
import os
import cv2

cam1 = camera.Panasonic()
cam1.take_frame()
cam1.save_file(saved_filename='box2')


# cam2 = camera.Panasonic(mode='Movie')
# cam2.list_files()