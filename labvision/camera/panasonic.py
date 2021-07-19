from labvision.camera import CameraBase
import os
import cv2
import subprocess
import time
import numpy as np
from labvision.images import Displayer, display
import pexpect
import re


class Panasonic(CameraBase):
    """
    This class is for Panasonic cameras. In order to take photos or movies, the camera must be far enough away from any
    objects so that it can autofocus or the code will hang.

    Parameters
    ----------
    duration : int or None  Recording length in seconds
    """

    def __init__(self, cam_type='Panasonic', mode='Picture'):
        super(Panasonic, self).__init__(cam_type=cam_type)
        self.kill_process()
        self.file_location = '/store_00010001/DCIM/100_PANA/'
        if mode == 'Picture':
            self.pic_initialise()
            print('Camera is in picture mode')
        if mode == 'Movie':
            self.movie_initialise()
            print('Camera is in movie mode')

    def kill_process(self):
        # kill the gphoto2 process at power on
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate()

        for line in out.splitlines():
            if b'gvfsd-gphoto2' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

    def preview(self):
        window = Displayer('Camera')
        loop = True
        while loop:
            proc = subprocess.Popen(["gphoto2 --capture-preview --stdout"], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            frame = cv2.imdecode(np.frombuffer(out, np.uint8), -1)
            window.update_im(frame)
            if not window.active:
                loop = False

    def pic_initialise(self):
        self.gphoto2_shell = pexpect.spawn('gphoto2 --shell', timeout=15)
        filename = self.take_frame()
        self.delete_file(file=filename)
        return filename

    def movie_initialise(self):
        self.start_movie(first=True, duration=2)
        self.delete_file()


    def take_frame(self):
        self.gphoto2_shell.sendline('capture-image')
        self.gphoto2_shell.expect(' on the camera')
        filename = self.gphoto2_shell.before.decode().split('100_PANA/')[-1]
        self.current_file = filename
        return filename

    def list_files(self, print_list=True):
        self.gphoto2_shell.sendline('ls ' + self.file_location)
        index = self.gphoto2_shell.expect(['P10.+JPG  ', 'P10.+MP4  ', pexpect.TIMEOUT])
        if index == 2:
            if print_list:
                print('There are no files')
        file_list = None
        if index == 0 or index == 1:
            file_string = self.gphoto2_shell.after.decode().split('/store_00010001/DCIM/100_PANA')[-1]
            file_list = re.findall(r'[\w.]+', file_string)
            if print_list:
                print(file_list)
        return file_list

    def delete_file(self, file=None):
        if file is None:
            file = self.current_file
        self.gphoto2_shell.sendline('delete ' + self.file_location + file)
        self.gphoto2_shell.expect(' ')

    def delete_multiple_files(self, all_files=False, file_list=None):
        if all_files:
            file_list = self.list_files(print_list=False)
        for file in file_list:
            self.delete_file(file=file)

    def save_file(self, file=None, saved_filename=None):
        if saved_filename is None:
            print(self._timestamp())
            saved_filename = self._timestamp()
        if file is None:
            file = self.current_file
        print('get ' + self.file_location + file)
        self.gphoto2_shell.sendline('get ' + self.file_location + file)
        self.gphoto2_shell.expect('Saving')
        os.system('mv ' + file + ' ' + saved_filename)

    def save_multiple_files(self, all_files=False, file_list=None):
        if all_files:
            file_list = self.list_files(print_list=False)
        for file in file_list:
            self.save_file(file=file)

    def start_movie(self, duration=None, first=False):
        if first is False:
            self.gphoto2_shell.close()
        self.gphoto2_shell = pexpect.spawn('gphoto2 --shell', timeout=15)
        self.gphoto2_shell.sendline('capture-image')
        time.sleep(1)
        self.gphoto2_shell.close()
        time.sleep(1)
        self.gphoto2_shell = pexpect.spawn('gphoto2 --shell', timeout=15)
        if duration:
            time.sleep(duration)
            self.stop_movie()

    def stop_movie(self):
        self.gphoto2_shell.sendline('capture-image')
        self.gphoto2_shell.expect('on the camera')
        filename = self.gphoto2_shell.before.decode().split('100_PANA/')[-1]
        self.current_file = filename
