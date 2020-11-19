import tkinter as tk
import random
from PIL import Image, ImageTk
import numpy as np

from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QCheckBox
from PySide2.QtCore import Qt

from qtwidgets import QImageViewer, QCustomSlider


from ..video import ReadVideo
from ..images import gray_to_bgr
from .geometric import *

import sys


__all__ = [
    "ParamGui",
]


class ParamGui:

    def __init__(self, source):
        # self.show_original = show_original
        self.parse_source(source)
        self.init_ui()

    def parse_source(self, source):
        assert isinstance(source, ReadVideo) or isinstance(source, list) or isinstance(source, np.ndarray), \
            "source must be a ReadVideo, list or numpy array instance"
        if isinstance(source, np.ndarray):
            self.im = source
            self.type = 'im'

        if isinstance(source, ReadVideo):
            self.vid = source
            self.frame_no = 0
            self.num_frames = self.vid.num_frames
            self.im = self.vid.find_frame(self.frame_no)
            self.type = 'vid'

        if isinstance(source, list):
            self.ims = source
            self.im = self.ims[0]
            self.frame_no = 0
            self.num_frames = len(self.ims)
            self.type = 'list'

        self.im0 = self.im.copy()

    def init_ui(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.image_viewer = QImageViewer()
        self.image_viewer.setImage(self.im)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.image_viewer)

        self.live_update_checkbox = QCheckBox('Live Update', parent=self.window)
        self.vbox.addWidget(self.live_update_checkbox)

        self.add_sliders()
        self.live_update_checkbox.stateChanged.connect(self._update_sliders)
        self.window.setLayout(self.vbox)
        self.window.show()
        self.app.exec_()

    def add_sliders(self):

        self.sliders = {}

        if self.type in ['list', 'vid']:
            self.frame_slider = QCustomSlider(
                self.window, title='frame', min_=0, max_=self.num_frames-1, spinbox=True,
                return_func=self.frame_slider_update)
            self.vbox.addWidget(self.frame_slider)

        for key in sorted(self.param_dict.keys()):
            params = self.param_dict[key]
            val, bottom, top, step = params
            slider = QCustomSlider(
                parent=self.window, title=key, min_=bottom, max_=top, value_=val,
                return_func=self.slider_callback, odd=True, spinbox=True)
            self.vbox.addWidget(slider)
            self.sliders[key] = slider

    def slider_callback(self, val):
        for key in self.param_dict:
            val = self.sliders[key].value()
        if self.live_update_checkbox.isChecked():
            self._update_sliders()

    def _update_sliders(self):
        if self.type in ['list', 'vid']:
            self.frame_no = self.frame_slider.value()
            if self.type == 'list':
                self.im0 = self.ims[self.frame_no]
            else:
                self.im0 = self.read_vid.find_frame(self.frame_no)

        for key in self.param_dict:
            val = self.sliders[key].value()
            self.param_dict[key][0] = val
        self.update()
        self.update_im()

    def frame_slider_update(self, value):
        if self.type == 'list':
            print('get')
            self.im = self.ims[value]
        else:
            self.im = self.vid.find_frame(value)

    def _display_img(self, *ims):
        if len(ims) == 1:
            self.im = ims[0]
        else:
            ims = list(ims)
            for i in range(len(ims)):
                if len(ims[i].shape) == 2:
                    ims[i] = gray_to_bgr(ims[i])
            self.im = hstack(*ims)

    def update_im(self):
        self.image_viewer.setImage(self.im)
