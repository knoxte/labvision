from .colours import *
import cv2
import numpy as np
from matplotlib import cm
from scipy import spatial

__all__ = [
    "draw_filled_polygon",
    "draw_circle",
    "draw_circles",
    "draw_circles_with_scale",
    "draw_delaunay_tess",
    "draw_polygon",
    "draw_polygons",
    "draw_voronoi_cells",
    "draw_contours"
]

def draw_circle(img, cx, cy, rad, color=YELLOW, thickness=2):
    """Draws single Circle on an image

    :param img:RGB image as np.ndarray
    :param cx: x centre of circle
    :param cy: y centre of circle
    :param rad: radius of circle
    :param color: colour of circle --> see colors.py for enumerated types
    :param thickness: thickness of circle line. -1 fills the circle.

    :return: image with circle drawn on it

    """
    assert len(np.shape(img)) == 3, "Image needs to be 3 channel"
    cv2.circle(img, (int(cx), int(cy)), int(rad), color, thickness)
    return img

def draw_polygon(img: np.ndarray, vertices, color=RED, thickness=1):
    """
    Draws a closed polygon on an image from a list of vertices

    Parameters
    ----------
    img: input rgb image (np.ndarray)
       

    vertices: array of N vertices
        Shape (N, 2) where
            vertices[:, 0] contains x coordinates
            vertices[:, 1] contains y coordinates
            e.g vertices = np.array([[x1,y1],[x2,y2].......[xn,yn]])

    color: BGR tuple
        if input image is grayscale then circles will be black

    thickness: int
        Thickness of the lines. -1 will fill polygon

    Returns
    -------
    output_img: output image
        Same shape and type as input image
    """
    assert len(np.shape(img)) == 3, "Image needs to be 3 channel"
    vertices = vertices.astype(np.int32)
    vertices = vertices.reshape((-1,1,2))
    if thickness == -1:
        output_img = cv2.fillPoly(img, [vertices], color)
    else:
        output_img = cv2.polylines(img, [vertices], True, color, thickness=thickness)
    return output_img

def draw_contours(img, contours, color=RED, thickness=1):
    """
    Takes a set of contours and draws them on an image

    :param img: rgb image (np.ndarray)
    :param contours: a set of contours produced by find_contours
    :param col: colour -> See colors.py for defined values. Can also pass list of colors same length as contours to specify colour of each contour in order.
    :param thickness: -> thickness of line. -1 will fill enclosed contour

    :return: Image with contours draw on it.

    """

    assert len(np.shape(img)) == 3, "Image needs to be 3 channel"
    if (np.size(np.shape(color)) == 0) | (np.size(np.shape(color)) == 1):
        img = cv2.drawContours(img, contours, -1, color, thickness)
    else:
        assert len(color) == len(contours), "If supplying colour for each contour must be same number of colours as contours"
        for i, contour in enumerate(contours):
            img = cv2.drawContours(img, contour, -1, color[i], thickness)
    return img

def draw_delaunay_tess(img, points, color=RED, thickness=1):
    """
    Draws the delaunay tesselation for a set of points on an image

    Parameters
    ----------
    im: input image
        Any number of channels

    points: array of N points
        Shape (N, 2).
        points[:, 0] contains x coordinates
        points[:, 1] contains y coordinates
        e.g points = np.array([[x1,y1],[x2,y2].......[xn,yn]])

    Returns
    -------
    in: annotated image
        Same shape and type as input image
    """
    assert len(np.shape(img)) == 3, "Image needs to be 3 channel"
    points = points.astype(np.int32)
    points = points.reshape((-1,1,2))
    tess = spatial.Delaunay(points)
    
    img = draw_polygons(img,
                        points[tess.simplices],
                        color=color)
                        
    return img


def draw_voronoi_cells(img, points):
    """
    Draws the voronoi cells for a set of points on an image

    Parameters
    ----------
    img: input image
        Any number of channels

    points: array of N points
        Shape (N, 2).
        points[:, 0] contains x coordinates
        points[:, 1] contains y coordinates

    Returns
    -------
    im: annotated image
        Same shape and type as input image
    """

    assert len(np.shape(img)) == 3, "Image needs to be 3 channel"
    voro = spatial.Voronoi(points)
    ridge_vertices = voro.ridge_vertices
    new_ridge_vertices = []
    for ridge in ridge_vertices:
        if -1 not in ridge:
            new_ridge_vertices.append(ridge)
    img = draw_polygons(img,
                       voro.vertices[new_ridge_vertices],
                       color=PINK)
    return img

#-----------------------------------------------------------------------------
#Kept for historical reasons but untested
#----------------------------------------------------------------------------

def draw_circles_with_scale(img, circles, values, cmap=cm.viridis, thickness=2):
    """
    NEEDS DOCSTRING

    :param img:
    :param circles:
    :param values:
    :param cmap:
    :param thickness:

    :return:

    """

    assert len(np.shape(img)) == 3, "Image needs to be 3 channel"
    for (x, y, r), v in zip(circles, values):
        col = np.multiply(cmap(v), 255)
        cv2.circle(img, (int(x), int(y)), int(r), col, thickness)
    return img

def draw_filled_polygon(img, points, color=RED):
    """
    Adds a filled polygon to an image

    :param img: np.ndarrary of dtype np.uint8
    :param points: N, 2 ndarray of corner points
    :param color: BGR color tuple or images library color
    :return: im: ndarray
    """
    return cv2.fillPoly(img, np.array([points], dtype=np.int32), color)

def draw_circles(img, circles, color=YELLOW, thickness=2):
    """
    NEEDS DOCSTRING

    :param img:
    :param circles:
    :param color:
    :param thickness:

    :return:

    """

    assert len(np.shape(img)) == 3, "Image needs to be 3 channel"
    assert len(circles) > 0, "Circles must not be empty"
    if len(np.shape(circles)) == 1:
        assert len(circles) == 3, "Circles must contain x, y, and r"
        circles = [circles]
    else:
        assert np.shape(circles)[1] == 3, "Circles must contain x, y, and r"
    for x, y, rad in circles:
        cv2.circle(img, (int(x), int(y)), int(rad), color, thickness)
    return img

def draw_polygons(img, polygons, color=RED):
    """
    Draws multiple polygons on an image from a list of polygons

    Parameters
    ----------
    img: input image
        Any number of channels

    polygons: array containing coordinates of polygons
        shape is (P, N, 2) where P is the number of polygons, N is the number
        of vertices in each polygon. [:, :, 0] contains x coordinates,
        [:, :, 1] contains y coordinates.

    color: BGR tuple

    Returns
    -------
    img: annotated image
        Same shape and type as input image
    """
    assert len(np.shape(img)) == 3, "Image needs to be 3 channel"
    for vertices in polygons:
        img = draw_polygon(img, vertices, color)
    return img
