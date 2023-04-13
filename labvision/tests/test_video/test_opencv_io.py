import os
import sys
import shutil
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import labvision.video as video
import labvision.images as imgs
import numpy as np
import cv2

data_dir = 'labvision/labvision/data'
mp4_videopath = os.path.join(data_dir, 'video/SampleVideo.mp4')
avi_videopath = os.path.join(data_dir, 'video/SampleVideo.avi')
mkv_videopath = os.path.join(data_dir, 'video/SampleVideo.mkv')
png_seqpath = os.path.join(data_dir, 'pngs/SampleVideo*.png')
jpg_seqpath = os.path.join(data_dir, 'jpgs/SampleVideo*.jpg')
tiff_seqpath = os.path.join(data_dir, 'tiffs/SampleVideo*.tiff')
single_img = os.path.join(data_dir, 'pngs/SampleVideo1.png')
output_filename = os.path.join(data_dir, 'video/test.mp4')


#=================================================================================
# ReadVideo Tests #=================================================================================

def test_read_video_frame_mp4():
    """Check working with mp4"""
    vid = video.ReadVideo(mp4_videopath)
    frame = vid.read_next_frame()
    assert np.shape(frame) == (1080, 1920, 3)
    
def test_read_video_frame_avi():
    """Check working with avi"""
    vid = video.ReadVideo(avi_videopath)
    frame = vid.read_next_frame()
    assert np.shape(frame) == (1080, 1920, 3)
    
def test_read_video_frame_mkv():
    """Check working with mkv"""
    vid = video.ReadVideo(png_seqpath)
    frame = vid.read_next_frame()
    assert np.shape(frame) == (1080, 1920, 3)

def test_read_png_frames():
    """Check working with pngs"""
    vid = video.ReadVideo(png_seqpath)
    frame = vid.read_next_frame()
    assert np.shape(frame) == (1080, 1920, 3)
    
def test_read_jpg_frames():
    """Check working with jpgs"""
    vid = video.ReadVideo(jpg_seqpath)
    frame = vid.read_next_frame()
    assert np.shape(frame) == (1080, 1920, 3)
    
def test_read_tiff_frames():
    """Check working with tiffs"""
    vid = video.ReadVideo(tiff_seqpath)
    frame = vid.read_next_frame()
    assert np.shape(frame) == (1080, 1920, 3)

def test_read_frame_range(): 
    """Check if reading with a frame_range works correctly"""
    vid = video.ReadVideo(mp4_videopath, frame_range=(1,10,2))
    for index, img in enumerate(vid):
        pass
    assert index == 4

def test_read_framenum_too_high():
    """Check Error raised if asking for frame outside of video numframes range"""
    vid = video.ReadVideo(mp4_videopath)
    with pytest.raises(AssertionError):
        vid.read_frame(n=1000)

def test_read_vid_props():
    """Test we are reading video properties"""
    vid = video.ReadVideo(mp4_videopath)
    assert vid.num_frames == 20
    
def test_read_seq_props():
    """Test we are reading the properties of img sequence.  
    png_path should only find files named SampleVideo....
    """
    vid = video.ReadVideo(png_seqpath)
    assert vid.num_frames == 4

def test_read_single_img():
    """Check working with single imgs"""
    vid = video.ReadVideo(single_img)
    frame = vid.read_next_frame()
    assert vid.num_frames == 1

def test_imgs_to_video():
    """Check imgs convert to video correctly"""
    output_filename=png_seqpath[:-5]+'.mp4'
    video.opencv_io.imgs_to_video(png_seqpath, output_filename, sort=None)
    assert os.path.exists(output_filename)
    os.remove(output_filename)

def test_video_to_imgs():
    """Check imgs convert to video correctly"""
    
    test_dir = data_dir + '/test'
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    output_filenamestub=test_dir + '/test'
    os.mkdir(test_dir)
    video.opencv_io.video_to_imgs(mp4_videopath, output_filenamestub)  
    assert os.path.exists(test_dir + '/test02.png')
    shutil.rmtree(test_dir)

#=================================================================================
# WriteVideo Tests #=================================================================================

def test_write_video():
    test_img = cv2.imread(single_img)
    writevid = video.WriteVideo(output_filename, frame_size=(1080, 1920, 3))
    writevid.add_frame(test_img)
    writevid.close()
    assert os.path.exists(output_filename)
    os.remove(output_filename)

def test_frame_wrong_shape_raises_error():
    writevid = video.WriteVideo(output_filename, frame_size=(1080, 1920, 3))
    test_img = np.zeros((1000, 1000, 3), dtype=np.uint8)
    with pytest.raises(AssertionError):
        writevid.add_frame(test_img)

def test_either_img_framesize_supplied_error():
    with pytest.raises(AssertionError):
        writevid = video.WriteVideo(output_filename, frame_size=None, frame=None)

def test_suffix_generator():
    assert video.opencv_io.suffix_generator(5, num_figs=4) == '0005'

    




        