#from labvision.camera import CameraBase
# from labvision.camera import QuickTimer
from ctypes import Union
import os
import cv2
import subprocess
import time
import pexpect
import re
import datetime
from typing import List, Dict, Tuple, Union, Optional

time_sleep = 1

class Panasonic:
    """
    This class is for The Panasonic G9 Camera. However, the underlying code probably works for
     everything that can be accessed with GPhoto2 command line tool. In order to take photos or movies, the camera must be far enough away from any objects so that it can autofocus or the code will hang. The code also requires access to gphoto2 which only seems to be available for linux and Mac. However, Windows now has the linux subsystem which should make it possible to use this.

    If fresh install check that gphoto2 is finding camera correctly. Open terminal type gphoto2 --auto-detect. If blank
    check its plugged in! I tried altering usb mode in camera menu to tether and turned camera on and off. It is
    something to do with things holding onto usb resources.
    """

    def __init__(self, movie_mode: bool = True,folder: Optional[str] = None):
        """Initialise Camera object

        Parameters
        ----------
        movie_mode : bool, optional
            True --> Take Movie
        folder : str, optional
            Path to folder on computer where you want to store the files. If None
            stores to either ~/Videos or ~/Pictures as appropriate.
        """
        self.cam_location = '/store_00010001/DCIM/100_PANA/'
        self.folder = folder
        if movie_mode:
            self.ext ='.mp4'
            if folder is None:
                self.folder = '~/Videos/' 
            self._movie_initialise()
        else:
            self.ext ='.jpg'
            if folder is None:
                self.folder = '~/Pictures/'
            self._pic_initialise()
    
    def _shell_cmd(self, command: str ='capture-image', time_sleep: int = 1):
        """Class method to send command to GPhoto2 Shell"""
        self.gphoto2_shell = pexpect.spawn('gphoto2 --shell')
        self.gphoto2_shell.sendline(command)
        time.sleep(time_sleep)
        self.gphoto2_shell.close()
    
    def _shell_cmd_reply(self, command : str = 'capture-image', expect_reply : str =' on the camera', time_sleep=1):
        self.gphoto2_shell = pexpect.spawn('gphoto2 --shell')
        self.gphoto2_shell.sendline(command)
        self.gphoto2_shell.expect(expect_reply)
        time.sleep(time_sleep)
        reply = self.gphoto2_shell.before.decode().split('100_PANA/')[-1]
        self.gphoto2_shell.close()
        return reply
        
    def _timestamp(self):
        shot_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        return shot_time
    """
    -----------------------------------------------------------------------------------------------------
    Movie Mode 
    --------------------------------------------------------------------------------------------------------
    """
    def _movie_initialise(self):
        # allows the gphoto2 shell to access files on the camera while in movie mode
        self.start_movie(duration=2)
        self.delete_file_from_camera()
        print('Camera is in movie mode')

    def start_movie(self, duration=None):
        try:
            self._shell_cmd('capture-image', time_sleep = duration)
        except:
            self.gphoto2_shell.close()
            self.start_movie(duration=duration)
        print('Movie Capture Started '  + self._timestamp())
        self.stop_movie()
        
    def stop_movie(self):
        self.cam_filename = self._shell_cmd_reply()
        print('Movie Capture Stopped ' + self._timestamp())

    """
    -----------------------------------------------------------------------------------------------------
    Picture Mode 
    --------------------------------------------------------------------------------------------------------
    """
    def _pic_initialise(self):
        # allows the gphoto2 shell to access files on the camera while in picture mode
        self.cam_filename = self._shell_cmd_reply()
        self.delete_file_from_camera(file=cam_filename)
        print('Camera is in picture mode')

    def get_frame(self):
        """Get a frame from the camera and return"""
        self.cam_filename = self._shell_cmd_reply()
        im_filename = self.save_file_onto_computer()
        self.delete_file_from_camera()
        im = cv2.imread(im_filename)
        return im

    def list_files(self, print_list : bool = True):
        """Obtain a list of all files currently on the camera"""
        index = self._shell_cmd_reply(command='ls ' + self.file_location, expect_reply=['P10.+JPG  ', 'P10.+MP4  ', pexpect.TIMEOUT])

        if index == 2:
            if print_list:
                print('There are no files')
        file_list = None
        if index == 0 or index == 1:
            file_string = self.gphoto2_shell.after.decode().split(self.cam_location)[-1]
            file_list = re.findall(r'[\w.]+', file_string)
            if print_list:
                print(file_list)
        return file_list

    def delete_file_from_camera(self, file : Optional[str] = None):
        """Delete file from camera. If None deletes the last image."""
        if file is None:
            file = self.cam_filename
        print('delete ' + self.cam_location + file)
        self._shell_cmd_reply(command='delete ' + self.cam_location + file, expect_reply=' ')
    

    def delete_multiple_files_from_camera(self, file_list : str = 'All'):
        """Delete some or all of the photos on the camera"""
        if file_list == 'All':
            file_list = self.list_files(print_list=False)
        for file in file_list:
            self.delete_file_from_camera(file=file)

    def save_file_onto_computer(self, cam_filename: Optional[str] = None):
        """Transfer a file from camera to the folder on the computer"""
        if cam_filename is None:
            cam_filename = self.cam_filename
        saved_filename = self._timestamp() + '_' + cam_filename
        print('get ' + self.cam_location + cam_filename)
        self._shell_cmd_reply(command='get ' + self.cam_location + cam_filename, expect_reply='Saving')
        os.system('mv ' + self.folder + saved_filename + ' ' + cam_filename)
        return saved_filename

    def save_multiple_files_onto_computer(self, file_list : str | List = 'all'):
        """Transfer some or all files on camera to computer"""
        if file_list == 'all':
            cam_file_list = self.list_files(print_list=False)
        else:
            cam_file_list = file_list
            
        for cam_file in cam_file_list:
            self.save_file_onto_computer(cam_filename=cam_file)


if __name__ == '__main__':
    cam = Panasonic()
    cam.start_movie(duration=10)
    cam.save_file_onto_computer()