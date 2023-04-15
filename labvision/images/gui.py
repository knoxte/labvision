import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox
from PyQt5.Qt import Qt
import PyQt5.QtCore as QtCore
from qtwidgets import QImageViewer, QCustomSlider


from .. import video
from . import gray_to_bgr
from .geometric import *

import sys


__all__ = [
    "ConfigGui"
]

class ConfigGui:
    def __init__(self, img, func, param_dict) -> None:
        """ConfigGui

        Takes an image and applies a image processing function to it.
        It then displays that image processed via the arguments in param_dict.
        Each param is assigned a slider which can be used to adjust the params.
        This is called by most functions if you set config=True.
        Enter or quite closes the window.

        Parameters
        ----------
        img : _type_
            _description_
        func : _type_
            _description_
        param_dict : _type_
            _description_
        """
        self.im=img
        self.im0 = img.copy()
        self.param_dict = {k:check_init_param_val(v) for k,v in param_dict.items()}
        self.func = func
        self.init_ui()
    
    def init_ui(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.image_viewer = QImageViewer()
        self.image_viewer.setImage(self.im)
        self.image_viewer.keyPressed.connect(self.close_gui)
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

        for key in sorted(self.param_dict.keys()):
            val, bottom, top, step = self.param_dict[key]
            slider = QCustomSlider(
                parent=self.window, title=key, min_=bottom, max_=top, value_=val,
                step_=step, spinbox=True)
            slider.valueChanged.connect(self.slider_callback)
            self.vbox.addWidget(slider)
            self.sliders[key] = slider

    def slider_callback(self):
        if self.live_update_checkbox.isChecked():
            self._update_sliders()

    def _update_sliders(self):
        for key in self.param_dict:
            val = self.sliders[key].value()
            self.param_dict[key][0] = val
        self.update_img()

    def update_img(self):
        """Update the image. Takes original image and applies the function
        to it. The dict comprehension takes the first value from the list of values
        with each key which corresponds to the value and passes new dictionary with key and 
        just this value to function."""
        self.im = self.func(self.im0,**{k:v[0] for k,v in self.param_dict.items()})
        self.image_viewer.setImage(self.im)
    
    def close_gui(self, event):
        if (event.type() == QtCore.QEvent.KeyPress):
            if event.key() == QtCore.Qt.Key_Space:
                self.reduced_dict = {k:v[0] for k,v in self.param_dict.items()}
                print(self.reduced_dict)
                self.window.close()
                

def check_init_param_val(param_list: list[int]):
    if param_list[3]%2==0:
        #If the increment value is 2 implies only odd values allowed
        if param_list[0]%2==0:
            #If initial value is even make it odd
            param_list[0] += 1
    return param_list
