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


class RssEntertainmentFeed:
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



    def rottentomatos_news_rss(self) -> List[Tuple[str, str]]:
        """Get Rotten Tomatoes RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://editorial.rottentomatoes.com/feed/',
            'Rotten Tomatoes',
            limit=3
        )

    def collider_news_rss(self) -> List[Tuple[str, str]]:
        """Get Collider RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://collider.com/feed/',
            'Collider',
            limit=3
        )

    def tvline_news_rss(self) -> List[Tuple[str, str]]:
        """Get TVline RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://tvline.com/feed/',
            'TVline',
            limit=3
        )

    def hollywoodreportertv_news_rss(self) -> List[Tuple[str, str]]:
        """Get The Hollywood Reporter TV RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://www.hollywoodreporter.com/c/tv/tv-news/feed/',
            'Hollywood Reporter TV',
            limit=3
        )

    def ign_news_rss(self) -> List[Tuple[str, str]]:
        """Get IGN RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://feeds.feedburner.com/ign/games-all',
            'IGN',
            limit=3
        )

    def polygon_news_rss(self) -> List[Tuple[str, str]]:
        """Get Polygon RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://www.polygon.com/rss/index.xml',
            'Polygon',
            limit=3
        )

    def crunchyrolls_news_rss(self) -> List[Tuple[str, str]]:
        """Get Crunchyrolls RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://cr-news-api-service.prd.crunchyrollsvc.com/v1/en-US/rss',
            'Crunchyrolls',
            limit=3
        )

    def myanimelist_news_rss(self) -> List[Tuple[str, str]]:
        """Get Myanimelist RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://myanimelist.net/rss/news.xml',
            'Myanimelist',
            limit=3
        )

    def pitchfork_news_rss(self) -> List[Tuple[str, str]]:
        """Get Pitchfork RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://pitchfork.com/rss/news/',
            'Pitchfork',
            limit=3
        )

    def nme_news_rss(self) -> List[Tuple[str, str]]:
        """Get NME RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://www.nme.com/news/music/feed',
            'NME',
            limit=3
        )

    def bookriot_news_rss(self) -> List[Tuple[str, str]]:
        """Get BookRiot RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://bookriot.com/feed/',
            'BookRiot',
            limit=3
        )

    def bookbrowse_news_rss(self) -> List[Tuple[str, str]]:
        """Get BookBrowse RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://www.bookbrowse.com/rss/book_news.rss',
            'BookBrowse',
            limit=3
        )

    def comicquarters_news_rss(self) -> List[Tuple[str, str]]:
        """Get ComicQuarters RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://comicquarters.com/feed/',
            'ComicQuarters ',
            limit=3
        )

    def playbill_news_rss(self) -> List[Tuple[str, str]]:
        """Get PlayBites RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://playbill.com/rss/news',
            'PlayBites',
            limit=3
        )

    def tmz_news_rss(self) -> List[Tuple[str, str]]:
        """Get TMZ RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://www.tmz.com/rss.xml',
            'TMZ',
            limit=3
        )

    def dicebreaker_news_rss(self) -> List[Tuple[str, str]]:
        """Get Dicebreaker RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://www.dicebreaker.com/feed',
            'Dicebreaker',
            limit=3
        )

    def variety_news_rss(self) -> List[Tuple[str, str]]:
        """Get Variety RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://variety.com/feed/',
            'Variety',
            limit=3
        )

    def artnet_news_rss(self) -> List[Tuple[str, str]]:
        """Get ArtNet RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://news.artnet.com/feed',
            'ArtNet',
            limit=3
        )

    def podcasts_news_rss(self) -> List[Tuple[str, str]]:
        """Get Podecasts RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://podnews.net/rss',
            'PodCast News',
            limit=3
        )





    def get_news(self) -> List[Tuple[str, str, str]]:
        """Fetch all enabled RSS news sources
        Returns: List of (source, title, link)
        """
        self.news_list = []

        rss_config = self.config.get("entertainment", {})

        if rss_config.get("movies"):
            print("Fetching Rotten Tomatoes RSS...")
            for title, link in self.rottentomatos_news_rss():
                self.news_list.append(("Rotten Tomatoes", title, link))

        if rss_config.get("movies"):
            print("Fetching Collider News RSS...")
            for title, link in self.collider_news_rss():
                self.news_list.append(("Collider News", title, link))

        if rss_config.get("tv_series"):
            print("Fetching TVline News RSS...")
            for title, link in self.tvline_news_rss():
                self.news_list.append(("TVline", title, link))

        if rss_config.get("tv_series"):
            print("Fetching Hollywood Reporter TV...")
            for title, link in self.hollywoodreportertv_news_rss():
                self.news_list.append(("Hollywood Reporter", title, link))

        if rss_config.get("games"):
            print("Fetching IGN RSS...")
            for title, link in self.ign_news_rss():
                self.news_list.append(("IGN", title, link))

        if rss_config.get("games"):
            print("Fetching Polygon RSS...")
            for title, link in self.polygon_news_rss():
                self.news_list.append(("Polygon", title, link))

        if rss_config.get("anime"):
            print("Fetching Crunchyrolls RSS...")
            for title, link in self.crunchyrolls_news_rss():
                self.news_list.append(("Crunchyrolls", title, link))

        if rss_config.get("anime"):
            print("Fetching Myanimelist RSS...")
            for title, link in self.myanimelist_news_rss():
                self.news_list.append(("Myanimelist", title, link))

        if rss_config.get("music"):
            print("Fetching Pitchfork RSS...")
            for title, link in self.nme_news_rss():
                self.news_list.append(("Pitchfork", title, link))

        if rss_config.get("music"):
            print("Fetching NME RSS...")
            for title, link in self.nme_news_rss():
                self.news_list.append(("NME", title, link))

        if rss_config.get("books"):
            print("Fetching BookRiot RSS...")
            for title, link in self.bookriot_news_rss():
                self.news_list.append(("BookRiot", title, link))

        if rss_config.get("books"):
            print("Fetching BookBrowse RSS...")
            for title, link in self.bookbrowse_news_rss():
                self.news_list.append(("BookBrowse", title, link))

        if rss_config.get("comics"):
            print("Fetching ComicQuarters RSS...")
            for title,link in self.comicquarters_news_rss():
                self.news_list.append(("ComicQuarters ", title, link))

        if rss_config.get("theater"):
            print("Fetching playbill RSS...")
            for title, link in self.playbill_news_rss():
                self.news_list.append(("Playbill", title, link))

        if rss_config.get("celebrity"):
            print("Fetching Movie RSS...")
            for title,link in self.tmz_news_rss():
                self.news_list.append(("TMZ", title, link))

        if rss_config.get("tabletop"):
            print("Fetching Dicebreaker RSS...")
            for title, link in self.dicebreaker_news_rss():
                self.news_list.append(("Dicebreaker", title, link))

        if rss_config.get("pop_culture"):
            print("Fetching Variety RSS...")
            for title, link in self.variety_news_rss():
                self.news_list.append(("Variety", title, link))

        if rss_config.get("art/museums"):
            print("Fetching ArtNet RSS...")
            for title, link in self.artnet_news_rss():
                self.news_list.append(("ArtNet", title, link))

        if rss_config.get("podcast"):
            print("Fetching Podcast News RSS...")
            for title,link in self.podcasts_news_rss():
                self.news_list.append(("Podcast", title, link))


        return self.news_list


if __name__ == "__main__":
    rss = RssEntertainmentFeed(config_data)
    news = rss.get_news()

    print("\nRSS Headlines\n")
    for source, title, link in news:
        print(f"{source}: {title}")
        print(f"->{link}\n")
