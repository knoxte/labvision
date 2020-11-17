import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from .draw import draw_filled_polygon

__all__ = [
    'BBox',
    'crop',
    'mask',
    'crop_and_mask',
    'crop_circle',
    'crop_polygon',
    'crop_rectangle'
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
        self.setup(im)

    def setup(self, im, width=1280, height=720):
        self.master = tk.Tk()
        self.master.wm_title("Crop")
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        label = tk.Label(self.frame, text="Click to add points")
        label.pack()

        self.canvas = tk.Canvas(self.frame, width=width,
                                height=height)
        self.shape = self.create_shape()
        self.canvas.pack()

        image = Image.fromarray(im)
        self.h_ratio = image.height / height
        self.w_ratio = image.width / width
        image = image.resize((width, height))
        image = ImageTk.PhotoImage(image)

        self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
        self.canvas.bind("<Button-1>", self.mouse1_callback)
        self.canvas.bind("<Button-2>", self.mouse2_callback)
        self.canvas.bind("<Button-3>", self.mouse3_callback)
        self.master.bind("<Return>", self.return_callback)

        undo_button = tk.Button(self.frame, text='Undo (Right Click)',
                                command=self.undo)
        undo_button.pack(side=tk.LEFT, fill=tk.BOTH)
        finished_button = tk.Button(self.frame, text='Finished (Return)',
                                    command=self.finish)
        finished_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        reset_button = tk.Button(self.frame, text='Reset (Middle Click)',
                                 command=self.reset)
        reset_button.pack(side=tk.LEFT, fill=tk.BOTH)
        tk.mainloop()

    def undo(self):
        if len(self.points) == 2:
            self.reset()
        elif len(self.points) > 2:
            self.points.pop()
            self.points.pop()
            self.canvas.delete(self.shape)
            self.shape = self.create_shape(self.points)

    def reset(self):
        self.points = []
        self.canvas.delete(self.shape)
        self.shape = self.create_shape()

    def finish(self):
        self.finish_crop()
        self.master.quit()
        self.master.destroy()

    def update(self,x,y):
        #stub to be implemented in child
        pass

    def mouse1_callback(self, event):
        x = event.x
        y = event.y
        self.update(x, y)

    def mouse2_callback(self, event):
        self.reset()

    def mouse3_callback(self, event):
        self.undo()

    def return_callback(self, event):
        self.finish()


class CropRect(CropBase):
    def __init__(self,im):
        super(CropRect, self).__init__(im)

    def create_shape(self, points=[0, 0, 0, 0]):
        return self.canvas.create_rectangle(points, outline='black',
                                          width=2)

    def update(self, x, y):
        self.canvas.delete(self.shape)
        #self.shape = self.create_shape(self.points)
        #if len(self.points) < 4:
        self.points.append(x)
        self.points.append(y)

        if len(self.points) == 4:
            self.shape = self.create_shape(self.points)

    def finish_crop(self):
        mask = np.zeros_like(self.im[:, :, 0], dtype=np.uint8)
        points = np.array(self.points)
        points = points.reshape(len(points) // 2, 2)
        points[:, 0] = points[:, 0] * self.w_ratio
        points[:, 1] = points[:, 1] * self.h_ratio
        bbox = BBox(min(points[:, 0]), max(points[:, 0]), min(points[:, 1]),
                    max(points[:, 1]))
        cv2.rectangle(mask, (points[0,0], points[0,1]),(points[1,0], points[1,1]),
                     color=(255, 255, 255), thickness=-1)
        points[:, 0] -= bbox.xmin
        points[:, 1] -= bbox.ymin
        self.result = CropResult(bbox, mask, points=points)


class CropPolygon(CropBase):
    def __init__(self,im):
        super(CropPolygon, self).__init__(im)

    def create_shape(self, points=[0,0]):
        return self.canvas.create_polygon(points, outline='black',
                                                  width=2)

    def update(self, x, y):
        self.points.append(x)
        self.points.append(y)
        self.canvas.delete(self.shape)
        self.shape = self.create_shape(self.points)

    def finish_crop(self):
        mask = np.zeros_like(self.im[:, :, 0], dtype=np.uint8)
        points = np.array(self.points)
        points = points.reshape(len(points) // 2, 2)
        points[:, 0] = points[:, 0] * self.w_ratio
        points[:, 1] = points[:, 1] * self.h_ratio
        bbox = BBox(min(points[:, 0]), max(points[:, 0]), min(points[:, 1]),
                    max(points[:, 1]))
        cv2.fillPoly(mask, pts=np.array([points], dtype=np.int32),
                     color=(255, 255, 255))
        points[:, 0] -= bbox.xmin
        points[:, 1] -= bbox.ymin
        self.result = CropResult(bbox, mask, points=points)


class CropCircle(CropBase):
    def __init__(self, im):
        self.selections = []
        super(CropCircle, self).__init__(im)

    def create_shape(self, points=[0,0,0,0]):
        return self.canvas.create_oval(points, outline='black',
                                              width=2)
    def update(self, x, y):
        if len(self.points) < 6:
            self.points.append(x)
            self.points.append(y)
            self.selections.append(
                self.canvas.create_oval([x - 2, y - 2, x + 2, y + 2],
                                        outline='red', width=2))
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
        mask = np.zeros_like(self.im[:, :, 0], dtype=np.uint8)
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
        self.master.quit()

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