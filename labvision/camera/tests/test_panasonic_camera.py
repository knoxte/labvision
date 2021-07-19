import sys

from labvision import camera
from sh import gphoto2
import time
import subprocess
import os
import cv2
#
cam1 = camera.Panasonic(mode='Movie')
cam1.list_files()


# import pexpect
# child = pexpect.spawn('gphoto2 --shell')
# child.sendline('capture-image')
# child.expect(' on the camera')
# child.sendline('get /store_00010001/DCIM/100_PANA/P1000727.JPG')
# child.expect('Saving')
# # time.sleep(1)
# child.sendline('capture-image')
# child.expect(r'[\w]')
# child.sendline('ls /store_00010001/DCIM/100_PANA')
# child.expect(r'[\w]')
# print(child.after.decode())
# child.expect(' on the camera')
# child.sendline('ls /store_00010001/DCIM/100_PANA')
# index = child.expect(['/P.+JPG  ', pexpect.EOF])
# print(index)
# print(child.before.decode())
# print(child.after.decode())
#
# cam2 = camera.Panasonic()
# cam2.list_files()
