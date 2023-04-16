from labvision.camera import WebCamera
from labvision.images.basics import display

cam = WebCamera()
display(cam.get_frame())
