import os
import cv2
import numpy as np
from slicerator import Slicerator
from filehandling import BatchProcess
from .. import images


__all__ = ['ReadVideo','WriteVideo','video_to_imgs','imgs_to_video']


@Slicerator.from_class
class ReadVideo:
    """Reading Videos class is designed to wrap
    the OpenCV VideoCapture class and make it easier to
    work with.

    Attributes
    ----------
    vid : instance
        OpenCV VideoCapture instance
    filename : str
        Full path and filename to video to read
    grayscale : bool
        True to read as grayscale
    frame_range : tuple
        (start frame num, end frame num, step)
    frame_num : int
        current frame pointed at in video
    num_frames : int
        number of frames in the video. If a range is selected this may not be accessible.
    width : int
        width of frame in pixels
    height : int
        height of frame in pixels
    colour : int
        number of colour channels
    frame_size : tuple
        gives same format as np.shape
    fps : int
        number of frames per second
    file_extension : str
        file extension of the video. ReadVideo works with .mp4, .MP4, .m4v and '.avi'
    properties: dict
        a dictionary of the parameters

    Examples
    --------
    Use a get method:

        | read_vid = ReadVideo(filename)
        | img = read[4]

    ReadVideo supports usage as a generator:

        | for img in ReadVideo(filename, range=(5,20,4)):
        |     labvision.images.basics.display(img)

    ReadVideo supports "with" usage. This basically means no need to call .close():

        | with ReadVideo() as readvid:
        |     DoStuff

    """

    def __init__(self, filename=None, grayscale=False,
                 frame_range=(0, None, 1), return_function=None):
        self.filename = filename
        self.grayscale = grayscale
        self._detect_file_type()
        self.init_video()
        self.get_vid_props()
        self.frame_num = 0
        self.vid_position = 0
        self.set_frame_range(frame_range)
        self.return_func = return_function
        self.cached_frame = None
        self.cached_frame_number = None

    def set_frame_range(self, frame_range):
        self.frame_range = (
        frame_range[0], self.num_frames, frame_range[2]) if (
                    frame_range[1] == None) else frame_range
        self.frame_num = frame_range[0]
        if self.frame_num != self.vid_position:
            self.set_frame(self.frame_num)

    def _detect_file_type(self):
        self.ext = os.path.splitext(self.filename)[1]
        if self.ext in ['.MP4', '.mp4', '.m4v', '.avi', '.mkv', '.webm']:
            self.filetype = 'video'
        else:
            raise NotImplementedError('File extension is not implemented')

    def init_video(self):
        """ Initialise video capture object"""
        self.vid = cv2.VideoCapture(self.filename)

    def get_vid_props(self):
        """
        Get the properties of the video

        :return: dict(properties)
        """
        self.frame_num = self.vid.get(cv2.CAP_PROP_POS_FRAMES)
        self.num_frames = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_time = self.vid.get(cv2.CAP_PROP_POS_MSEC)
        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if self.vid.get(cv2.CAP_PROP_MONOCHROME) == 0.0:
            self.colour = 3
            self.frame_size = (self.height, self.width, 3)
        else:
            self.colour = 1
            self.frame_size = (self.width, self.height)
        self.fps = self.vid.get(cv2.CAP_PROP_FPS)
        self.format = self.vid.get(cv2.CAP_PROP_FORMAT)
        self.codec = self.vid.get(cv2.CAP_PROP_FOURCC)
        self.file_extension = self.filename.split('.')[1]

        self.properties = {'frame_num': self.frame_num,
                           'num_frames': self.num_frames,
                           'width': self.width,
                           'height': self.height,
                           'colour': self.colour,
                           'frame_size': self.frame_size,
                           'fps': self.fps,
                           'codec': self.codec,
                           'format': self.format,
                           'file_extension': self.file_extension}

    def read_frame(self, n=None):
        """
        | Read a single frame from the video
        |
        | :param n: int
        |    frame index calls specified frame. If None or not
        |    specified calls the next available frame.
        | :return: np.ndarray
        |    returns specified image
        """
        if n is None:
            return self.read_next_frame()
        else:
            self.set_frame(n)
            return self.read_next_frame()

    def set_frame(self, n):
        """
        Set_frame moves the pointer in the video to the index n

        :param n: int
            index specifying the frame
        :return: None
        """
        if n == self.cached_frame_number:
            self.frame_num = n
        elif n == self.vid_position:
            self.frame_num = n
        else:
            self.frame_num = n
            if self.frame_num < self.frame_range[0]:
                self.frame_num = self.frame_range[0]
            elif self.frame_num >= self.frame_range[1]:
                self.frame_num = self.frame_range[1] - 1
            if self.frame_num != self.vid_position:
                self.vid.set(cv2.CAP_PROP_POS_FRAMES, float(n))
                self.vid_position = n

    def read_next_frame(self):
        """
        Reads the next available frame. Note depending on the range specified
        when instantiating object this may be step frames.
        :return:
        """
        assert (self.frame_num >= self.frame_range[0]) & \
               (self.frame_num < self.frame_range[1]) & \
               ((self.frame_num - self.frame_range[0]) % self.frame_range[
                   2] == 0), \
            'Frame not in range'

        if self.frame_num == self.cached_frame_number:
            ret = True
            im = self.cached_frame
        elif self.frame_num == self.vid_position:
            ret, im = self._read()
        else:
            self.set_frame(self.frame_num)
            ret, im = self._read()

        self.frame_num += self.frame_range[2]
  
        if ret:
            if self.grayscale:
                im = images.bgr_to_gray(im)
            if self.return_func:
                im = self.return_func(im)

            return im.copy()
        else:
            raise Exception('Cannot read frame')

    def _read(self):
        ret, im = self.vid.read()
        self.cached_frame = im
        self.cached_frame_number = self.vid_position
        self.vid_position += 1
        return ret, im

    def close(self):
        """Closes video object"""
        if self.filetype == 'video':
            self.vid.release()

    def __getitem__(self, frame_num):
        """Getter reads frame specified by passed index"""
        return self.read_frame(n=frame_num)

    def __len__(self):
        return self.num_frames

    def __iter__(self):
        return self

    def __next__(self):
        """
        Generator returns next available frame specified by step
        :return:
        """
        if self.frame_num < self.frame_range[1]:
            return self.read_frame()
        else:
            raise StopIteration

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class WriteVideo:
    """WriteVideo writes images to a video file using OpenCV

    Attributes
    ----------
    filename : String
        Full path and filename to output file
    vid : instance
        OpenCV VideoWriter instance
    frame_size : tuple
        (height, width) - Same order as np.shape. This should be the input frame_size.
        If the frame is grayscale this will be automatically converted to 3 bit depth
        to keep opencv happy. A warning is printed to remind you.
    frame : np.ndarray
        example image to be saved
    fps : int
        frames per second playback of video
    codec : string
        used to encode file

    Examples
    --------
    | with WriteVideo(filename) as writevid:
    |    writevid.add_frame(img)
    |    writevid.close()

    """


    def __init__(self, filename, frame_size=None, frame=None, fps=50.0, codec='XVID'):
        self.filename=filename

        fourcc = cv2.VideoWriter_fourcc(*list(codec))

        assert (frame_size is not None or frame is not None), "One of frame or frame_size must be supplied"

        self.grayscale = False

        if np.size(np.shape(frame_size)) == 2:
            print('Warning: grayscale image')
            print('Images will be converted to bit depth 3 to keep OpenCV happy!')
            self.grayscale = True

        if frame_size is None:
            self.frame_size = np.shape(frame)

        if frame is None:
            self.frame_size = frame_size

        self.vid = cv2.VideoWriter(
            filename,
            fourcc,
            fps,
            (self.frame_size[1], self.frame_size[0]))

        #assert self.vid.isOpened(), 'Video failed to open'

    def add_frame(self, im):
        """
        Add frame to open video instance

        :param im: Image
        :return: None
        """
        assert np.shape(im) == self.frame_size, "Added frame is wrong shape"

        if self.grayscale:
            im=cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_GRAY2BGR)
        self.vid.write(im)

    def close(self):
        """
        Release video object
        """
        self.vid.release()


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def suffix_generator(i, num_figs=5):
    """Creates a number suffix as string
    e.g 00005"""

    num_digits = len(str(i))
    assert num_figs >= num_digits, 'num digits is greater than requested length of suffix'

    suffix = '0'*(num_figs-num_digits) + str(i)
    return suffix


def video_to_imgs(videoname, image_filename_stub, ext='.png'):
    """
    Function to disassemble video into images
    
    videoname   :   full path to video including extension
    image_filename_stub :   filename stub for all the images (full path)
    ext :   type of image extension, defaults to png
    """
    readvid = ReadVideo(videoname)
    for i, img in enumerate(readvid):
        suffix = suffix_generator(i, num_figs=len(str(readvid.num_files)))
        images.write_img(image_filename_stub + suffix + ext)


def imgs_to_video(file_filter, videoname, sort=None):
    """
    Function to assemble images into a video
    
    file_filter :   full path including wild cards to specify images
    videoname   :   full path to video including extension
    sort        :   optional function handle to specify order of images
    """
    f = BatchProcess(file_filter, smart_sort=sort)

    for i, filename in enumerate(f):
        img = images.read_img(filename)
        if i==0:
            write_vid = WriteVideo(videoname,frame=img)
        write_vid.add_frame(img)
    write_vid.close()
        

    
