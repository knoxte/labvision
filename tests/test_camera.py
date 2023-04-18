from labvision.camera import Camera

def test_camera_get_frame():
    with Camera(0) as cam:
        img = cam.get_frame()
    assert np.shape(img)