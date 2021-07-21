import numpy as np
import cv2
from labvision import images
from labequipment import arduino
from labvision import camera
import time


def crop_image_to_contour(img, rect):
    # rotate img
    angle = rect[2]
    rows, cols = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    img_rot = cv2.warpAffine(img, M, (cols, rows))

    # rotate bounding box
    rect0 = (rect[0], rect[1], 0.0)
    box = cv2.boxPoints(rect0)
    pts = np.int0(cv2.transform(np.array([box]), M))[0]
    pts[pts < 0] = 0

    # crop
    img_crop = img_rot[pts[1][1]:pts[0][1], pts[1][0]:pts[2][0]]

    img_crop = img_crop[18:-18, 18:-18]

    return img_crop


def get_com_and_midpoint(im):
    original_image = cv2.imread(im)
    greyscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    threshold_image = images.threshold(greyscale_image, 75)

    contours = images.find_contours(threshold_image)
    sorted_contours = images.sort_contours(contours)
    biggest_contour = sorted_contours[-1]

    rect = cv2.minAreaRect(biggest_contour)

    cropped_im = crop_image_to_contour(threshold_image, rect)
    colour_cropped = crop_image_to_contour(original_image, rect)

    midpoint = (int(colour_cropped.shape[0] / 2), int(colour_cropped.shape[1] / 2))

    inverted_im = cv2.bitwise_not(cropped_im)
    com = images.center_of_mass(inverted_im)

    show_com = cv2.circle(colour_cropped, com, radius=20, color=(0, 0, 255), thickness=-1)
    show_midpoint = cv2.circle(show_com, midpoint, radius=20, color=(255, 0, 0), thickness=-1)
    images.display(show_midpoint)

    return com, midpoint


def motor_combos(com, midpoint):
    xdiff = midpoint[0] - com[0]
    ydiff = midpoint[1] - com[1]
    magnitude = np.sqrt(xdiff ** 2 + ydiff ** 2)
    duration = 3 * magnitude
    if xdiff > 0:
        print('+i')
    if xdiff < 0:
        print('-i')
    if ydiff < 0:
        print('+j')
    if ydiff > 0:
        print('-j')
    if ydiff == 0 and xdiff == 0:
        print('surface is level')


motorbox = "/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_55735323935351809202-if00"


class PushButtons():
    def __init__(self):
        """ Initialise with an instance of arduino.Arduino"""
        self.ard = arduino.Arduino(port=motorbox, wait=True)

    def move_motor(self, motor_no, direction):
        """
        Generate the message to be sent to self.ard.send_serial_line
        Inputs:
        motor_no: 1, 2 or 3
        direction: either 'f', 'b' or 'stop'
        """
        message = str(motor_no) + direction
        self.ard.send_serial_line(message)


def motor_commands(command, duration):
    motors = PushButtons()
    if command == '+i':
        this = camera.QuickTimer(time_list)
        motors.move_motor(1, 'f')
        motors.move_motor(2, 'f')


test1 = PushButtons()
test1.move_motor(1, 'f')
test1.move_motor(2, 'stop')
test1.move_motor(3, 'stop')

com, midpoint = get_com_and_midpoint('box')

motor_combos(com, midpoint)
