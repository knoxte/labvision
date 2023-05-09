
import numpy as np
from labvision.images.cropmask import viewer

pts=viewer(np.zeros((2000, 2000, 3)), shape='polygon')
print(pts)
