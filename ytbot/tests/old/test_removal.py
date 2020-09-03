"""
Python script that removes URLs that are not valid from the folder list.

"""

import os
import time

import glob
import itertools
from ytbot.contrib.__main__ import YouTubeDownloader


def main():
    suffix_names = [
        f
        for f in os.listdir("/Users/shu/Documents/Datasets/LRS3/trainval")
        if not f.startswith(".")
    ]
    root_path = "/Users/shu/Documents/Datasets/VGG_Lipreading/trainval"
    urls = ["https://youtube.com/watch?v=" + suffix for suffix in suffix_names]

    ytdownloader = YouTubeDownloader(urls, extract_path=root_path)
    # ytdownloader._filter_available_nonthreading(verbose=True, remove_directory=True)


if __name__ == "__main__":
    main()
