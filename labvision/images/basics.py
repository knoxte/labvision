import cv2
import matplotlib.pyplot as plt
import numpy as np
from qtwidgets.config import get_monitor_size
from labvision.images.geometric import get_shape
import datetime

from labvision.custom_exceptions import NotImageError

__all__ = [
    'display',
    'Displayer',
    'read_img',
    'load',
    'read',
    'write_img',
    'save',
    'write'
]

def setupWindow(image,title=''):
    img_shape = get_shape(image)
    if (img_shape[2] != 1) and (img_shape[2] != 3):
        raise NotImageError()

    w,h=get_monitor_size()
    
    w_scale = 0.75*w / img_shape[1]
    h_scale = 0.75*h / img_shape[0]

    if w_scale >= h_scale:
        scale = w_scale
    else:
        scale = h_scale
       

    cv2.namedWindow(title, cv2.WINDOW_NORMAL)#, cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow(title, int(scale*img_shape[1]), int(scale*img_shape[0]))
    cv2.moveWindow(title, int(0.125*w), int(0.075*h))
    

Pt = tuple[int, int]
def display(image : np.ndarray, title : str=' ', padding: int=100) -> list[Pt]: 
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
    setupWindow(image, title=title)    

    display_points = []
    def left_mouse_click(event, x : int, y : int, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            display_points.append((x,y))        
    cv2.setMouseCallback(title,left_mouse_click)
    
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return display_points

class Displayer:
    
    def __init__(self, img: np.ndarray, title: str=''):
        """A OpenCV window where the image can be updated.

        Parameters
        ----------
        img : np.ndarray
            initial image to initialise with
        title : str, optional
            name of the window.
        """
        self.active = True
        self.window_name = title
        setupWindow(img, title=title)

    def update_im(self, img):
        cv2.imshow(self.window_name, img)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            self.active = False
            cv2.destroyAllWindows()


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


def write_img(img : np.ndarray, filename : str, addtimestamp=False):
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
    if addtimestamp:
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        _, ext = os.splitext(filename)
        filename = filename[:-len(ext)] + timestamp + ext

    ret = cv2.imwrite(filename, img)
    if not ret:
        raise Exception('Could not write image')


save = write_img
write = write_img



