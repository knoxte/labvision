import cv2
import numpy as np

from qtwidgets.config import ConfigGui

from labvision.images.colours import bgr_to_gray, gray_to_bgr

__all__ = [
    'threshold',
    'adaptive_threshold',
]


def threshold(im, value=None, invert=False, configure=False):
    """
    Thresholds an image

    Pixels below thresh set to black, pixels above set to white
    modes =cv2.THRESH_BINARY (default), cv2.THRESH_BINARY_INV
    complete list here (https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html#ggaa9e58d2860d4afa658ef70a9b1115576ac7e89a5e95490116e7d2082b3096b2b8)
    """
    
    if configure:
        param_dict = {'value':[value,0,255,1],'invert':[int(invert),0,1,1]}
        gui = ConfigGui(im, threshold, param_dict)
        thresh_img = threshold(im, **gui.reduced_dict)
        gui.app.quit()
    else:
        if value is None:
            invert = invert + cv2.THRESH_OTSU
        thresh_img = cv2.threshold(im, value, 255, int(invert))[1]
    return thresh_img


def adaptive_threshold(im, block_size=10, constant=5, invert=False, configure=False):
    """
    Performs an adaptive threshold on an image

    Uses cv2.ADAPTIVE_THRESH_GAUSSIAN_C:
        threshold value is the weighted sum of neighbourhood values where
        weights are a gaussian window.

    Uses cv2.THRESH_BINARY:
        Pixels below the threshold set to black
        Pixels above the threshold set to white

    Parameters
    ----------
    img: numpy array containing an image

    block_size: the size of the neighbourhood area

    constant: subtracted from the weighted sum
    """

    if configure:
        param_dict = {'block_size':[block_size,1,block_size*25,2],'constant':[constant,1,constant*25,2],'invert':[int(invert),0,1,1]}
        gui = ConfigGui(im, adaptive_threshold, param_dict)
        out = adaptive_threshold(im, **gui.reduced_dict)
        gui.app.quit()
    else:
        out = cv2.adaptiveThreshold(
            im,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            int(invert),
            block_size,
            constant
        )
    return out



def absolute_diff(img, value, normalise=False, configure=False):
    """Returns an image which is the absolute difference between value and pixel intensity
    """
    if configure:
        param_dict = {'value':[100,1,255,1], 'normalise':[0, 0, 1, 1]}
        gui = ConfigGui(img, absolute_diff, param_dict)
        out = absolute_diff(img, **gui.reduced_dict)
        gui.app.quit()
    else:
        subtract_frame = value*np.ones(np.shape(img), dtype=np.uint8)  
        frame1 = cv2.subtract(subtract_frame, img)
        frame1 = cv2.normalize(frame1, frame1 ,0,255,cv2.NORM_MINMAX)
        frame2 = cv2.subtract(img, subtract_frame)
        frame2 = cv2.normalize(frame2, frame2,0,255,cv2.NORM_MINMAX)
        out = cv2.add(frame1, frame2)

        if normalise == True:
            out = cv2.normalize(out, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

    return out




