import cv2
import numpy as np
from .draw import draw_filled_polygon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QErrorMessage, QLabel
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPolygonF, QPen
from qtwidgets import QImageViewer
import sys

__all__ = [
    'BBox',
    'crop',
    'mask',
    'crop_and_mask',
    'crop_circle',
    'crop_polygon',
    'crop_rectangle',
]


class BBox:
    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def to_tuple(self):
        return ((self.xmin, self.ymin), (self.xmax, self.ymax))

    def to_list(self):
        return [[self.xmin, self.ymin], [self.xmax, self.ymax]]

    def __str__(self):
        s = "BBOX: xmin = {}, xmax = {}, ymin = {}, ymax = {}".format(self.xmin, self.xmax, self.ymin, self.ymax)
        return s


def crop(im, bbox):
    """
    Crops an image to a bounding box

    Parameters
    ----------
    im: input image
        Any number of channels

    bbox: BBox instance
    """
    if len(np.shape(im)) == 3:
        out = im[bbox.ymin:bbox.ymax, bbox.xmin:bbox.xmax, :]
    else:
        out = im[bbox.ymin:bbox.ymax, bbox.xmin:bbox.xmax]
    return out


def mask(im, mask_im, color='black'):
    """
    Masks pixels in an image.

    Pixels in the image that are 1 in the mask are kept.
    Pixels in the image that are 0 in the mask are set to 0.

    Parameters
    ----------
    im: The input image
        Any number of channels

    mask_im: Mask image
        Same height and width as img containing 0 or 1 in each pixel

    color: Color of the mask

    Returns
    -------
    out: The masked image
        Same dimensions and type as img
    """
    out = cv2.bitwise_and(im, im, mask=mask_im)
    if color == 'white':
        add = cv2.cvtColor(~mask_im, cv2.COLOR_GRAY2BGR)
        out = cv2.add(out, add)
    return out


def crop_and_mask(im, bbox, mask_im, mask_color='black'):
    im = mask(im, mask_im, mask_color)
    im = crop(im, bbox)
    return im


def crop_polygon(im):
    crop_object = CropPolygon(im)
    return crop_object.result


def crop_circle(im):
    crop_object = CropCircle(im)
    return crop_object.result

def crop_rectangle(im):
    crop_object = CropRect(im)
    return crop_object.result


class CropBase:

    def __init__(self, im):
        self.im = im
        self.points = []
        self.selections = []
        self.setup()

    def setup(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.image_viewer = QImageViewer()
        self.image_viewer.setImage(self.im)
        self.image_viewer.leftMouseButtonReleased.connect(self.mouse1_callback)
        self.image_viewer.rightMouseButtonReleased.connect(self.mouse3_callback)
        self.image_viewer.keyPressed.connect(self.keypress_callback)
        self.shape = self.create_shape()
        self.vbox = QVBoxLayout()
        self.label = QLabel(self.message)
        self.vbox.addWidget(self.label)

        self.vbox.addWidget(self.image_viewer)

        self.hbox = QHBoxLayout()
        self.undo_button = QPushButton('Undo (Right Mouse)')
        self.undo_button.clicked.connect(self.undo)
        self.hbox.addWidget(self.undo_button)
        self.enter_button = QPushButton('Finish (Return Key)')
        self.enter_button.clicked.connect(self.finish)
        self.hbox.addWidget(self.enter_button)
        self.reset_button = QPushButton('Reset')
        self.reset_button.clicked.connect(self.reset)
        self.hbox.addWidget(self.reset_button)

        self.vbox.addLayout(self.hbox)

        self.window.setLayout(self.vbox)
        self.window.show()
        self.app.exec_()

    def mouse1_callback(self, x, y):
        self.add_selection(x, y)
        self.update(int(x), int(y))

    def mouse3_callback(self, event):
        self.undo()

    def keypress_callback(self, event):
        if event.key() == Qt.Key_Return:
            self.finish()

    def undo(self):
        if len(self.selections) > 0:
            self.remove_selection(-1)
        if len(self.points) == 2:
            self.reset()
        elif len(self.points) == 0:
            pass
        else:
            self.points.pop()
            self.points.pop()
        if self.shape is not None:
            self.image_viewer.scene.removeItem(self.shape)

    def reset(self):
        self.points = []
        for i in range(len(self.selections)):
            self.remove_selection(-1)
        if self.shape is not None:
            self.image_viewer.scene.removeItem(self.shape)
        self.shape = self.create_shape()

    def finish(self):
        try:
            self.finish_crop()
            self.app.exit()
        except Exception as e:

            error = QErrorMessage(self.window)
            error.setWindowTitle("Cropping Error")
            error.showMessage("Select more points")
            raise Exception(e)



    def create_shape(self, points=()):
        """This function should add the shape """
        pass

    def finish_crop(self):
        """This function should be overloaded"""
        pass

    def update(self, x, y):
        """This function should be overloaded"""
        pass

    def remove_selection(self, index):
        selection = self.selections[index]
        if selection is not None:
            self.image_viewer.scene.removeItem(selection)
            self.selections.pop(-1)

    def add_selection(self, x, y):
        rect = QRectF(QPointF(x - 2, y - 2), QPointF(x + 2, y + 2))
        self.selections.append(
            self.image_viewer.scene.addEllipse(rect, QPen(Qt.green, 2)))

    def create_empty_mask(self):
        if len(self.im.shape) == 2:
            mask = np.zeros_like(self.im, dtype=np.uint8)
        else:
            mask = np.zeros_like(self.im[:, :, 0], dtype=np.uint8)
        return mask


class CropPolygon(CropBase):
    def __init__(self, im):
        self.message = 'Select polygon vertices with left mouse'
        CropBase.__init__(self, im)


    def create_shape(self, points=[0, 0]):
        qpoints = [QPointF(int(p), int(q)) for p, q in zip(points[::2], points[1::2])]
        polygon = QPolygonF(qpoints)
        return self.image_viewer.scene.addPolygon(polygon, QPen(Qt.red, 3))

    def update(self, x, y):
        self.points.append(x)
        self.points.append(y)
        self.image_viewer.scene.removeItem(self.shape)
        self.shape = self.create_shape(self.points)

    def finish_crop(self):
        mask = self.create_empty_mask()
        points = np.array(self.points)
        points = points.reshape(len(points) // 2, 2)
        points[:, 0] = points[:, 0]
        points[:, 1] = points[:, 1]
        bbox = BBox(min(points[:, 0]), max(points[:, 0]), min(points[:, 1]),
                    max(points[:, 1]))
        cv2.fillPoly(mask, pts=np.array([points], dtype=np.int32),
                     color=(255, 255, 255))
        points[:, 0] -= bbox.xmin
        points[:, 1] -= bbox.ymin
        self.result = CropResult(bbox, mask, points=points)

    def undo(self):
        if len(self.selections) > 0:
            self.remove_selection(-1)
        if len(self.points) == 2:
            self.reset()
        elif len(self.points) == 0:
            pass
        else:
            self.points.pop()
            self.points.pop()
            self.image_viewer.scene.removeItem(self.shape)
            self.shape = self.create_shape(self.points)


class CropRect(CropBase):
    def __init__(self, im):
        self.message = "Select top-left and bottom-right vertices with left mouse"
        CropBase.__init__(self, im)

    def create_shape(self, points=[0, 0, 0, 0]):
        poly = QRectF(QPointF(points[0], points[1]),
                      QPointF(points[2], points[3]))
        return self.image_viewer.scene.addRect(poly, QPen(Qt.red, 4))

    def update(self, x, y):
        self.image_viewer.scene.removeItem(self.shape)
        self.points.append(x)
        self.points.append(y)

        if len(self.points) == 4:
            self.shape = self.create_shape(self.points)

    def finish_crop(self):
        mask = self.create_empty_mask()
        points = np.array(self.points)
        points = points.reshape(len(points) // 2, 2)
        points[:, 0] = points[:, 0]
        points[:, 1] = points[:, 1]
        bbox = BBox(min(points[:, 0]), max(points[:, 0]), min(points[:, 1]),
                    max(points[:, 1]))
        cv2.rectangle(mask, (points[0,0], points[0,1]),(points[1,0], points[1,1]),
                     color=(255, 255, 255), thickness=-1)
        points[:, 0] -= bbox.xmin
        points[:, 1] -= bbox.ymin
        self.result = CropResult(bbox, mask, points=points)


class CropCircle(CropBase):
    def __init__(self, im):
        self.message = 'Select three distant points on the edge of the circle using the left mouse'
        CropBase.__init__(self, im)

    def create_shape(self, points=[0,0,0,0]):
        rect = QRectF(QPointF(points[0], points[1]),
                      QPointF(points[2], points[3]))
        return self.image_viewer.scene.addEllipse(rect, QPen(Qt.red, 3))

    def update(self, x, y):
        if len(self.points) < 6:
            self.points.append(x)
            self.points.append(y)
        if len(self.points) == 6:
            xc, yc, r = self.find_circle()
            self.shape = self.create_shape([xc - r, yc - r, xc + r, yc + r])
            self.xc, self.yc, self.r = xc, yc, r

    def find_circle(self):
        "http://www.ambrsoft.com/trigocalc/circle3d.htm"
        x1,y1,x2,y2,x3,y3 = self.points

        A = np.linalg.det([[x1, y1, 1], [x2, y2, 1], [x3, y3, 1]])
        B = -np.linalg.det(
            [[x1 ** 2 + y1 ** 2, y1, 1], [x2 ** 2 + y2 ** 2, y2, 1],
             [x3 ** 2 + y3 ** 2, y3, 1]])
        C = np.linalg.det(
            [[x1 ** 2 + y1 ** 2, x1, 1], [x2 ** 2 + y2 ** 2, x2, 1],
             [x3 ** 2 + y3 ** 2, x3, 1]])
        D = -np.linalg.det(
            [[x1 ** 2 + y1 ** 2, x1, y1], [x2 ** 2 + y2 ** 2, x2, y2],
             [x3 ** 2 + y3 ** 2, x3, y3]])

        x0 = -(0.5 * B / A)
        y0 = -(0.5 * C / A)
        r = np.sqrt((B ** 2 + C ** 2 - 4 * A * D) / (4 * A ** 2))
        return x0, y0, r

    def finish_crop(self):
        mask = self.create_empty_mask()
        cv2.circle(mask, (int(self.xc), int(self.yc)), int(self.r),
                   [255, 255, 255], thickness=-1)
        xmin = int(self.xc - self.r)
        xmax = int(self.xc + self.r)
        ymin = int(self.yc - self.r)
        ymax = int(self.yc + self.r)
        if xmin < 0:
            xmin = 0
        if ymin < 0:
            ymin = 0
        bbox = BBox(xmin, xmax, ymin, ymax)
        points = [self.xc, self.yc, self.r]
        self.result = CropResult(bbox, mask, circle=points)


class CropResult:

    def __init__(self, bbox, mask, points=None, circle=None):
        self.bbox = bbox
        self.mask = mask
        self.points = points
        if circle is not None:
            self.circle = circle

    def __str__(self):
        return str(
            "Crop result containing where appropriate: \n "
            "   bbox: BBox object containing xmin, xmax, ymin, ymax attributes \n"
            "   mask: a mask to apply to an image \n "
            "   points: a list of points ([:, 0] contains x, [:, 1] contains y \n"
            "   circle: a list containing xc, yc, and r for the cropping circle")

def create_mask_from_polygon(im, points):
    msk = np.zeros_like(im, dtype=np.uint8)
    msk = draw_filled_polygon(msk, points, (255, 255, 255))
    return msk[:, :, 0]