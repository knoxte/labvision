from labvision.camera import CameraBase
import os
import cv2
import subprocess
import time
import pexpect
import re
import datetime


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
        # self.kill_process()
        self.file_location = '/store_00010001/DCIM/100_PANA/'
        if mode == 'Picture':
            self._pic_initialise()
            print('Camera is in picture mode')
        if mode == 'Movie':
            self._movie_initialise()
            print('Camera is in movie mode')

    def kill_process(self):
        # kill the gphoto2 process at power on
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate()

        for line in out.splitlines():
            if b'gvfsd-gphoto2' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

    def _pic_initialise(self):
        # allows the gphoto2 shell to access files on the camera while in picture mode
        self.gphoto2_shell = pexpect.spawn('gphoto2 --shell')
        filename = self.take_frame()
        self.delete_file_from_camera(file=filename)
        return filename

    def _movie_initialise(self):
        # allows the gphoto2 shell to access files on the camera while in movie mode
        self.start_movie(first=True, duration=2)
        self.delete_file_from_camera()

    def take_frame(self):
        self.gphoto2_shell.sendline('capture-image')
        self.gphoto2_shell.expect(' on the camera')
        filename = self.gphoto2_shell.before.decode().split('100_PANA/')[-1]
        self.current_file = filename
        return filename

    def get_frame(self, delete=False):
        self.take_frame()
        filename = self.save_file_onto_computer()
        self.delete_file_from_camera()
        im = cv2.imread(filename)
        if delete:
            os.remove(filename)
        return im

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

    def delete_file_from_camera(self, file=None):
        if file is None:
            file = self.current_file
        self.gphoto2_shell.sendline('delete ' + self.file_location + file)
        self.gphoto2_shell.expect(' ')

    def delete_multiple_files_from_camera(self, file_list='All'):
        if file_list == 'All':
            file_list = self.list_files(print_list=False)
        for file in file_list:
            self.delete_file_from_camera(file=file)

    def save_file_onto_computer(self, file=None, saved_filename=None):
        if saved_filename is None:
            saved_filename = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        if file is None:
            file = self.current_file
        self.gphoto2_shell.sendline('get ' + self.file_location + file)
        self.gphoto2_shell.expect('Saving')
        os.system('mv ' + file + ' ' + saved_filename)
        return saved_filename

    def save_multiple_files_onto_computer(self, all_files=False, file_list='All'):
        if file_list == 'All':
            file_list = self.list_files(print_list=False)
        for file in file_list:
            self.save_file_onto_computer(file=file)

    def start_movie(self, duration=None, first=False):
        if first is False:
            self.gphoto2_shell.close()
        self.gphoto2_shell = pexpect.spawn('gphoto2 --shell')
        self.gphoto2_shell.sendline('capture-image')
        time.sleep(1)
        self.gphoto2_shell.close()
        time.sleep(1)
        self.gphoto2_shell = pexpect.spawn('gphoto2 --shell')
        if duration:
            time.sleep(duration)
            self.stop_movie()

    def stop_movie(self):
        self.gphoto2_shell.sendline('capture-image')
        self.gphoto2_shell.expect('on the camera')
        filename = self.gphoto2_shell.before.decode().split('100_PANA/')[-1]
        self.current_file = filename
