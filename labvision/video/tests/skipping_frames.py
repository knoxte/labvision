from labvision import video, images

vid = video.ReadVideo("/home/ppxjd3/Code/labvision/labvision/data/numbered_video.mp4", frame_range=(0, 100, 10))

for f in range(vid.num_frames):
    frame = vid.read_next_frame()
    images.display(frame, f"{f}")