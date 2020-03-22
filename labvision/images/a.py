import cv2
from labvision.images import cropping
from labvision.images.basics import display


img = cv2.imread('/home/mike/PycharmProjects/labvision/labvision/data/SampleImage.jpg')

#crops= cropping.CropPolygonTest(img)
crops= cropping.CropRect(img)
print(crops.result)


