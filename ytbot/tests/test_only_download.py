"""
Python file that only downloads videos from YouTube.

This test script was written before the removal tool introduced later on in ``_filter_available_nonthreading``.

"""

import os
import time

import glob
import pytube
import itertools
from ytbot.contrib.__main__ import YouTubeDownloader


def get_info():
    suffix_names = [
        f
        for f in os.listdir("/Users/shu/Documents/Datasets/LRS3/trainval")
        if not f.startswith(".")
    ]
    root_path = "/Users/shu/Documents/Datasets/VGG_Lipreading/trainval"
    urls = ["https://youtube.com/watch?v=" + item for item in suffix_names]

    return suffix_names, root_path, urls


def test_one(suffix_names, root_path, urls):
    ytdownloader = YouTubeDownloader(urls[1], extract_path=root_path)
    ytdownloader._find_itags(pytube.YouTube(urls[1]))


def test_two(suffix_names, root_path, urls):
    ytdownloader = YouTubeDownloader(urls[0], extract_path=root_path)
    ytdownloader._is_valid(urls[0])


def test_three(suffix_names, root_path, urls):
    urls_subset = urls[:2]
    ytdownloader = YouTubeDownloader(urls_subset, extract_path=root_path)
    ytdownloader._filter_available_nonthreading(verbose=True)
    print("[INFO] The URL list after filtering is {}".format(ytdownloader.url_list))
    print(
        "[INFO] The number of URLs in the list after filtering is {}".format(
            ytdownloader.n_urls
        )
    )


def test_four(suffix_names, root_path, urls):
    urls_subset = urls[:4]
    ytdownloader = YouTubeDownloader(urls_subset, extract_path=root_path)
    ytdownloader._filter_available_nonthreading()
    print(ytdownloader.url_list)
    ytdownloader.download_all_videos()


if __name__ == "__main__":
    suffix_names, root_path, urls = get_info()

    # Test passed.
    print("".join("-" * 80))
    print("TEST ONE")
    print("".join("-" * 80))
    test_one(suffix_names, root_path, urls)

    # Test passed.
    print("".join("-" * 80))
    print("TEST TWO")
    print("".join("-" * 80))
    test_two(suffix_names, root_path, urls)

    # Test passed.
    print("".join("-" * 80))
    print("TEST THREE")
    print("".join("-" * 80))
    test_three(suffix_names, root_path, urls)

    # Test in progress.
    print("".join("-" * 80))
    print("TEST FOUR")
    print("".join("-" * 80))
    test_four(suffix_names, root_path, urls)

