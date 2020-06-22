import os
import re
import datetime

import cv2
import pytube
import matplotlib.pyplot as plt


"""
The idea for the following is that we are going to see if there is a stream where "progressive" is True. If it is, then we should just download the file since it already includes the video and audio. Otherwise, we download the best video and best audio and then combining those two together. 

New strategy: 
1. Filter by resolution.
1a. If the requested resolution is not available, go to the next available one.
1b. If the requested resolution is available, then move onto next step.
2. See if there is a progressive=True. 
2a. If progressive=True, then download it, and we are done.
2b. If progressive=False, then download it still.
3. Merge both the audio and video files.
"""


class YTBot:
    """
    Python implementation of the YouTube Scraping Bot.

    """

    def __init__(self, list_urls=None, extract_path=None):
        """
        Creates an instance of the YTBot.
        
        Parameters
        ----------
        list_urls : list, optional
            List containing urls represented as a string, by default None.
        extract_path : str, optional
            Absolute path to the folder where everything will be saved, by default None.

        Returns
        -------
        None

        """
        self.list_urls = list_urls
        self.n_urls = len(self.list_urls)
        self.extract_path = extract_path

    def download(self):
        """
        Downloads a video from YouTube and saves it to the ``extract_path`` directory.

        Parameters
        ----------
        None

        Return
        ------
        None

        """
        for k, url in enumerate(self.list_urls):
            video = pytube.YouTube(url)
            video_title = video.player_response.get("videoDetails", {}).get("title")
            print(video_title)
            print(type(video_title))
            # print(video.streams)
            """
            print(
                "Downloading {} with resolution {}".format(
                    re.sub(
                        r" +",
                        " ",
                        video.player_response.get("videoDetails", {}).get("title"),
                    ),
                    video.streams.get_by_itag(136).resolution,
                )
            )
            """
            """
            print("------------------------------------------------")
            print(video.streams.filter(resolution="1080p")[0].itag)
            print("\n")
            print(video.streams.filter(type="audio"))
            print("------------------------------------------------")
            print("\n")
            video.streams.get_by_itag(137).download(
                output_path=self.extract_path, filename_prefix="video"
            )
            video.streams.get_by_itag(140).download(
                output_path=self.extract_path, filename_prefix="audio"
            )
            # Once you are done downloading, then you can combine the video and audio.
            video_title = re.sub(" ", "\ ", video_title)
            video_title = re.sub(":", "", video_title)
            print(
                "ffmpeg -i {0}/video{1}.mp4 -i {2}/audio{3}.mp4 -c:v copy -c:a aac {4}.mp4".format(
                    self.extract_path,
                    video_title,
                    self.extract_path,
                    video_title,
                    video_title,
                )
            )
            os.system(
                "ffmpeg -i {0}/video{1}.mp4 -i {2}/audio{3}.mp4 -c:v copy -c:a aac {4}.mp4".format(
                    self.extract_path,
                    video_title,
                    self.extract_path,
                    video_title,
                    video_title,
                )
            )
            os.system(
                "rm -rf {0}/video{1}.mp4 {2}/audio{3}.mp4".format(
                    self.extract_path, video_title, self.extract_path, video_title
                )
            )
            """
            allowed_resolutions = ["1080p", "720p", "360p", "240p"]

            best_found = False
            best_resolution = 1080
            for resolution in allowed_resolutions:
                if best_found is True:
                    break
                stream_list = video.streams.filter(
                    resolution=resolution, mime_type="video/mp4", type="video"
                )
                if len(stream_list) == 0:
                    print("No streams in {}".format(resolution))
                else:
                    best_found = True
                    best_resolution = resolution
                    print("------------------------------------------------")
                    print("There are streams in {}".format(resolution))
                    print(stream_list)
                    print("------------------------------------------------")
                    print("\n")

                    video_itag = stream_list[0].itag

            audio_streams = video.streams.filter(type="audio", mime_type="audio/mp4")
            audio_itag = audio_streams[0].itag

            # Download the videos
            video.streams.get_by_itag(video_itag).download(
                output_path=self.extract_path, filename="video{}".format(k)
            )
            video.streams.get_by_itag(audio_itag).download(
                output_path=self.extract_path, filename="audio{}".format(k)
            )
            # Once you are done downloading, then you can combine the video and audio.
            # video_title = re.sub(" ", "\ ", video_title)
            # video_title = re.sub(":", "", video_title)
            """
            print(
                "ffmpeg -i {0}/video{1}.mp4 -i {2}/audio{3}.mp4 -c:v copy -c:a aac {4}.mp4".format(
                    self.extract_path,
                    video_title,
                    self.extract_path,
                    video_title,
                    video_title,
                )
            )
            """
            os.system(
                "ffmpeg -i {0}/video{1}.mp4 -i {2}/audio{3}.mp4 -c:v copy -c:a aac video{4}_{5}.mp4".format(
                    self.extract_path, k, self.extract_path, k, k, best_resolution
                )
            )
            os.system(
                "rm -rf {0}/video{1}.mp4 {2}/audio{3}.mp4".format(
                    self.extract_path, k, self.extract_path, k
                )
            )


'''
class YTBot:
    """
    Python implementation of the YouTube video downloading bot.

    """

    def __init__(self, list_of_urls, download_path=None, desired_resolution):
        """
        Instantiates a YTBot object.
        
        Parameters
        ----------
        list_of_urls : list (of str), optional
            [description], by default None
        download_path : str, optional
            Absolute path to the folder where everything will be saved, by default None. If None, then the defualt directory is the current directory.

        Returns
        -------
        None

        """
        self.list_of_urls = list_of_urls
        self.num_urls = len(self.list_of_urls)
        self.extract_path = extract_path

    def download_videos(self):
        """
        Downloads a video from YouTube and saves it to the ``download_path`` directory.

        Parameters
        ----------
        None

        Return
        ------
        None

        """
        for url in self.list_of_urls:
            video = pytube.YouTube(url)
            avail_streams = video.streams
'''
