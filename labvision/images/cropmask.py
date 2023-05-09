from labvision.images.geometric import get_shape
from typing import Tuple
from qtwidgets.config import SelectShapeGui
import numpy as np
import cv2


Pts = Tuple[Tuple[int,int],Tuple[int,int]]

def viewer(img, shape='rect', handle_rad=5):
    """viewer gives you a quick way to work out the coords for your crop or mask

    The points are printed to the command line and should be entered into cropbox
    of pts in the appropriate mask

    Parameters
    ----------
    img : np.ndarray - image to be cropped or masked
    shape : 'rect', 'circle', 'ellipse', 'polygon'   
    """
    select=SelectShapeGui(img, shape=shape, handle_rad=handle_rad)
    return select.pts
    

def crop(frame, cropbox):
    """crop a frame

    Parameters
    ----------
    frame : colour or grayscale frame
    cropbox : points defining box to be cropped. Should look like:

            cropbox = ((x1,y1),(x2,y2))

        where (x1,y1) is top left corner and (x2,y2) is bottom right corner

    Returns
    -------
    _type_
        _description_
    """
    if get_shape(frame)[2] == 3:
        frame=frame[cropbox[0][1]:cropbox[1][1],
                    cropbox[0][0]: cropbox[1][0],:]
    else:
        assert get_shape(frame)[2] == 1, 'Not valid frame depth'
        frame=frame[cropbox[0][1]:cropbox[1][1],
                cropbox[0][0]: cropbox[1][0]]
    return frame

"""Masking

To create a mask send a shape and set of points to the appropriate shape
You can combine them with combine_mask and apply it to an image with apply_mask
"""

def mask_ellipse(shape : Tuple[int,int], pts : Pts):
    """create elliptical mask

    Parameters
    ----------
    shape : shape of image to be masked use np.shape(img)
    pts : Tuple of tuples like ((x1,y1),(x2,y2)) upper left and bottom right point of rectangle containing ellipse

    Returns
    -------
    binary image
    """

    mask = _create_zeros_mask(shape)
    ellipse = np.array([[pts[0][0],pts[0][1]],[pts[0][0],pts[1][1]],[pts[1][0],pts[1][1]],[pts[1][0],pts[0][1]]])
    rect=cv2.minAreaRect(ellipse)
    mask = cv2.ellipse(mask,rect,255,thickness=-1)
    return mask

def mask_polygon(shape : Tuple[int,int], pts : Pts):
    """create polygonal mask

    polygon has as many points as are contained in pts

    Parameters
    ----------
    shape : Tuple[int,int]
        _description_
    pts : Pts
        ((x1,y1),(x2,y2),(x3,y3),(x4,y4),(x5,y5)) ==> a pentagon

    Returns
    -------
    binary image
    """
    mask = _create_zeros_mask(shape)
    #calculate mask given points
    poly = []
    for point in pts:
        poly.append([point[0],point[1]])
    mask = cv2.fillPoly(mask,[np.array(poly, np.int32)],(255,255,255))
    return mask

def mask_circle(shape : Tuple[int,int], pts : Pts):
    """create circular mask

    Parameters
    ----------
    shape : shape of image to be masked use np.shape(img)
    pts : Tuple of tuples like ((x1,y1),(x2,y2)) upper left and bottom right point

    Returns
    -------
    binary image
    """
    mask = _create_zeros_mask(shape)

    radius = ((pts[1][1]-pts[0][1])**2+(pts[1][0]-pts[0][0])**2)**0.5
    mask = cv2.circle(mask, pts[0],int(radius),255,thickness=-1)
    return mask

def mask_rect(shape : Tuple[int,int], pts : Pts):
    """create rectangular mask

    Parameters
    ----------
    shape : shape of image to be masked use np.shape(img)
    pts : Tuple of tuples like ((x1,y1),(x2,y2)) upper left and bottom right point

    Returns
    -------
    binary image
    """
    mask = _create_zeros_mask(shape)
    mask = cv2.rectangle(mask, pts[0], pts[1], 255, thickness=-1)
    return mask

def combine_mask(mask1, mask2):
    """add two masks together

    Parameters
    ----------
    mask1 : binary mask
    mask2 : binary mask

    Returns
    -------
    combined mask
    """
    return cv2.add(mask1, mask2)

def apply_mask(img, mask):
    """Use a mask to mask an image"""
    return cv2.bitwise_and(img, mask)

def _create_zeros_mask(shape : Tuple[int, int]):
    zeros_mask = np.zeros(shape, dtype=np.uint8)
    return zeros_mask

