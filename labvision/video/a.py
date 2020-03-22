from labvision.video.opencv_io import ReadVideo
from labvision.images.basics import display

for img in ReadVideo(filename='/home/mike/Videos/my_video-3.avi', frame_range=(2,22,5)):
    display(img)

readVid = ReadVideo(filename='/home/mike/Videos/my_video-3.avi', frame_range=(2,22,5))
readVid.read_frame(2)
#readVid.read_frame(8)

