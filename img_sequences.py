import sys

sys.path.append('..')
sys.path.append('.')

import labvision.video as labvid
import labvision.images as labimg
import cv2
import numpy as np


path='home/ppzmis/Videos/imgs/'
vid = labvid.ReadVideo(filename='/home/ppzmis/Videos/imgs/001.jpg')
img = vid.read_frame()
labimg.display(img)
img = vid.read_frame()
img = vid.read_frame()
img = vid.read_frame(n=0)

labimg.display(img)

    
    #num = '0'*(5-len(str(i))) + str(i)
    #labimg.basics.write_img(img, path + filename[:-4] + num + '.png')
    
