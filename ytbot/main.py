import time

from YTBot import YTBot


def main():
    list_urls = [
        # https://www.youtube.com/watch?v=7fQG4CcoRuM",
        # "https://www.youtube.com/watch?v=QJ2ZM-3YTg0",
        # "https://www.youtube.com/watch?v=7-MJZJjJs4A",
        # "https://www.youtube.com/watch?v=EkwqPJZe8ms",
        "https://www.youtube.com/watch?v=3tR6mKcBbT4",
    ]

    bot = YTBot(
        list_urls=list_urls, extract_path="/Users/administrator/Desktop/ytbot/videos/"
    )
    start = time.time()
    bot.download()
    end = time.time()
    print("Entire operation took {} seconds.".format(end - start))

    # When done downloading, then all the files should be processed using the codec method.


if __name__ == "__main__":
    main()
