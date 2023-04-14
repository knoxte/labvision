"""import cv2
import numpy as np
from .gui_base import *
from .thresholding import *
from .feature_detection import *
from .draw import *
from .colors import *
from .smoothing import *
from .contours import *
from .morphological import *


__all__ = [
    "ThresholdGui",
    "CircleGui",
    "AdaptiveThresholdGui",
    "Inrange3GUI",
    "InrangeGui",
    "CannyGui",
    "ContoursGui",
    "OpeningGui",
    "ClosingGui",
    "ErosionGui",
    "DilationGui"
]


class ThresholdGui(ParamGui):
    def __init__(self, im):
        self.grayscale = True
        self.param_dict = {
            'threshold': [1, 0, 255, 1],
            'invert': [0, 0, 1, 1]}
        ParamGui.__init__(self, im)

    def update(self):
        if self.param_dict['invert'][0] == 0:
            self._display_img(threshold(self.im0,
                                        value=self.param_dict['threshold'][0]))
        else:
            self._display_img(threshold(self.im0,
                                        value=self.param_dict['threshold'][0],
                                        mode=cv2.THRESH_BINARY_INV))

class OpeningGui(ParamGui):
    def __init__(self, im):
        self.grayscale = True
        self.param_dict = {
            'kernel': [3, 1, 99, 2],
            'iterations': [1, 1, 20, 1]
        }
        ParamGui.__init__(self, im)

    def update(self):
        self._display_img(opening(self.im0,
                                  kernel=(self.param_dict['kernel'][0], self.param_dict['kernel'][0]),
                                  iterations=self.param_dict['iterations'][0]))


class ClosingGui(ParamGui):
    def __init__(self, im):
        self.grayscale = True
        self.param_dict = {
            'kernel': [3, 1, 99, 2],
            'iterations': [1, 1, 20, 1]
        }
        ParamGui.__init__(self, im)

    def update(self):
        self._display_img(closing(self.im0,
                                  kernel=(self.param_dict['kernel'][0],
                                          self.param_dict['kernel'][0]),
                                  iterations=self.param_dict['iterations'][0]))


class ErosionGui(ParamGui):
    def __init__(self, im):
        self.grayscale = True
        self.param_dict = {
            'kernel': [3, 1, 99, 2],
            'iterations': [1, 1, 20, 1]
        }
        ParamGui.__init__(self, im)

    def update(self):
        self._display_img(erode(self.im0,
                                  kernel=(self.param_dict['kernel'][0],
                                          self.param_dict['kernel'][0]),
                                  iterations=self.param_dict['iterations'][0]))


class DilationGui(ParamGui):
    def __init__(self, im):
        self.grayscale = True
        self.param_dict = {
            'kernel': [3, 1, 99, 2],
            'iterations': [1, 1, 20, 1]
        }
        ParamGui.__init__(self, im)

    def update(self):
        self._display_img(dilate(self.im0,
                                  kernel=(self.param_dict['kernel'][0],
                                          self.param_dict['kernel'][0]),
                                  iterations=self.param_dict['iterations'][0]))

class CircleGui(ParamGui):
    def __init__(self, img, rmax=50):
        self.grayscale = True
        self.param_dict = {
            'distance': [25, 3, 2*rmax, 2],
            'thresh1': [200, 0, 255, 1],
            'thresh2': [5, 0, 20, 1],
            'min_rad': [17, 3, rmax, 1],
            'max_rad': [19, 3, rmax, 1]
        }
        ParamGui.__init__(self, img)

    def update(self):
        circles = find_circles(self.im0, self.param_dict['distance'][0],
                               self.param_dict['thresh1'][0],
                               self.param_dict['thresh2'][0],
                               self.param_dict['min_rad'][0],
                               self.param_dict['max_rad'][0])
        if len(circles) > 0:
            self._display_img(draw_circles(gray_to_bgr(self.im0), circles))
        else:

            self._display_img(gray_to_bgr(self.im0))


class AdaptiveThresholdGui(ParamGui):

    def __init__(self, img, mode=cv2.THRESH_BINARY):
        self.grayscale = True
        self.param_dict = {'window': [3, 3, 101, 2],
                           'constant': [0, -30, 30, 1],
                           'invert': [0, 0, 1, 1]}
        self.mode = mode
        ParamGui.__init__(self, img)

    def update(self):
        if self.param_dict['invert'][0] == 0:
            self._display_img(adaptive_threshold(self.im0,
                                                 self.param_dict['window'][0],
                                                 self.param_dict['constant'][
                                                     0],
                                                 mode=self.mode)
                              )
        else:
            self._display_img(adaptive_threshold(self.im0,
                                                 self.param_dict['window'][0],
                                                 self.param_dict['constant'][
                                                     0],
                                                 mode=cv2.THRESH_BINARY_INV)
                              )


class InrangeGui(ParamGui):

    def __init__(self, img):
        self.grayscale = True
        self.param_dict = {'bottom': [1, 0, 255, 1],
                           'top': [200, 0, 255, 1]}
        ParamGui.__init__(self, img)

    def update(self):
        self.im = cv2.inRange(self.im0, self.param_dict['bottom'][0],
                              self.param_dict['top'][0])


class Inrange3GUI(ParamGui):

    def __init__(self, img):
        self.grayscale = False
        self.param_dict = {'0 bottom': [1, 0, 255, 1],
                           '0 top': [200, 0, 255, 1],
                           '1 bottom': [1, 0, 255, 1],
                           '1 top': [200, 0, 255, 1],
                           '2 bottom': [1, 0, 255, 1],
                           '2 top': [200, 0, 255, 1]}
        ParamGui.__init__(self, img)

    def update(self):
        self.im = cv2.inRange(
            self.im0,
            (self.param_dict['0 bottom'][0], self.param_dict['1 bottom'][0],
             self.param_dict['2 bottom'][0]),
            (self.param_dict['0 top'][0], self.param_dict['1 top'][0],
             self.param_dict['2 top'][0]))


class CannyGui(ParamGui):

    def __init__(self, img):
        self.grayscale = True
        self.param_dict = {'p1': [1, 0, 255, 1],
                           'p2': [1, 0, 255, 1],
                          'aperture':[3,3,7,2]}
        ParamGui.__init__(self, img)

    def update(self):
        self.im = cv2.Canny(self.im0,
                            self.param_dict['p1'][0],
                            self.param_dict['p2'][0],
                           apertureSize=self.param_dict['aperture'][0])


class ContoursGui(ParamGui):
    '''
    This applies adaptive threshold (this is what you are adjusting and is the
    value on the slider. It then applies findcontours and draws them to display result
    '''

    def __init__(self, img, thickness=2):
        self.param_dict = {'window': [53, 3, 101, 2],
                           'constant': [-26, -30, 30, 1],
                           'invert': [0, 0, 1, 1]}
        self.thickness = thickness
        self.grayscale = True
        ParamGui.__init__(self, img)
        self.blurred_img = self.im.copy()
        self.update()

    def update(self):
        self.blurred_img = gaussian_blur(self.im0.copy())
        thresh = adaptive_threshold(self.blurred_img,
                                    self.param_dict['window'][0],
                                    self.param_dict['constant'][0],
                                    self.param_dict['invert'][0])

        contours = find_contours(thresh)
        im2 = draw_contours(gray_to_bgr(self.im0.copy()), contours,
                            thickness=self.thickness)
        self._display_img(thresh, im2)


class RotatedBoxGui(ParamGui):
    '''
    This applies adaptive threshold (this is what you are adjusting and is the
    value on the slider. It then applies findcontours and draws them to display result
    '''

    def __init__(self, img, thickness=2):
        self.param_dict = {'window': [53, 3, 101, 2],
                           'constant': [-26, -30, 30, 1],
                           'invert': [0, 0, 1, 1]}
        self.thickness = thickness
        self.grayscale = True
        ParamGui.__init__(self, img)
        self.blurred_img = self.im.copy()
        self.update()

    def update(self):
        self.blurred_img = gaussian_blur(self.im0.copy())
        thresh = adaptive_threshold(self.blurred_img,
                                    self.param_dict['window'][0],
                                    self.param_dict['constant'][0],
                                    self.param_dict['invert'][0])

        contours = find_contours(thresh)
        box = []
        for contour in contours:
            box_guess, rect_guess = rotated_bounding_rectangle(contour)
            print(rect_guess[1][0])
            if rect_guess[1][0] < 15:
                box.append(box_guess)
            else:
                img = separate_rects(contour, box_guess)

        box = np.array(box)
        self._display_img(thresh, draw_contours(self.im0.copy(), box,
                                                thickness=self.thickness))


class DistanceTransformGui(ParamGui):
    def __init__(self, img):
        self.param_dict = {'window': [3, 3, 101, 2],
                           'constant': [0, -30, 30, 1],
                           'invert': [0, 0, 1, 1],
                           }
        self.grayscale = True
        ParamGui.__init__(self, img)
        self.blurred_img = self.im.copy()
        self.update()

    def update(self):
        self.blurred_img = gaussian_blur(self.im0.copy())
        thresh = adaptive_threshold(self.blurred_img,
                                    self.param_dict['window'][0],
                                    self.param_dict['constant'][0],
                                    self.param_dict['invert'][0]
                                    )

        dist_transform_img = distance_transform(self.blurred_img,
                                                preprocess=True,
                                                block_size=
                                                self.param_dict['window'][0],
                                                constant=
                                                self.param_dict['constant'][0],
                                                mode=self.param_dict['invert'][
                                                    0]
                                                )
        dist_transform_img = 255 * dist_transform_img / np.max(
            dist_transform_img)
        self._display_img(thresh, dist_transform_img)


class WatershedGui(ParamGui):
    def __init__(self, img):
        self.param_dict = {'window': [41, 3, 101, 2],
                           'constant': [-26, -30, 30, 1],
                           'invert': [0, 0, 1, 1],
                           'watershed_thresh': [1, 0, 255, 1]}
        self.grayscale = True
        ParamGui.__init__(self, img)
        self.blurred_img = self.im.copy()
        self.update()

    def update(self):
        self.blurred_img = gaussian_blur(self.im0.copy())
        thresh = adaptive_threshold(self.blurred_img,
                                    self.param_dict['window'][0],
                                    self.param_dict['constant'][0],
                                    self.param_dict['invert'][0]
                                    )

        watershed_img = watershed(self.im0.copy(),
                                  watershed_threshold=
                                  self.param_dict['watershed_thresh'][0],
                                  block_size=self.param_dict['window'][0],
                                  constant=self.param_dict['constant'][0],
                                  mode=self.param_dict['invert'][0]
                                  )
        self._display_img(thresh, watershed_img)
"""