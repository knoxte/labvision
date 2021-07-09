from labvision import camera
from sh import gphoto2
import time
import subprocess
import os
import cv2

cam1 = camera.Panasonic()

# cam1.save_frame(filename='test.jpg', time_stamp=True)
# cam1.start_movie(filename='test')
# time.sleep(3)
#
# cam1.stop_movie(filename='new4')
# cam1.show_frame()

cam1.preview()