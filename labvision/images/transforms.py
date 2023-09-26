import cv2
import numpy as np

from qtwidgets.config import ConfigGui

from labvision.images.colours import bgr_to_gray, gray_to_bgr

__all__ = [
    'brightness_contrast',
    'gamma',
    'watershed',
    'distance',
    'absolute_diff'
]

def brightness_contrast(img, brightness=0, contrast=0, configure=False):
    """Brightness and Contrast control

    This is implemented as g(x) = contrast * f(x) + brightness

    but with checks to make sure the values don't fall outside 0-255"""
    if configure:
        param_dict = {'brightness':[brightness,0,255,0.001], 'contrast':[contrast,-100,100,0.001]}
        gui = ConfigGui(img, gamma, param_dict)
        brightness_contrast_img = brightness_contrast(img, **gui.reduced_dict)
        gui.app.quit()
    else:
        brightness_contrast_img =  cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)
    return brightness_contrast_img

def gamma(gray_img, gamma=1.0, configure=False):
    '''
    Apply look up table to image with power gamma

    Notes
    -----
    This generates a lookup table which maps the values 0-255 to 0-255
    however not in a linear way. The mapping follows a power law
    with exponent gamma/100.0.

    gamma
        single float can be positive or negative. The true value applied is the displayed value / 100.

    Args
    ----
    frame
        This is must be a grayscale / single colour channel image
    parameters
        Nested dictionary like object (same as .param files or output from general.param_file_creator.py
    call_num
        Usually None but if multiple calls are made modifies method name with get_method_key

    Returns
    -------
        grayscale image

    '''
    if configure:
        param_dict = {'gamma':[gamma,0,50,0.001]}
        gui = ConfigGui(gray_img, gamma, param_dict)
        gamma_img = gamma(gray_img, **gui.reduced_dict)
        gui.app.quit()
    else:
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
        if gamma == 0:
            gamma = 0.000001
        invGamma = 1.0 / gamma

        table = np.array([((i / 255.0) ** invGamma) *
                        255 for i in np.arange(0, 256)]).astype("uint8")

        gamma_img = cv2.LUT(gray_img, table)
    return gamma_img

def distance(bw_img, normalise=True):
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
    gray_img = cv2.distanceTransform(bw_img, cv2.DIST_L2, 5)
    if normalise:
        gray_img = 255 * gray_img / np.max(gray_img)
    return gray_img

def absolute_diff(img, value=0, normalise=False, configure=False):
    """Returns an image which is the absolute difference between value and pixel intensity
    """
    if configure:
        param_dict = {'value':[100,1,255,1], 'normalise':[0, 0, 1, 1]}
        gui = ConfigGui(img, absolute_diff, param_dict)
        img = absolute_diff(img, **gui.reduced_dict)
        gui.app.quit()
    else:
        subtract_frame = value*np.ones(np.shape(img), dtype=np.uint8)  
        frame1 = cv2.subtract(subtract_frame, img)
        frame1 = cv2.normalize(frame1, frame1 ,0,255,cv2.NORM_MINMAX)
        frame2 = cv2.subtract(img, subtract_frame)
        frame2 = cv2.normalize(frame2, frame2,0,255,cv2.NORM_MINMAX)
        img = cv2.add(frame1, frame2)

        if normalise == True:
            img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

    return img

#---------------------------------------------------------
# Not actively used or tested. kept for historical reasons #---------------------------------------------------------


def watershed(img, watershed_threshold=0.5, block_size=5, constant=0,
              invert=False):
    d = depth(img)
    if d == 3:
        grayscale_img = bgr_to_gray(img)
    else:
        grayscale_img = img.copy()
        img = gray_to_bgr(
            img)

    binary_img = adaptive_threshold(grayscale_img, block_size=block_size,
                                    constant=constant, invert=invert)

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


