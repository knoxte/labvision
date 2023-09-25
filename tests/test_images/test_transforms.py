from tests import binary_single_circle
from labvision.images.transforms import distance


def test_distance_transform():
    """Tests distance transform. Draws single binary circle cx,cy = 50,50 of radius 30 on blank image (100,100) and tests value of central pixel in circle which should be the rad in pixels."""
    img = distance(binary_single_circle(), normalise=False)
    assert int(img[50, 50]) == 29