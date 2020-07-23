"""
Python (not-tested) implementation of objects used to download videos from 
YouTube, for generating datasets.

"""

import os
import re
import time
import configparser
import concurrent.futures

import cv2
import pytube


class YouTubeDownloader:
    """
    Python implementation of the YouTubeDownloader class used for downloading YouTube videos.

    Attributes
    ----------
    TODO

    Methods
    -------
    TODO

    """

    def __init__(self, url_list, config_path=os.getcwd(), extract_path=os.getcwd()):
        """
        Instantiates a YouTubeDownloader object.

        This is the main interface used for downloading videos from YouTube.
        
        Parameters
        ----------
        url_list : list (of str)
            List containing urls, represented as strings.
        config_path : str, optional
            The absolute path to the folder containing the config.properties file, by default the current working directory.
        extract_path : str, optional
            The absolute path to the directory where videos will be stored, by default the current working directory.
        
        Returns
        -------
        None

        """
        assert len(url_list) != 0
        self.url_list = url_list
        self.n_urls = len(self.url_list)
        self.extract_path = extract_path
        self.config_path = config_path

    def find_itags(self, video):
        """
        Finds the itags of the YouTube videos with the best resolution and audio quality.
        
        Parameters
        ----------
        video : pytube.YouTube instance
            pytube.YouTube object used for finding available streams.
        
        Returns
        -------
        video_itag : str
            The itag of the video with the best resolution.
        audio_itag : str
            The itag of the audio that has the best audio quality.
        best_resolution : str
            The best resolution (of the video) that is available.

        """
        resolutions = ["1080p", "720p", "360p", "240p"]
        best_found = False
        best_resolution = 1080

        for resolution in resolutions:
            if best_found is True:
                break
            video_streams = video.streams.filter(
                resolution=resolution, mime_type="video/mp4", type="video"
            )

            if len(video_streams) != 0:
                best_found = True
                best_resolution = resolution
                video_itag = video_streams[0].itag

        audio_streams = video.streams.filter(type="audio", mime_type="audio/mp4")
        audio_itag = audio_streams[0].itag

        return video_itag, audio_itag, best_resolution

    def download_video(self, url, filename):
        """
        Downloads a single video using ``url`` as a reference.
        
        Parameters
        ----------
        url : str
            The url of the video.
        
        Returns
        -------
        None
        
        """
        video = pytube.YouTube(url)
        video_itag, audio_itag, best_resolution = self.find_itags(video)
        print("Tags, video {} and audio {}".format(video_itag, audio_itag))
        video.streams.get_by_itag(video_itag).download(
            output_path=self.extract_path, filename="video{}".format(filename)
        )
        video.streams.get_by_itag(audio_itag).download(
            output_path=self.extract_path, filename="audio{}".format(filename)
        )

        print("Downloaded video{} successfully.".format(filename))

        del video
        del video_itag
        del audio_itag

    @staticmethod
    def get_captions(url, filename, output_path):
        """
        Obtains the captions associated with the video.
        """
        video = pytube.YouTube(url)
        print(
            video.captions["en"].download(
                title=filename, output_path=output_path, filename_prefix="caption"
            )
        )

    def _get_captions(self, url, filename):
        """
        Internal method for downloading the captions associated with the video, if available.

        Parameters
        ----------
        url : str
            String representing the URL.
        filename : str
            The name of the caption file.

        Returns
        -------
        None
        """
        video = pytube.YouTube(url)
        has_en_captions = "en" in video.captions
        if has_en_captions:
            video.captions["en"].download(
                title=filename, output_path=self.extract_path, filename_prefix="caption"
            )

    def download_all_videos(self):
        """
        Downloads all the videos, using the links in ``self.url_list`` as a reference.

        See Also:
        ---------
        ytbot.__main__.YouTubeDownloader.download_video : subroutine
        """
        filenames = ["{}".format(k) for k in range(self.n_urls)]

        with concurrent.futures.ThreadPoolExecutor(5) as executor:
            executor.map(self.download_video, self.url_list, filenames)

    def download_all_captions(self):
        filenames = ["{}".format(k) for k in range(self.n_urls)]

        with concurrent.futures.ThreadPoolExecutor(5) as executor:
            executor.map(self._get_captions, self.url_list, filenames)
