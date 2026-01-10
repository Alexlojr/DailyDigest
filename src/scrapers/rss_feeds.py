import json
import feedparser
from pathlib import Path
from typing import List, Tuple

#load config with proper path
config_path = Path(__file__).parent.parent / 'configs' / 'config.json'

try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
except FileNotFoundError:
    print(f'config.json not found at {config_path}')
    config_data = {}

class RssFeed:
    def __init__(self, config_json):
        self.config_json = config_json

    def cnn_rss(self)-> tuple:
        rss_url = 'http://rss.cnn.com/rss/edition.rss'
        feed = feedparser.parse(rss_url)

        title = []
        link = []

        # pass the info to
        for entry in feed.entries[:3]:
            title.append(entry.get("title", "Sem título"))
            link.append(entry.get("link", ""))

        return title, link

    def bbc_rss(self)-> tuple:
        rss_url = 'http://feeds.bbci.co.uk/news/world/rss.xml'
        feed = feedparser.parse(rss_url)

        title = []
        link = []

        for entry in feed.entries[:3]:
            title.append(entry.get("title", "Sem título"))
            link.append(entry.get("link", ""))

        return title, link

    def get_news(self) -> List[tuple]:
        """Fetch all enabled news sources"""
        self.news_list = []

        scrapers_config = self.config_json.get("web_scrapper", {})

        if scrapers_config.get("cnn_rss"):
            print("Fetchting CNN RSS...")




#if __name__ == "__main__":
    # title, link = cnn_rss()
    # title1, link1 = bbc_rss()
    #
    # for index in range(len(title)):
    #     print(f'CNN: {title[index]}\n->{link[index]}')
    #
    # for index in range(len(title1)):
    #     print(f'BBC: {title[index]}\n->{link[index]}')
