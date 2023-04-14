from cv2 import threshold
import numpy as np
from labvision.tests import binary_img_test, grayscale_img_test, rgb_img_test, grayscale_img_test2, contour_test, contour_test2
from labvision.tests.test_images.test_morphological import test_dilate, test_erode, test_closing, test_opening
from labvision.tests.test_images.test_feature_detection import test_extract_nth_biggest_object, test_find_circles, test_find_connected_components

filename = 'C:\\Users\\mikei\\OneDrive - The University of Nottingham\\Documents\\Programming\\labvision\\labvision\\data\\jpgs\\SampleImage.jpg'


test_extract_nth_biggest_object()
