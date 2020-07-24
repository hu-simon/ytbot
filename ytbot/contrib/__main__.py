"""
Python (non-tested) implementation of objects used to download videos from YouTube.
"""

import os
import re
import time
import configparser
import concurrent.futures

import cv2
import pytube


class YouTubeDownloader:
    """Implementation of the YouTubeDownloader class used for downloading YouTube videos."""

    def __init__(self, url_list, extract_path=os.getcwd()):
        """Instantiates a YouTubeDownloader object.

        This is the main interface used for downloading videos and captions from YouTube.

        Parameters
        ----------
        url_list : list (of strs)
            List containing the URLs of the YouTube videos to download, represented as strings.
        extract_path : str, optional
            The absolute path to the directory where video data will be stored, by default the current working directory. 
        
        Returns
        -------
        None

        Notes
        -----
        Downloaded videos will be stored in {extract_path}/media/video, audio will be stored in {extract_path}/media/audio, video captions will be stored in {extract_path}/media/captions/raw, and raw transcripts (from VGG dataset) will be stored in {extract_path}/media/captions/processed

        """
        assert len(url_list) != 0
        self.url_list = url_list
        self.n_urls = len(self.url_list)
        self.extract_path = extract_path

    def find_itags(self, video):
        """Finds the itags of the YouTube streams, and identifies the stream with the best resolution and audio quality.

        Parameters
        ----------
        video : pytube.YouTube instance
            pytube.YouTube object used for identifying available streams.
        
        Returns
        -------
        video_itag : str
            The itag of the video stream with the best resolution. 
        audio_itag :  str
            The itag of the audio stream with the best resolution.
        best_resolution : str
            The best resolution, of the video, that is available for download. The only available resolutions, as of 2020, are {1080p, 720p, 480p, 360p, 240p, 144p}.

        """
        resolutions = ["1080p", "720p", "480p", "360p", "240p", "144p"]
        best_found = False
        best_resolution = "1080p"

        for resolution in resolutions:
            

