"""Python test that tests the scraping ability of the YouTube scraper for the Lip Reading dataset.
"""

import os
import time

import glob
import itertools
from ytbot.contrib.__main__ import YouTubeDownloader


def main():
    # Prepare the paths for loading and saving.
    suffix_names = [
        f
        for f in os.listdir("/Users/shu/Documents/Datasets/LRS3/trainval")
        if not f.startswith(".")
    ]
    root_path = "/Users/shu/Documents/Datasets/LRVideos/trainval"
    paths = [os.path.join(root_path, suffix) for suffix in suffix_names]
    subdirectories = [
        "frames",
        "media/captions/raw",
        "media/captions/manual",
        "media/video",
        "media/audio",
    ]
    prods = list(itertools.product(paths, subdirectories))
    paths = ["/".join(item) for item in prods]

    # Create these directories.
    for path in paths:
        try:
            os.makedirs(path)
        except OSError:
            print("Failed to create the directory at {}.".format(path))
        else:
            print("Successfully created the directory at {}.".format(path))

    print("".join("-" * 80))
    print("DOWNLOADING YOUTUBE VIDEOS")
    print("".join("-" * 80))

    # The plan then is to finish this code so that we can download everything and put the data into the folders.
    urls = ["https://youtube.com/watch?v=" + item for item in suffix_names]
    urls_subset = urls[:2]
    print(urls_subset)
    # ytdownloader = YouTubeDownloader(urls, extract_path=root_path)
    # ytdownloader.download_all_videos()


if __name__ == "__main__":
    main()
