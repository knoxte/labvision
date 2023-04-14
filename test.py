
from ast import Param
from labvision.images.gui import ConfigGui
from labvision.tests import grayscale_img_test
from labvision.images.thresholding import threshold
from labvision.images.basics import display

img = threshold(grayscale_img_test(), value=100, configure=True)
display(img)
