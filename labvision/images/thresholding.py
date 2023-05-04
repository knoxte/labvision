import cv2
import numpy as np

from qtwidgets.config import ConfigGui

from labvision.images.colors import bgr_to_gray, gray_to_bgr

__all__ = [
    'threshold',
    'adaptive_threshold',
    'inrange',
    'watershed',
    'distance_transform'
]


def threshold(im, value=None, mode=cv2.THRESH_BINARY, configure=False):
    """
    Thresholds an image

    Pixels below thresh set to black, pixels above set to white
    modes =cv2.THRESH_BINARY (default), cv2.THRESH_BINARY_INV
    complete list here (https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html#ggaa9e58d2860d4afa658ef70a9b1115576ac7e89a5e95490116e7d2082b3096b2b8)
    """
    
    if configure:
        param_dict = {'value':[value,0,255,1],'mode':[mode,0,1,1]}
        gui = ConfigGui(im, threshold, param_dict)
        thresh_img = threshold(im, **gui.reduced_dict)
        gui.app.quit()
    else:
        if value is None:
            mode = mode + cv2.THRESH_OTSU
        thresh_img = cv2.threshold(im, value, 255, mode)[1]
    return thresh_img


def adaptive_threshold(im, block_size=10, constant=5, mode=cv2.THRESH_BINARY, configure=False):
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
        param_dict = {'block_size':[block_size,1,block_size*25,2],'constant':[constant,1,constant*25,2],'mode':[mode,0,1,1]}
        gui = ConfigGui(im, adaptive_threshold, param_dict)
        out = adaptive_threshold(im, **gui.reduced_dict)
        gui.app.quit()
    else:
        out = cv2.adaptiveThreshold(
            im,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            mode,
            block_size,
            constant
        )
    return out

def distance_transform(img):
    """
    Calculates the distance to the closest zero pixel for each pixel.

    Calculates the approximate or precise distance from every binary image
    pixel to the nearest zero pixel. For zero image pixels, the distance will
    obviously be zero.

    Parameters
    ----------
    img: 8-bit image.

    Returns
    -------
    out: Output image with calculated distances.
        It is a 8-bit or 32-bit floating-point, single-channel image of the
        same size as img.

    References
    ----------
    Pedro Felzenszwalb and Daniel Huttenlocher. Distance transforms of sampled
    functions. Technical report, Cornell University, 2004.
    """
    dist_transform = cv2.distanceTransform(img, cv2.DIST_L2, 5)
    return dist_transform


#---------------------------------------------------------
# Not actively used or tested. kept for historical reasons #---------------------------------------------------------


def inrange(im, bottom_tuple, top_tuple):
    return cv2.inRange(im, bottom_tuple, top_tuple)


def watershed(img, watershed_threshold=0.5, block_size=5, constant=0,
              mode=cv2.THRESH_BINARY):
    d = depth(img)
    if d == 3:
        grayscale_img = bgr_to_gray(img)
    else:
        grayscale_img = img.copy()
        img = gray_to_bgr(
            img)

    binary_img = adaptive_threshold(grayscale_img, block_size=block_size,
                                    constant=constant, mode=mode)

    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel,
                               iterations=2)
    # sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform_img = distance_transform(binary_img)

    # sure foreground area
    sure_fg = threshold(dist_transform_img, value=watershed_threshold)
    sure_fg = np.uint8(sure_fg)

    # Finding unknown region
    unknown = cv2.subtract(sure_bg, sure_fg)
    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1

    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0
    markers = cv2.watershed(img, markers)
    img[markers == -1] = [255, 0, 0]

    return img


