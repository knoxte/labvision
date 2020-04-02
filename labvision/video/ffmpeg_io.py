
import numpy as np
import ffmpeg
from slicerator import Slicerator

__all__ = ['ReadVideoFFMPEG', 'WriteVideoFFMPEG']


@Slicerator.from_class
class ReadVideoFFMPEG:
    """
    ReadVideoFFMPEG reads images from video using FFMPEG

    Attributes
    ----------
    filename : str
        full path and filename for video to be read
    width : int
        width of frame being read
    height : int
        height of frame being read
    num_frames : int
        total number of frames in video

    Examples
    --------

    | readVid = ReadVideoFFMPEG(filename)
    | img = readVid.read_frame()
    """

    def __init__(self, filename):
        self.filename = filename
        self._get_info()
        self._setup_process()

    def _get_info(self):
        probe = ffmpeg.probe(self.filename)
        video_info = next(
            s for s in probe['streams'] if s['codec_type'] == 'video')
        self.width = int(video_info['width'])
        self.height = int(video_info['height'])
        self.num_frames = int(video_info['nb_frames'])

    def _setup_process(self):
        self.process = (
            ffmpeg
            .input(self.filename)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run_async(pipe_stdout=True, quiet=False)
            )

    def read_frame(self):
        """
        read_frame reads the next image from the video

        :return: np.ndarray
        """
        frame_bytes = self.process.stdout.read(self.width * self.height * 3)
        frame = (
            np.frombuffer(frame_bytes, np.uint8)
            .reshape([self.height, self.width, 3]))
        return frame

    def read_frame_bytes(self):
        frame_bytes = self.process.stdout.read(self.width * self.height * 3)
        return frame_bytes

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.read_frame()
        except IndexError:
            raise StopIteration

    def __getitem__(self):
        return self.read_frame()

    def __len__(self):
        return self.num_frames

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.process.stdin.close()
        self.process.wait()


class WriteVideoFFMPEG:
    """WriteVideoFFMPEG writes images to file with FFMPEG

        Attributes
        ----------
        filename : str
            Full path and filename to output file
        bitrate : str
            bitrate affects video quality and file size
        framerate : int
            frames per second playback of video
        speed : str
            specifies the speed


        Examples
        --------
        | with WriteVideo(filename) as writevid:
        |    writevid.add_frame(img)
        |    writevid.close()

    """

    def __init__(self, filename, speed='superfast', bitrate='LOW4K', framerate=50.0):
        self.filename = filename
        self.frame_no = 0
        bitrates = {
            'LOW4K': '20000k',
            'MEDIUM4K': '50000k',
            'HIGH4K': '100000k',
            'LOW1080': '5000k',
            'MEDIUM1080': '10000k',
            'HIGH1080': '20000k'}
        self.video_bitrate = bitrates[bitrate]
        self.framerate=framerate
        self.preset = speed

    def add_frame(self, frame):
        """
        add next frame to the video being written

        :param frame: np.ndarray
            frame to be added to the video
        :return: None
        """

        if self.frame_no == 0:
            width = np.shape(frame)[1]
            height = np.shape(frame)[0]
            self._setup_process(width, height)
        self.process.stdin.write(frame.astype(np.uint8).tobytes())
        self.frame_no += 1

    def add_frame_bytes(self, frame, width, height):
        if self.frame_no == 0:
            self._setup_process(width, height)
        self.process.stdin.write(frame)
        self.frame_no += 1

    def _setup_process(self, width, height):
        self.process = (
            ffmpeg
            .input(
                'pipe:',
                format='rawvideo',
                pix_fmt='rgb24',
                s='{}x{}'.format(width, height),
                r=50
            )
            .output(
                self.filename,
                pix_fmt='yuv420p',
                vcodec='libx264',
                preset=self.preset,
                video_bitrate=self.video_bitrate,
                r=self.framerate
            )
            .overwrite_output()
            .run_async(
                pipe_stdin=True,
                quiet=False
            )
        )

    def close(self):
        """
        Release video object
        :return: None
        """

        self.process.stdin.close()
        self.process.wait()
