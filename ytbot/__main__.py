import os
import re
import datetime

import cv2
import pytube


class YouTubeDownloader:
    """
    Python implementation of the YouTubeDownloader class, used for downloading YouTube videos.

    Attributes
    ----------
    TODO

    Methods
    -------
    TODO

    """

    def __init__(
        self, list_of_urls, download_path=os.getcwd(), settings_file=os.getcwd()
    ):
        """
        Instantiates a YouTubeDownloader object.
        
        Parameters
        ----------
        list_of_urls : list (of str)
            List containing urls, represented as strings.
        download_path : str, optional
            The absolute path to the folder where videos are stored, by default the current directory.
        settings_file : str, optional
            The absolute path to the folder containing the settings.txt file, by default the current directory.
        """
        assert len(list_of_urls) != 0
        self.list_of_urls = list_of_urls
        self.download_path = download_path
        self.settings_file = settings_file

    def load_settings(self):
        pass

    def download_videos(self):
        pass


class VideoConverter:
    """
    Python implementation of the VideoConverter class, used for converting video and audio files into a single video with audio.

    """

    def __init__(self):
        pass


class FrameExtractor:
    """
    Python implementation of the FrameExtractor class, used for extracting certain frames from videos with audio. 
    """

    def __init__(self):
        pass
