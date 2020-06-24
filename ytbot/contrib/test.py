import time

from ytbot.contrib.__main__ import YouTubeDownloader


def main():
    url_list = [
        "https://www.youtube.com/watch?v=7fQG4CcoRuM",
        "https://www.youtube.com/watch?v=QJ2ZM-3YTg0",
        "https://www.youtube.com/watch?v=7-MJZJjJs4A",
        "https://www.youtube.com/watch?v=EkwqPJZe8ms",
        "https://www.youtube.com/watch?v=3tR6mKcBbT4",
    ]

    ytdownloader = YouTubeDownloader(
        url_list, extract_path="/Users/administrator/Desktop/ytbot/videos/"
    )
    start_time = time.perf_counter()
    ytdownloader.download_all_videos()
    finish_time = time.perf_counter()

    print("Operation took {} second(s).".format(finish_time - start_time))


if __name__ == "__main__":
    main()
