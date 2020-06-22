import time
import json
import configparser

from YTBot import YTBot


def main():
    links = [
        "https://www.youtube.com/watch?v=7fQG4CcoRuM",
        "https://www.youtube.com/watch?v=QJ2ZM-3YTg0",
        "https://www.youtube.com/watch?v=7-MJZJjJs4A",
        "https://www.youtube.com/watch?v=EkwqPJZe8ms",
        "https://www.youtube.com/watch?v=3tR6mKcBbT4",
    ]

    bot = YTBot(links, extract_path="/Users/administrator/Desktop/ytbot/videos/")
    start = time.time()
    bot.download()
    end = time.time()
    print("Entire operation took {} seconds.".format(end - start))


if __name__ == "__main__":
    main()
