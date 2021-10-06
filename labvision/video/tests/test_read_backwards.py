from labvision import video, images

vid = video.ReadVideo("/home/ppxjd3/Code/labvision/labvision/data/numbered_video.mp4")

frame_numbers = [0, 1, 2, 3, 10, 11, 20, 21, 20, 19, 18]


for f in frame_numbers:
    frame1 = vid.read_frame(f)
    frame2 = vid.read_frame(f)
    frame = images.hstack(frame1, frame2)
    images.display(frame, title=f'{f}')


