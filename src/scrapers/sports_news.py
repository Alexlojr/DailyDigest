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


class RssSportsFeed:
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



    def espn_rss(self) -> List[Tuple[str, str]]:
        """Get ESPN RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://www.espn.com/espn/rss/news',
            'ESPN',
            limit=2
        )

    def bbc_sports_rss(self) -> List[Tuple[str, str]]:
        """Get BBC Sports RSS feed (top x limit set)"""
        return self._fetch_rss(
            'http://feeds.bbci.co.uk/sport/rss.xml',
            'BBC Sports',
            limit=2
        )

    def sky_sports_rss(self) -> List[Tuple[str, str]]:
        """Get Sky Sports RSS feed (top x limit set)"""
        return self._fetch_rss(
                'http://feeds.skynews.com/feeds/rss/sports.xml',
            'Sky Sports',
            limit=2
        )



    def get_news(self) -> List[Tuple[str, str, str]]:
        """Fetch all enabled RSS news sources
        Returns: List of (source, title, link)
        """
        self.news_list = []

        rss_config = self.config.get("rss_feeds", {})

        if rss_config.get("epn_rss"):
            print("Fetching ESPN RSS...")
            for title, link in self.espn_rss():
                self.news_list.append(("ESPN", title, link))

        if rss_config.get("bsp_rss"):
            print("Fetching BBC Sports RSS...")
            for title, link in self.bbc_sports_rss():
                self.news_list.append(("BBC Sports", title, link))

        if rss_config.get("sky_rss"):
            print("Fetching Sky Sports RSS...")
            for title, link in self.sky_sports_rss():
                self.news_list.append(("Sky Sports", title, link))


        return self.news_list


if __name__ == "__main__":
    rss = RssSportsFeed(config_data)
    news = rss.get_news()

    print("\nRSS Headlines\n")
    for source, title, link in news:
        print(f"{source}: {title}")
        print(f"->{link}\n")