from tests import binary_single_circle, grayscale_img_test
from labvision.images.transforms import brightness_contrast, distance, gamma

def test_gamma():
    img = gamma(grayscale_img_test(), gamma=2)
    assert img[30,50] == 55, 'Test gamma gave wrong value'

def test_brightness_contrast():
    img = brightness_contrast(grayscale_img_test(), brightness=10, contrast=-2)
    assert img[30,50] == 14, 'Test brightness contrast gave wrong value'

def test_distance_transform():
    """Tests distance transform. Draws single binary circle cx,cy = 50,50 of radius 30 on blank image (100,100) and tests value of central pixel in circle which should be the rad in pixels."""
    img = distance(binary_single_circle(), normalise=False)
    assert int(img[50, 50]) == 29