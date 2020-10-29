import tkinter as tk
import random
from PIL import Image, ImageTk
import numpy as np

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider
from PyQt5.QtCore import Qt

from .QtImageViewer import QtImageViewer


from ..video import ReadVideo

import qimage2ndarray

from .basics import *
from .colors import *
from .geometric import *

import sys


__all__ = [
    "ParamGui",
    "ParamGui2"
]


class ParamGui2:

    def __init__(self, source):
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

    def init_ui(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.image_viewer = QtImageViewer()
        im = qimage2ndarray.array2qimage(self.im)
        self.image_viewer.setImage(im)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.image_viewer)
        self.add_sliders()
        self.window.setLayout(self.vbox)
        self.window.show()
        self.app.exec_()


    def add_sliders(self):
        if self.type in ['list', 'vid']:
            frame_slider = QSlider(Qt.Horizontal, self.window)
            frame_slider.setRange(0, self.num_frames-1)
            frame_slider.valueChanged.connect(self.frame_slider_update)
            self.vbox.addWidget(frame_slider)

    def frame_slider_update(self, value):
        if self.type == 'list':
            print('get')
            self.im = self.ims[value]
        else:
            self.im = self.vid.find_frame(value)
        # self.image_viewer.setImage(self.im)

class ParamGui:

    def __init__(self, img_or_vid, num_imgs=1, scale=1):
        self.scale = scale
        self.num_imgs = num_imgs
        self._file_setup(img_or_vid)
        self.im0 = self.im.copy()
        self.height, self.width = self.im0.shape[:2]
        self.width = int(self.width * self.scale)
        self.height = int(self.height * self.scale)
        if self.num_imgs == 2:
            self.width *= 2.1

        if num_imgs == 2:
            self._display_img(self.im0, self.im0)
        self.init_ui()

    def _file_setup(self, img_or_vid):
        if isinstance(img_or_vid, np.ndarray):
            if self.grayscale and len(img_or_vid.shape) == 3:
                self.im = bgr_to_gray(img_or_vid)
            else:
                self.im = img_or_vid
            self.type = 'singleframe'
        else:
            self.read_vid = img_or_vid
            self.frame_no = 0
            self.num_frames = self.read_vid.num_frames
            self.read_vid.grayscale = self.grayscale
            self.im = self.read_vid.find_frame(self.frame_no)
            self.type = 'multiframe'

    def init_ui(self):
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.canvas = tk.Canvas(self.frame, width=self.width,
                                height=self.height)
        im = Image.fromarray(self.im).resize((self.width, self.height))
        image = ImageTk.PhotoImage(im)
        self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW,
                                                     image=image)
        self.image = image
        self.canvas.pack()

        # Create live update checkbox
        self.live_update = tk.BooleanVar(False)
        cb = tk.Checkbutton(self.frame, text='Live update',
                            variable=self.live_update, onvalue=True,
                            offvalue=False, command=self.cb_callback)
        cb.pack()

        self.add_sliders()

        tk.mainloop()

    def cb_callback(self):
        if self.live_update:
            self._update_sliders()

    def slider_callback(self, val):
        for key in self.param_dict:
            val = self.sliders[key].get()
            self.labels[key].config(text=val)
        if self.live_update.get():
            self._update_sliders()

    def add_sliders(self):

        self.variables = {}
        self.sliders = {}
        self.labels = {}

        if self.type == 'multiframe':
            frame = tk.Frame(self.frame)
            label = tk.Label(frame, text='frame')
            label.pack(side=tk.LEFT)
            self.frame_slider = tk.Scale(frame, from_=0, to=self.num_frames,
                                         orient=tk.HORIZONTAL,
                                         length=self.width // 2,
                                         command=self.slider_callback)
            self.frame_slider.pack(side=tk.LEFT, fill=tk.X)

        for key in sorted(self.param_dict.keys()):
            params = self.param_dict[key]
            val, bottom, top, step = params
            frame = tk.Frame(self.frame)
            label = tk.Label(frame, text=key)
            label.pack(side=tk.LEFT)
            var = tk.Variable(value=val)
            slider = OddScale(frame, from_=bottom, to=top, resolution=step,
                              orient=tk.HORIZONTAL, showvalue=False,
                              length=self.width // 2,
                              command=self.slider_callback, variable=var)
            slider.pack(side=tk.LEFT, fill=tk.X)
            label = tk.Label(frame, text=slider.get())
            label.pack(side=tk.LEFT)
            frame.pack()
            self.variables[key] = var
            self.sliders[key] = slider
            self.labels[key] = label

    def _update_sliders(self):
        if self.type == 'multiframe':
            self.frame_no = self.frame_slider.get()
            self.im0 = self.read_vid.find_frame(self.frame_no)

        for key in self.param_dict:
            val = self.sliders[key].get()
            self.param_dict[key][0] = val
        self.update()
        self.update_im()

    def update_im(self):
        im = Image.fromarray(self.im).resize((self.width, self.height))
        self.image = ImageTk.PhotoImage(im)
        self.canvas.itemconfig(self.canvas_image, image=self.image)

    def _display_img(self, *ims):
        if len(ims) == 1:
            self.im = ims[0]
        else:
            self.im = hstack(*ims)


class OddScale(tk.Scale):

    def __init__(self, master=None, cnf={}, **kw):
        self.odd_only = False
        if 'resolution' in kw:
            if 'from_' in kw:
                if (kw['resolution'] == 2) * (kw['from_'] % 2 != 0):
                    self.odd_only = True
        kw['resolution'] = 1
        tk.Scale.__init__(self, master, cnf, **kw)

    def get(self):
        value = self.tk.call(self._w, 'get')
        try:
            val = self.tk.getint(value)
        except (ValueError, TypeError, tk.TclError):
            val = self.tk.getdouble(value)
        if self.odd_only:
            if val % 2 == 0:
                val += 1
        self.set(val)
        return val
