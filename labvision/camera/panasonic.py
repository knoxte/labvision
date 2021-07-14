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

    def get_filename(self, filename=None, time_stamp=False):
        if filename is None:
            time_stamp = True
            filename = ''
        else:
            filename = filename.split('.')[0]

        if time_stamp:
            filename = filename + self._timestamp()

        return filename

    # def start_movie(self, duration=None, filename=None, time_stamp=False, not_started=True):
    #     filename = self.get_filename(filename=filename, time_stamp=time_stamp) + '.mp4'
    #
    #     if not_started:
    #         a = subprocess.Popen('gphoto2 --capture-image', shell=True)
    #
    #     if duration:
    #         time.sleep(duration)
    #         os.system('killall -9 gphoto2')
    #         os.system('gphoto2 --capture-image-and-download --filename ' + filename)
    #
    # def stop_movie(self, filename=None):
    #     self.start_movie(duration=0.1, filename=filename, not_started=False)
    #
    # def save_frame(self, filename=None, time_stamp=False):
    #     filename = self.get_filename(filename=filename, time_stamp=time_stamp) + '.jpg'
    #     os.system('gphoto2 --capture-image-and-download --filename ' + filename)
    #     return filename

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
        self.child = pexpect.spawn('gphoto2 --shell')
        self.child.sendline('capture-image')
        self.child.expect(' on the camera')
        file_name = self.child.before.decode().split('location ')[1]
        file_location = '/store_00010001/DCIM/100_PANA'
        self.child.sendline('delete ' + file_name)
        self.child.expect('')
        return file_location

    def movie_initialise(self):
        pass

    def list_files(self):
        file_location = '/store_00010001/DCIM/100_PANA'
        self.child.sendline('ls ' + file_location)
        self.child.expect('/P.+JPG  ')
        print(self.child.after.decode().split('/store_00010001/DCIM/100_PANA')[3])

    def delete_files(self, all_files=False):
        file_location, child = self.pic_initialise()

        pass

    def take_frame(self):
        pass

    def save_frame(self, filename=None, time_stamp=False):
        filename = self.get_filename(filename=filename, time_stamp=time_stamp)
        pass

    def frame(self, filename=None, save=False, time_stamp=False):
        self.take_frame()
        if save:
            self.save_frame()

    def start_movie(self, duration=None, filename=None, time_stamp=False, not_started=True, save=False):
        filename = self.get_filename(filename=filename, time_stamp=time_stamp) + '.mp4'

        if not_started:
            self.take_frame()

        if duration:
            time.sleep(duration)
            self.take_frame()

        if save:
            self.save_frame()

    def stop_movie(self, filename=None, save=False):
        self.start_movie(duration=0.1, filename=filename, not_started=False, save=save)
        p = subprocess.Popen(['gphoto2 --capture-image'], stdout=subprocess.PIPE)
        output = p.communicate()[0].split(b'\r\n')[1:-1]
        print(output)

    def communicate(self):
        a = subprocess.Popen(['gphoto2', '--capture-image'], stdout=subprocess.PIPE)
        time.sleep(1)
        a.kill()
        p = subprocess.Popen(['gphoto2', '--shell'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        query1 = 'capture-image'
        query2 = 'summary'
        concat_query = "{}\n{}".format(query1, query2)
        print(p.communicate(input=concat_query.encode('utf-8'))[0])
        # out, err = p.communicate(input='capture-image')
        # p.stdin.write('capture-image')
        # file_location = out[92:-56]
        # print('file location is ' + file_location)
