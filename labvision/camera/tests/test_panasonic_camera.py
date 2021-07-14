import sys

from labvision import camera
from sh import gphoto2
import time
import subprocess
import os
import cv2
#
cam1 = camera.Panasonic()
cam1.take_frame()



# import pexpect
# child = pexpect.spawn('gphoto2 --shell')
# child.sendline('capture-image')
# child.expect(' on the camera')
# child.sendline('ls /store_00010001/DCIM/100_PANA')
# index = child.expect(['/P.+JPG  ', pexpect.EOF])
# print(index)
# print(child.before.decode())
# print(child.after.decode())
