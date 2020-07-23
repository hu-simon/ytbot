import time

from ytbot.__main__ import YouTubeDownloader


def main():
    url_list = [
        "https://www.youtube.com/watch?v=YLO7tCdBVrA",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    ]

    extract_path = "/Users/shu/Downloads/ytvideos"
    ytdownloader = YouTubeDownloader(url_list, extract_path=extract_path)
    ytdownloader.download_all_videos()
    ytdownloader.download_all_captions()


if __name__ == "__main__":
    main()
