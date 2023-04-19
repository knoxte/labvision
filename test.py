from labvision.camera import Camera, get_cameras_on_windows
from labvision.camera.camera_config import CameraProperty
from labvision.images import display
from tests.test_camera import test_camera_get_property

# cam = Camera(1)
# display(cam.get_frame())

cam = Camera()
display(cam.get_frame())
