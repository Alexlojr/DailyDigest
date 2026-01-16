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


class RssScienceFeed:
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



    def science_daily_rss(self) -> List[Tuple[str, str]]:
        """Get Science Daily RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://www.sciencedaily.com/rss/all.xml',
            'Science Daily',
            limit=3
        )

    def nasa_rss(self) -> List[Tuple[str, str]]:
        """Get NASA RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://www.nasa.gov/rss/dyn/breaking_news.rss',
            'NASA',
            limit=3
        )

    def nature_rss(self) -> List[Tuple[str, str]]:
        """Get Nature RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://www.nature.com/nature.rss',
            'Nature',
            limit=3
        )

    def get_news(self) -> List[Tuple[str, str, str]]:
        """Fetch all enabled RSS news sources
        Returns: List of (source, title, link)
        """
        self.news_list = []

        rss_config = self.config.get("rss_feeds", {})

        if rss_config.get("sci_rss"):
            print("Fetching Science Daily RSS...")
            for title, link in self.science_daily_rss():
                self.news_list.append(("Science Daily", title, link))

        if rss_config.get("nas_rss"):
            print("Fetching NASA RSS...")
            for title, link in self.nasa_rss():
                self.news_list.append(("NASA", title, link))

        if rss_config.get("nat_rss"):
            print("Fetching Nature RSS...")
            for title, link in self.nature_rss():
                self.news_list.append(("Nature", title, link))

        return self.news_list


if __name__ == "__main__":
    rss = RssScienceFeed(config_data)
    news = rss.get_news()

    print("\nRSS Headlines\n")
    for source, title, link in news:
        print(f"{source}: {title}")
        print(f"->{link}\n")
