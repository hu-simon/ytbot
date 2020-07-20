import time

from ytbot.__main__ import YouTubeDownloader


def main():
    url_list = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=xFrGuyw1V8s",
    ]

    extract_path = "/Users/shu/Downloads/"
    ytdownloader = YouTubeDownloader(url_list, extract_path=extract_path)
    start_time = time.perf_counter()
    ytdownloader.download_all_videos()
    finish_time = time.perf_counter()

    print("Entire operation took {} seconds(s).".format(finish_time - start_time))


if __name__ == "__main__":
    main()
