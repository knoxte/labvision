import cv2
import matplotlib.pyplot as plt
import numpy as np

from labvision.custom_exceptions import NotImageError

__all__ = [
    'display',
    'read_img',
    'load',
    'read',
    'write_img',
    'save',
    'write'
]
    
Pt = tuple[int, int]
def display(image : np.ndarray, title : str=' ') -> list[Pt]: 
    """display

    Displays a single image in pop up window. You can click as many times as you want storing the (x,y) coords in a list. This is returned when the user presses a key to close the window.

    Example
    -------
    pts=display(img)

    Parameters
    ----------
    image : np.ndarray
        _description_
    title : str, optional
        title bar of image, by default ' '
    resolution : Pt, optional
        window resolution, by default (960, 540)

    Returns
    -------
    list[Pt]
        
    """
    img_shape = np.shape(image)
    if np.size(img_shape) == 2:
        resolution =(img_shape[1],img_shape[1])
    elif np.size(img_shape) == 3:
        resolution = (img_shape[1],img_shape[0])
    else:
        raise NotImageError()

    cv2.namedWindow(title, cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow(title, *resolution)
 
    display_points = []
    def left_mouse_click(event, x : int, y : int, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            display_points.append((x,y))        
    cv2.setMouseCallback(title,left_mouse_click)
    
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return display_points


def read_img(filepath, grayscale=False, alpha=False):
    """
    Reads an image from a filepath.

    The image should be in the working directory or a full path of image
    should be given.

    Parameters
    ----------
    filepath: filepath of the image

    flag: Specifies how the image is read
        1: Loads a color image. Any transparency will be neglected.
        0: Loads image in grayscale mode.
        -1: Loads image including alpha channel

    Returns
    -------
    img: output image
        Number of channels will be determined by the chosen flag.
        Equal to None if filepath does not exist
        Color images will have channels stored in BGR order

    """
    assert grayscale * alpha == 0, 'Only one of alpha and grayscale can be True'
    if grayscale:
        flag = 0
    elif alpha:
        flag = -1
    else:
        flag = 1
    img = cv2.imread(filepath, flag)
    return img


load = read_img
read = read_img


def write_img(img : np.ndarray, filename : str):
    """write_img

    Saves an image to a specified file.
    The image format is chosen based on the filename extension

    Example
    -------
    write_img(img, filename)

    Parameters
    ----------
    img: Image to be saved

    filename: Name of the file

    Notes
    -----
    Only 8-bit single channel or 3-channel (BGR order) can be saved. If
    the format, depth or channel order is different convert it first.

    It is possible to store PNG images with an alpha channel using this
    function. To do this, create 8-bit 4-channel image BGRA, where the alpha
    channel goes last. Fully transparent pixels should have alpha set to 0,
    fully opaque pixels should have alpha set to 255

    """
    ret = cv2.imwrite(filename, img)
    if not ret:
        raise Exception('Could not write image')


save = write_img
write = write_img



