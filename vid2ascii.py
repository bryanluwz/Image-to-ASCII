"""
Python file for Converter Class for converting Video to ASCII characters.
"""

import cv2
import os
import imageio
import numpy as np
import shutil
from moviepy.editor import VideoFileClip, AudioFileClip
import time

from img2ascii import IMG2ASCIIConverter
from helper import bcolors


class VID2ASCIIConverter:
    """
    A class for converting an video to ASCII characters.
    """

    def __init__(self) -> None:
        # Initialise image to ASCII converter
        self.image_to_ascii_converter = IMG2ASCIIConverter()
        self.init_image_to_ascii_converter()

        # Video stuff
        self.video_capture = None
        self.video_path = ""
        self.fps = -1
        self.total_frame_count = -1

        # Video writer stuff
        self.video_writer = None
        self.video_output_path = None
        self.temp_video_output_path = "./out.mp4"
        self.VIDEO_WRITER_REPEAT_CYCLE = 50  # Video writer will write frames to output every ?? frames
        self.converter_video_frames_buffer = [None] * self.VIDEO_WRITER_REPEAT_CYCLE

        # Quality of Life update
        self.previous_five_time = np.ones(shape=(5))
        
    def init_image_to_ascii_converter(self, horizontal: int=100, vertical: int=100):
        """
        Sets the horizontal and vertical ASCII characters count.

        Final frame will have either 'horizontal' amount of characters widthwise
        or 'vertical' amount of characters heightwise, whichever one depending on
        the original image's aspect ratio.
        """
        self.image_to_ascii_converter.set_ascii_chars_count(horizontal, vertical)

    def set_video(self, video_path: str):
        """
        Sets the `self.video_capture` by using cv2.VideoCapture(video_path).

        Returns True if it is set successfully.
        """
        # Check if file exists
        if not os.path.exists(video_path):
            print(
                f"{bcolors.WARNING}[-] Video file of path '{video_path}' does not exist 0.o {bcolors.ENDC}\n"
            )
            return False

        # Read video, and set variables, and aslo video output path ig
        self.video_path = video_path
        self.video_capture = cv2.VideoCapture(video_path)
        self.fps = self.video_capture.get(cv2.CAP_PROP_FPS)
        self.total_frame_count = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        root, ext = os.path.splitext(video_path)
        self.video_output_path = root + "_ascii" + ext
        
        return True

    def create_video(self, gscale_level: int=0):
        """
        Create video of ASCII characters from frame
        """
        # Check if got video
        if self.video_capture is None:
            print(f"{bcolors.WARNING}[!] Wow slow down there Jose, no video is set yet >:/{bcolors.ENDC}\n")
            return False

        # Check if is gif
        is_gif = False
        
        print(os.path.splitext(self.video_path)[-1].lower())
        if 'gif' in os.path.splitext(self.video_path)[-1].lower():
            print(f"{bcolors.WARNING}[!] Correct me if I'm wrong but this is a GIF, ... right??{bcolors.ENDC}\n")
            is_gif = True

        # While loop to slowly loop through video
        print(f"{bcolors.WARNING}[!] Converting frames to ASCII characters and writing frames to output video {bcolors.ENDC}\n")

        ret, frame = self.video_capture.read()

        i = 0

        while ret:
            t0 = time.time()

            # Get grayscale frame, and convert to ASCII image
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.image_to_ascii_converter.set_image_by_array(gray_frame)
            self.image_to_ascii_converter.scale_image()
            self.image_to_ascii_converter.create_text(gscale_level=gscale_level)
            self.image_to_ascii_converter.create_image()

            # Save to frame buffer, and update time in 5 cycle moving average of time taken
            self.converter_video_frames_buffer[i % self.VIDEO_WRITER_REPEAT_CYCLE] = self.image_to_ascii_converter.ascii_image_array
            self.previous_five_time[i % 5] = time.time() - t0

            # Every fifty cycle append frame to output video, then clear buffer
            if i % self.VIDEO_WRITER_REPEAT_CYCLE == 49:
                for frame in self.converter_video_frames_buffer:
                    self.append_frames_to_output(frame, not is_gif)
                self.converter_video_frames_buffer = [None] * self.VIDEO_WRITER_REPEAT_CYCLE

            # Print out info of frame
            i += 1
            print(f"{bcolors.WARNING}[!] Frame {i} out of {self.total_frame_count} completed. About {np.mean(self.previous_five_time) * (self.total_frame_count - i):.2f}s to go! ඞ {bcolors.ENDC}")

            # Load next video frame
            ret, frame = self.video_capture.read()

        # Append remaining frames from buffer, and add audio
        for frame in self.converter_video_frames_buffer:
            if frame is None:
                break
            else:
                self.append_frames_to_output(frame)

        print(f"\n{bcolors.WARNING}[!] Video created ლ(╹◡╹ლ) {bcolors.ENDC}\n")
        
        self.video_writer.close()

        if not is_gif:
            self.add_original_audio()

        return True

    def append_frames_to_output(self, frame, write_as_temp=True):
        """
        Append frames to video output, automatically create video writer if not instantiated yet.

        @param `write_as_temp`: Whether to write frames to temporary output path or actual output path.
        """
        if self.video_writer is None or self.video_writer.closed:
            self._create_video_writer(write_as_temp=write_as_temp)
        
        try:
            self.video_writer.append_data(frame)
            return True
        except:
            print(f"{bcolors.WARNING}[-] Rewriting video due to some weird reason :< {bcolors.ENDC}\n")
            return False

    def _create_video_writer(self, write_as_temp=True):
        """
        Create video writer, shouldn't be called outside of class.
        """
        if write_as_temp:
            self.video_writer = imageio.get_writer(self.temp_video_output_path, fps=self.fps)
        else:
            self.video_writer = imageio.get_writer(self.video_output_path, fps=self.fps)

    def add_original_audio(self, del_temp=True):
        print(f"{bcolors.WARNING}[!] Adding audio to video file of path {self.video_output_path} ◑﹏◐ {bcolors.ENDC}\n")

        video_clip = VideoFileClip(self.temp_video_output_path)
        audio_clip = AudioFileClip(self.video_path)
        video_clip = video_clip.set_audio(audio_clip)
        video_clip.write_videofile(self.video_output_path)

        if del_temp:
            os.remove(self.temp_video_output_path)

        print(f"\n{bcolors.WARNING}[!] Finished adding audio to {self.video_output_path} · ᴗ · {bcolors.ENDC}\n")

if __name__ == "__main__":
    t0 = time.time()

    converter = VID2ASCIIConverter()
    # converter.set_video("ඞ.mp4")
    converter.set_video("./test_folder/rick_roll.mp4")
    converter.init_image_to_ascii_converter(200, 200)
    converter.create_video()
    
    print(f"{bcolors.WARNING}Wow all that took {(time.time() - t0):.2f}s {bcolors.ENDC}\n")