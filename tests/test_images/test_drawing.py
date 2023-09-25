
from labvision.images.colours import WHITE
from labvision.images.draw import draw_circle, draw_contours, draw_polygon, draw_delaunay_tess, draw_voronoi_cells
from tests import rgb_img_test, contour_test, contour_test2

import numpy as np
from labvision.images.basics import display


def test_draw_circle():
    img = rgb_img_test()
    img = draw_circle(img, 100, 100, 50, color=WHITE, thickness=-1)
    assert img[120, 120, 1] == 255


def test_draw_filled_polygon():
    """Check draws filled polygon"""
    img = rgb_img_test()
    vertices = np.array([[100, 200], [500, 200],
                         [500, 600], [100, 600]], np.int32)

    img = draw_polygon(img, vertices, color=WHITE, thickness=-1)
    assert img[300, 300, 1] == 255

def test_draw_hollow_polygon():
    img = rgb_img_test()
    vertices = np.array([[100, 200], [500, 200],
                         [500, 600], [100, 600]], np.int32)

    img = draw_polygon(img, vertices, color=WHITE, thickness=3)
    assert img[200, 100, 1] == 255


def test_draw_contour():
    """Test drawing single contour"""
    contour = contour_test()
    img = rgb_img_test()
    img = draw_contours(img, contour, color=WHITE, thickness=-1)
    assert img[contour[0][0][1], contour[0][0][0], 1] == 255


def test_draw_contours():
    """Test draw multiple contours"""
    cnts = tuple([contour_test(), contour_test2()])
    img = rgb_img_test()
    img = draw_contours(img, cnts, color=WHITE, thickness=-1)
    assert img[cnts[1][0][0][1], cnts[1][0][0][0], 1] == 255

"""def test_draw_delaunay():
    Getting Segmentation fault to do with spatial.Delaunay
    
    Note - we kept getting a segmentation fault when we ran this but it turned out to be an issue with version of scipy
    points = np.array([[0, 0], [3, 4], [5, 6], [7, 7],[7,3]])
    img = np.zeros((10,10,3),dtype=np.uint8)
    img = draw_delaunay_tess(img, points)
    display(img)
    
    
    def test_draw_voronoi():
        needs implementing
    
    """