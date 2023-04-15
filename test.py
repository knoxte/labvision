
from ast import Param
from labvision.images.feature_detection import find_circles
from labvision.images.gui import ConfigGui
from labvision.tests import binary_single_circle, grayscale_img_test2, rgb_img_test2
from labvision.images.morphological import dilate, closing, opening
from labvision.images.basics import display

img = opening(binary_single_circle(), kernel=3, iterations=5, configure=True)
display(img)
