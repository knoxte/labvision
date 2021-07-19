import sys

from labvision import camera
from sh import gphoto2
import time
import subprocess
import os
import cv2


cam1 = camera.Panasonic()
cam1.take_frame()
cam1.save_file(saved_filename='square')



# cam2 = camera.Panasonic()
# cam2.list_files()
