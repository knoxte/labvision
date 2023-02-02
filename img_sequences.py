import sys

sys.path.append('..')
sys.path.append('.')

import labvision.video as labvid
import labvision.images as labimg
import cv2

path='/home/ppzmis/Videos/'
path2='home/ppzmis/Pictures/'
filename = 'test.MP4'

readvid = labvid.ReadVideo(path + filename)

for i, img in enumerate(readvid):
    #labimg.basics.display(img)
    
    num = '0'*(5-len(str(i))) + str(i)
    labimg.basics.write_img(img, path + filename[:-4] + num + '.png')
    
