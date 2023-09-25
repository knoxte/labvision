
from labvision.camera import Camera
from labvision.camera.camera_config import CameraProperty
import numpy as np

"""Warning these tests require a USB camera attached!"""

def test_camera_get_frame():
    with Camera(0) as cam:
        img = cam.get_frame()
    assert np.shape(img), 'This test requires a USB camera to be attached'

