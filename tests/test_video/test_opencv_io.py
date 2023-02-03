import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from unittest import TestCase
import labvision.video as video
import labvision.images as imgs
import numpy as np

data_dir = 'labvision/data/'

mp4_videopath = os.path.join(data_dir, 'SampleVideo.mp4')
avi_videopath = os.path.join(data_dir, 'SampleVideo.avi')
mkv_videopath = os.path.join(data_dir, 'SampleVideo.mkv')
png_seqpath = os.path.join(data_dir, 'pngs/SampleVideo*.png')
jpg_seqpath = os.path.join(data_dir, 'jpgs/SampleVideo*.jpg')
tiff_seqpath = os.path.join(data_dir, 'tiffs/SampleVideo*.tiff')
single_img = os.path.join(data_dir, 'pngs/SampleVideo1.png')


class TestReadVideo(TestCase):
    def test_read_video_frame_mp4(self):
        """Check working with mp4"""
        vid = video.ReadVideo(mp4_videopath)
        frame = vid.read_next_frame()
        self.assertTrue(np.shape(frame) == (1080, 1920, 3))
    
    def test_read_video_frame_avi(self):
        """Check working with avi"""
        vid = video.ReadVideo(avi_videopath)
        frame = vid.read_next_frame()
        self.assertTrue(np.shape(frame) == (1080, 1920, 3))
    
    def test_read_video_frame_mkv(self):
        """Check working with mkv"""
        vid = video.ReadVideo(png_seqpath)
        frame = vid.read_next_frame()
        self.assertTrue(np.shape(frame) == (1080, 1920, 3))

    def test_read_png_frames(self):
        """Check working with pngs"""
        vid = video.ReadVideo(png_seqpath)
        frame = vid.read_next_frame()
        self.assertTrue(np.shape(frame) == (1080, 1920, 3))
    
    def test_read_jpg_frames(self):
        """Check working with jpgs"""
        vid = video.ReadVideo(jpg_seqpath)
        frame = vid.read_next_frame()
        self.assertTrue(np.shape(frame) == (1080, 1920, 3))
    
    def test_read_tiff_frames(self):
        """Check working with tiffs"""
        vid = video.ReadVideo(tiff_seqpath)
        frame = vid.read_next_frame()
        self.assertTrue(np.shape(frame) == (1080, 1920, 3))

    def test_read_vid_props(self):
        """Test we are reading video properties"""
        vid = video.ReadVideo(mp4_videopath)
        self.assertTrue(vid.num_frames == 241)
    
    def test_read_seq_props(self):
        """Test we are reading the properties of img sequence.
        
        png_path should only find files named SampleVideo....
        """
        vid = video.ReadVideo(png_seqpath)
        self.assertTrue(vid.num_frames == 4)
    
    def test_read_single_img(self):
        """Check working with single imgs"""
        vid = video.ReadVideo(single_img)
        frame = vid.read_next_frame()
        self.assertTrue(vid.num_frames == 1)

    




        