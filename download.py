"""
Main python script that downloads videos.
"""

import os
import time

import glob
import argparse
from ytbot.contrib.__main__ import YouTubeDownloader

parser = argparse.ArgumentParser(description="YouTube Video Downloader")

parser.add_argument(
    "--target_dest",
    type=str,
    help="Target destination where the videos are stored",
    required=True,
)
parser.add_argument(
    "--urls",
    type=str,
    help="Path to .txt file containing the URLs, each on a separate line",
)
parser.add_argument(
    "--download", dest="download", action="store_true", help="Enable download mode"
)

args = parser.parse_args()


def download(args, urls):
    ytdownloader = YouTubeDownloader(url_list=urls, extract_path=args.target_dest)
    ytdownloader.download_all_videos()


if __name__ == "__main__":

    if not os.path.exists(args.target_dest):
        raise ValueError("The target directory does not exist. Please try again.")

    f = open(args.urls, "r")
    urls = f.readlines()
    urls = [url.split("\n")[0] for url in urls]
    f.close()

    if args.download:
        download(args, urls)
