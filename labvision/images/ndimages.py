from labvision.video import ReadVideo, WriteVideo
import numpy as np


def convert_vid_ndimg(read_vid_obj, stackdepth=1):

    assert read_vid_obj.num_frames % stackdepth == 0, \
    "stackdepth not compatible with number of frames"

    ndimg = np.empty((read_vid_obj.num_frames, read_vid_obj.weight, read_vid_obj.width, 3), np.dtype('uint8'))
    for i in range(read_vid_obj.num_frames):
        ndimg[i]=read_vid_obj.read()

    if stackdepth > 1:
        ndimg = np.reshape(ndimg, (read_vid_obj.width, read_vid_obj.height, stackdepth, -1))

    return ndimg

