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

    def _find_itags(self, video, best_video=True):
        """Finds the itags of the YouTube streams, and identifies the stream with the best resolution and audio quality.

        Parameters
        ----------
        video : pytube.YouTube instance
            pytube.YouTube object used for identifying available streams.
        best_video : {True, False}, bool, optional
            If True, then this method finds the best available quality, in terms of resolution, video stream, by default True.

        Returns
        -------
        video_itag : str
            The itag of the video stream with the best resolution. 
        audio_itag :  str
            The itag of the audio stream with the best resolution.
        resolution : str
            The best resolution, of the video, that is available for download. The only available resolutions, as of 07/23/2020 (MM/DD/YYYY), are {1080p, 720p, 480p, 360p, 240p, 144p}.

        Notes
        -----
        Note that "best resolution" in the documentation refers to the best resolution depending on the specified scheme. For example if ``best_video`` is ``True`` then the best resolution is the highest number resolution. Contrastingly, if ``best_video`` is ``False`` then the best resolution is the lowest number resolution.

        """
        resolutions = ["1080p", "720p", "480p", "360p", "240p", "144p"]

        if best_video is False:
            resolutions.reverse()

        video_tag_found = False
        base_resolution = resolutions[0]
        for resolution in resolutions:
            if video_tag_found is True:
                break
            video_streams = video.streams.filter(
                resolution=resolution, mime_type="video/mp4", type="video"
            )
            if len(video_streams) != 0:
                video_tag_found = True
                base_resolution = resolution
                video_itag = video_streams[0].itag

        audio_streams = video.streams.filter(type="video", mime_type="audio/mp4")
        audio_itag = audio_streams[0].itag

        return {
            "video_itag": video_itag,
            "audio_itag": audio_itag,
            "resolution": base_resolution,
        }

    def download_video(self, url, name, verbose=False):
        """Downloads a single video using the provided ``url`` and pytube.
        
        Parameters
        ----------
        url : str
            The URL of the video to be downloaded.
        name : str
            The name of the folder to be created.
        verbose : {False, True}, bool, optional
            Determines if verbose information is output to the system log, by default False. If True, then itag information about the video and audio streams is passed to the system logger.

        Returns
        -------
        None

        """
        video = pytube.YouTube(url)
        itags = self._find_itags(video, best_video=True)

        if verbose:
            print(
                "Tags found. video: {}, audio: {}.".format(
                    itags["video_itag"], itags["audio_itag"]
                )
            )

        video_extract_path = os.path.join()
        video.streams.get_by_itag(itags["video_itag"]).download(output_path=)
