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


class RssWorldFeed:
    def __init__(self, config_json):
        self.config = config_json
        self.news_list = []

    def _fetch_rss(self, url: str, source_name: str, limit: int = 3) -> List[Tuple[str, str]]:
        """Generic RSS fetcher"""
        try:
            feed = feedparser.parse(url)
            results = []

            for entry in feed.entries[:limit]:
                title = entry.get("title", "No title")
                link = entry.get("link", "")
                results.append((title, link))

            return results

        except Exception as e:
            print(f"Error fetching {source_name} RSS: {e}")
            return []



    def cnn_rss(self) -> List[Tuple[str, str]]:
        """Get CNN RSS feed (top x limit set)"""
        return self._fetch_rss(
            'http://rss.cnn.com/rss/edition.rss',
            'CNN',
            limit=2
        )

    def bbc_rss(self) -> List[Tuple[str, str]]:
        """Get BBC RSS feed (top x limit set)"""
        return self._fetch_rss(
            'http://feeds.bbci.co.uk/news/world/rss.xml',
            'BBC',
            limit=2
        )

    def nyt_rss(self) -> List[Tuple[str, str]]:
        """Get NYT RSS feed (top x limit set)"""
        return self._fetch_rss(
                'https://rss.nytimes.com/services/xml/rss/nyt/World.xml',
                'NYT',
                limit=2
        )

    def get_news(self) -> List[Tuple[str, str, str]]:
        """Fetch all enabled RSS news sources
        Returns: List of (source, title, link)
        """
        self.news_list = []

        rss_config = self.config.get("rss_feeds", {})

        if rss_config.get("cnn_rss"):
            print("Fetching CNN RSS...")
            for title, link in self.cnn_rss():
                self.news_list.append(("CNN", title, link))

        if rss_config.get("bbc_rss"):
            print("Fetching BBC RSS...")
            for title, link in self.bbc_rss():
                self.news_list.append(("BBC", title, link))

        if rss_config.get("nyt_rss"):
            print("Fetching NYT RSS...")
            for title, link in self.nyt_rss():
                self.news_list.append(("NYT", title, link))

        return self.news_list


if __name__ == "__main__":
    rss = RssWorldFeed(config_data)
    news = rss.get_news()

    print("\nRSS Headlines\n")
    for source, title, link in news:
        print(f"{source}: {title}")
        print(f"->{link}\n")
