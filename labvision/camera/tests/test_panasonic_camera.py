import sys

from labvision import camera
from sh import gphoto2
import time
import subprocess
import os
import cv2

cam1 = camera.Panasonic()
cam1.list_files()

# cam1.save_frame(filename='test.jpg')
# cam1.start_movie(filename='test')
# time.sleep(3)
#
# cam1.stop_movie(filename='new4')
# cam1.show_frame()

# cam1.preview()

# cam1.show_frame('test.jpg')

#
# a = subprocess.Popen(['gphoto2', '--capture-image'], stdout=subprocess.PIPE)
#
# time.sleep(1)
# a.kill()

# print(child.readline()[16:-16])
# child.sendline('cd /store_00010001/DCIM/100_PANA')
# child.expect('Remote directory')
# child.sendline('get P1000386.JPG')
# child.expect('Saving file')
# child.sendline('capture-image')
# child.expect('New')

# import pexpect
# child = pexpect.spawn('gphoto2 --shell')
# child.sendline('capture-image')
# child.expect(' on the camera')
# print(child.before.decode())

#
# import re
#
# pattern = '^a...s$'
# test_string = 'ab2ss'
# result = re.match(pattern, test_string)
#
# if result:
#   print("Search successful.")
# else:
#   print("Search unsuccessful.")
#

