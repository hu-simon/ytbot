import os
import time

import glob
import itertools
from ytbot.__main__ import YouTubeDownloader


def create_directories():
    suffix_names = [
        f
        for f in os.listdir("/Users/shu/Documents/Datasets/LRS3/trainval")
        if not f.startswith(".")
    ]
    root_path = "/Users/shu/Documents/Datasets/VGG_Lipreading/trainval"
    paths = [os.path.join(root_path, suffix) for suffix in suffix_names]
    subdirectories = [
        "frames",
        "media/captions/raw",
        "media/captions/manual",
        "media/raw_audio",
        "media/raw_video",
        "media/comb_video",
    ]
    prods = list(itertools.product(paths, subdirectories))
    paths = ["/".join(item) for item in prods]

    for path in paths:
        try:
            os.makedirs(path)
        except OSError:
            print("[INFO] Failed to create {}".format(path))
        else:
            print("[INFO] Successfully created {}".format(path))

    return suffix_names, root_path


def download_video(suffix_names, root_path):
    urls = ["https://youtube.com/watch?v=" + item for item in suffix_names]

    print("[INFO] Downloading {}".format(urls[1]))

    ytdownloader = YouTubeDownloader(urls[1], extract_path=root_path)
    ytdownloader.download_all_videos()

def main():
    suffix_names, root_path = create_directories()
    download_video(suffix_names, root_path)


if __name__ == "__main__":
    main()
