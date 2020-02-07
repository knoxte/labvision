import os
from unittest import TestCase
from labvision import data_dir, video
import numpy as np

videopath = os.path.join(data_dir, 'SampleVideo.mp4')


class TestReadVideo(TestCase):
    def test_read_video_frame(self):
        vid = video.ReadVideo(videopath)
        frame = vid.read_next_frame()
        self.assertTrue(type(frame) == np.ndarray)

    def test_video_slicerator(self):
        vid = video.ReadVideo(videopath)
        for frame in vid[:2]:
            self.assertTrue(type(frame) == np.ndarray)