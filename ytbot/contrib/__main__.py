"""
Python (non-tested) implementation of objects used to download videos from YouTube.
"""

import os
import re
import time
import shutil
import configparser
import concurrent.futures

import cv2
import pytube
import requests
import threading


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
        assert len(url_list) != 0, "Need at least one viable URL."
        self.url_list = url_list
        self.n_urls = len(self.url_list)
        self._filter_available(verbose=True, remove_directory=True)
        self.extract_path = extract_path

    @staticmethod
    def _is_valid(url, verbose=True):
        """Checks if the URL is valid, by checking the response and HTML text.

        A URL is not valid if it either gives a bad response (not 200) or the HTML text contains the sequence "simpleText":"Video unavailable".

        Parameters
        ----------
        url : str
            The URL to be checked.
        verbose : {True, False}, bool, optional
            Determines if verbose information is output to the console.

        Returns
        -------
        valid_url : {True, False}, bool
            If True, then the URL is indeed valid, and the video and audio streams can be accessed.
        
        """
        valid_url = True
        req = requests.get(url)

        if req.status_code != 200:
            valid_url = False
            if verbose:
                print("[INFO] {} is not a valid URL".format(url))

        if req.text.find('"simpleText":"Video unavailable"') != -1:
            valid_url = False
            if verbose:
                print(
                    "[INFO] {} does not have any available audio or video streams".format(
                        url
                    )
                )

        return valid_url

    def _filter_available_nonthreading(self, verbose=True, remove_directory=False):
        """Filters out video URLs by testing to see if the video is available, without threading.

        Videos that are unavailable or do not exist can cause problems for the scraper.

        Parameters
        ----------
        verbose : {True, False}, bool, optional
            Determines if verbose output is output to the console, by default True.
        remove_directory : {False, True}, bool, optional
            If True, then the folder containing the data for the URL is removed.

        Returns
        -------
        None

        Notes
        -----
        This function is now deprecated, in favor of using ``_filter_available_single_thread``.

        """
        for url in self.url_list:
            valid_url = self._is_valid(url, verbose=verbose)
            if not valid_url:
                if verbose:
                    print(
                        "[INFO] {} is not a valid URL, removing it from the list".format(
                            url
                        )
                    )
                if remove_directory:
                    folder_name = url.split("=")[1]
                    if verbose:
                        print(
                            "[INFO] Deleting {}".format(
                                os.path.join(self.extract_path, folder_name)
                            )
                        )
                    shutil.rmtree(os.path.join(self.extract_path, folder_name))

                self.url_list.remove(url)

        self.n_urls = len(self.url_list)
        assert (
            self.n_urls > 0
        ), "Not enough URLs to run the scraper, need at least one valid URL."

    def _filter_available_single_thread(
        self, url, verbose=True, remove_directory=False
    ):
        """Filters out video URLs by testing to see if the video is available, for a single thread.

        Videos that are unavailable or do not exist can cause problems for the scraper, and the folders that host the videos can be removed using the ``remove_directory`` flag.

        Parameters
        ----------
        url : str
            The URL of the video to test availability.
        verbose : {True, False}, bool, optional
            Determines if verbose output is output to the console, by default True.
        remove_directory : {False, True}, bool, optional
            If True, then the folder containing the data for the URL is removed.
        
        Returns
        -------
        None

        """
        valid = self._is_valid(url, verbose=verbose)
        if not valid:
            if verbose:
                print("[INFO] {} is not a valid url".format(url))

            if remove_directory:
                folder_name = url.split("=")[1]
                if verbose:
                    print(
                        "[WARNING] Deleting {}".format(
                            os.path.join(self.extract_path, folder_name)
                        )
                    )
                shutil.rmtree(os.path.join(self.extract_path, folder_name))

            self.url_list.remove(url)
            self.n_urls = len(self.url_list)
            assert self.n_urls > 0, "Not enough valid URLs to run the scraper."

    def _filter_available(self, verbose=True, remove_directory=False):
        """Filters out video URLs by testing to see if the video is available. 

        Videos that are unavailable or do not exist can cause problems for the scraper.

        Parameters
        ----------
        verbose : {True, False}, bool, optional
            Determines if verbose output is output to the console, by default True.
        remove_directory : {False, True}, bool, optional
            If True, then the folders containing the data of invalid URLs are removed.

        Returns
        -------
        None

        """
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(
                self._filter_available_single_thread,
                self.url_list,
                [True] * self.n_urls,
                [True] * self.n_urls,
            )

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

        audio_streams = video.streams.filter(type="audio", mime_type="audio/mp4")
        audio_itag = audio_streams[0].itag

        # Debugging, delete later.
        print("Found tags, {} and {}".format(video_itag, audio_itag))

        return {
            "video_itag": video_itag,
            "audio_itag": audio_itag,
            "resolution": base_resolution,
        }

    def _download_video(self, url, name, verbose=False):
        """Downloads a single video using the provided ``url`` and pytube.
        
        Parameters
        ----------
        url : str
            The URL of the video to be downloaded.
        name : str
            The name to be appended to the end of the captions header.
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
                "[INFO] Tags found. video: {}, audio: {}.".format(
                    itags["video_itag"], itags["audio_itag"]
                )
            )

        video_extract_path = os.path.join(
            self.extract_path, "{}/media/raw_video".format(url.split("=")[1])
        )
        audio_extract_path = os.path.join(
            self.extract_path, "{}/media/raw_audio".format(url.split("=")[1])
        )
        caption_extract_path = os.path.join(
            self.extract_path, "{}/media/captions/raw".format(url.split("=")[1])
        )

        video.streams.get_by_itag(itags["video_itag"]).download(
            output_path=video_extract_path, filename="video{}".format(name)
        )
        video.streams.get_by_itag(itags["audio_itag"]).download(
            output_path=audio_extract_path, filename="audio{}".format(name)
        )
        self._get_captions(
            video=video, name=name, extract_path=caption_extract_path, verbose=verbose
        )

        if verbose:
            print("[INFO] Downloaded audio and video from {} successfully.".format(url))

        del video
        del itags

    def _get_captions(self, video, name, extract_path, code="en", verbose=True):
        """Extracts the captions associated with the YouTube video associated with ``url``.

        Note that only official captions are supported; auto-generated captions are not supported at this time.

        Parameters
        ----------
        video : pytube.YouTube instance
            pytube.YouTube instance containing all the video information.
        name : str
            The name to be appened to the end of the captions header.
        extract_path : str
            The absolute path to the directory where video data will be stored, by default the current working directory. 
        code: str, optional
            The code representing the type of language we want to download the captions in, by default "en" 
        verbose : {True, False}, bool, optional
            Determines if verbose information is shown by the console, by default False.

        Returns
        -------
        None

        """
        has_en_captions = "en" in video.captions
        if has_en_captions:
            video.captions["en"].download(
                title=name, output_path=extract_path, filename_prefix="caption"
            )

            if verbose:
                print(
                    "Downloaded captions from {} successfully.".format(video.watch_url)
                )

    def _get_captions_using_url(self, url, name, verbose=True):
        """Extracts the captions associated with the YouTube video associated with ``url``.

        This function calls ``_get_captions`` as a subroutine, and the only difference is that this method passes the ``url`` instead of a pytube.YouTube instance.

        Parameters
        ----------
        url : str
            The URL of the video to extract captions from.
        name : str
            The name to be appended to the end of the captions header.
        verbose : {True, False}, bool, optional
            Determines if verbose information is output to the system log, by default False.

        Returns
        -------
        None
        
        See Also
        --------
        _get_captions : subroutine
        """
        video = pytube.YouTube(url)
        self._get_captions(video, name=name, verbose=verbose)

    def download_all_videos(self, max_workers=8, verbose=True):
        """Downloads the media information in ``self.url_list``.

        Downloads the video, audio, and captions, if they are available.

        Parameters
        ----------
        max_workers : int, optional
            The maximum number of workers (i.e. threads) in the ``ThreadPoolExecutor``.
        verbose : {True, False}, bool, optional
            Determines if verbose information is output to the system log, by default False.

        Returns
        -------
        None

        """
        names = ["{}".format(k) for k in range(self.n_urls)]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(
                self._download_video, self.url_list, names, [True] * len(names)
            )
