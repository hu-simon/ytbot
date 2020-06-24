"""
Python implementation of the YouTubeDownloader, which downloads videos from YouTube, for dataset generation.

TODO
1. Make the code amenable to multiprocessing, to speed everything up.
"""

import os
import re
import datetime
import configparser

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

    def __init__(self, links, config_path=os.getcwd(), extract_path=os.getcwd()):
        """
        Instantiates a YouTubeDownloader object.
        
        Parameters
        ----------
        links : list (of str)
            List containing urls, represented as strings.
        config_path : str, optional
            The absolute path to the folder containing the config.properties file, by default the current directory.
        extract_path : str, optional
            The absolute path to the folder where the videos will be stored, by default the current directory.

        Returns
        -------
        None

        """
        assert len(links) != 0
        self.links = links
        self.num_links = len(links)
        self.extract_path = extract_path
        self.config_path = config_path

        # self.parse_config_file()

    def parse_config_file(self):
        """
        Parses the configuration file to obtain desired parameters for the videos to download. 

        For example, we can set the desired resolution, etc.

        Parameters
        ----------
        None

        Returns
        -------
        None
        
        Raises
        ------
        Exception
            An exception is raised if the config.properties file cannot be found in the directory ``config_path``.
            
        """
        allowed_resolutions = [
            "2160",
            "1440",
            "1080",
            "720",
            "480",
            "360",
            "240",
            "best",
            "worst",
        ]

        self.config = configparser.ConfigParser()
        try:
            self.config.read(os.path.join(config_path, "config.properties"))
            try:
                if (
                    self.config.get("VideoSettings", "resolution")
                    in allowed_resolutions
                ):
                    self.video_resolution = self.config.get(
                        "VideoSettings", "resolution"
                    )
                else:
                    print(
                        "The resolution you have selected is not supported. The options are: 2160, 1440, 1080, 720, 480, 360, 240, best, worst"
                    )
            except:
                print(
                    "WARNING: No resolution setting was found in config.properties, defaulting to best resolution possible."
                )
                self.video_resolution = "best"

        except:
            raise Exception(
                "FATAL ERROR: Could not find the config.properties file in the specified directory. Please try again."
            )

    def download_videos(self):
        allowed_resolutions = ["2160p", "1440p", "1080p", "720p", "360p", "240p"]

        for k, link in enumerate(self.links):
            video = pytube.YouTube(link)

            best_found = False
            best_resolution = 1080
            for resolution in allowed_resolutions:
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

            video.streams.get_by_itag(video_itag).download(
                output_path=self.extract_path, filename="video{}".format(k)
            )
            video.streams.get_by_itag(audio_itag).download(
                output_path=self.extract_path, filename="audio{}".format(k)
            )

            os.system(
                "ffmpeg -i {0}/video{1}.mp4 -i {2}/audio{3}.mp4 -c:v copy -c:a aac video{4}_{5}.mp4".format(
                    self.extract_path, k, self.extract_path, k, k, best_resolution
                )
            )


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
