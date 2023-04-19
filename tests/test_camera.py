
from labvision.camera import Camera
from labvision.camera.camera_config import CameraProperty
import numpy as np

"""Warning these tests require a USB camera attached!"""

def test_camera_get_frame():
    with Camera(0) as cam:
        img = cam.get_frame()
    assert np.shape(img)

def test_camera_get_properties():
    with Camera(0) as cam:
        properties = cam.get_props()
    assert 'width' in properties.keys()

def test_camera_get_property():
    with Camera(0) as cam:
        property = cam.get_property(property = CameraProperty.WIDTH)
    assert type(property) == float
