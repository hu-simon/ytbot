"""
Python test script that tests manual entry of the URLs. 

The next Python test script should focus on testing the command line version of the scraper.
"""

import os
import time

import glob
import itertools
from ytbot.__main__ import YouTubeDownloader


def download_video(urls, extract_path):
    """Downloads videos using the links in ``urls`` and extracts them to ``extract_path``.
    
    Parameters
    ----------
    urls : list (of str)
        List containing the video URLs.
    extract_path : str
        Absolute path to the destination folder where the video and audio data is stored.
    
    Returns
    -------
    None

    """
    ytdownloader = YouTubeDownloader(urls, extract_path=extract_path)
    ytdownloader.download_all_videos()


def main():
    urls = ["https://www.youtube.com/watch?v=YLO7tCdBVrA"]
    extract_path = "/Users/administrator/Documents/Projects/ytbot/videos"

    download_video(urls=urls, extract_path=extract_path)


if __name__ == "__main__":
    main()
