import json
import requests
import feedparser
from bs4 import BeautifulSoup
from pathlib import Path
from typing import List, Tuple, Dict

#load config with proper path
config_path = Path(__file__).parent.parent / 'configs' / 'config.json'

try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
except FileNotFoundError:
    print(f'config.json not found at {config_path}')
    config_data = {}


    def _safe_scrape(url: str, tag: str, attrs: Dict) -> tuple:
        """Helper to safely scrape with error handling"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            element = soup.find(tag, attrs)
            if element:
                #get link
                title = element.text.strip()

                # if element is <a>, get href
                if tag == 'a':
                    link = element.get('href', url)
                else:

                    a_tag = element.find('a') or element.find_parent('a')
                    link = a_tag.get('href', url) if a_tag else url


                if link.startswith('/'):
                    from urllib.parse import urljoin
                    link = urljoin(url, link)

                return title, link
            else:
                return f"[Element not found]", url

        except Exception as e:
            return f"[Error: {str(e)}]", url

def get_crypto():
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {'ids': 'bitcoin,ethereum', 'vs_currencies': 'usd'}
    response = requests.get(url, params=params)
    return response.json()

def get_exchange_rate():

    return _safe_scrape(
        'https://www.oanda.com/currency-converter/en/?from=USD&to=GBP&amount=1',
        'input',
        {"class":'MuiInputBase-input MuiFilledInput-input'}
    )











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



    def bloomberg_rss(self) -> List[Tuple[str, str]]:
        """Get Bloomberg RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://feeds.bloomberg.com/markets/news.rss',
            'Bloomberg',
            limit=2
        )

    def financial_times_rss(self) -> List[Tuple[str, str]]:
        """Get Financial Times RSS feed (top x limit set)"""
        return self._fetch_rss(
            'https://www.ft.com/?format=rss',
            'Financial Times',
            limit=2
        )

    def coindesk_rss(self) -> List[Tuple[str, str]]:
        """Get CoinDesk RSS feed (top x limit set)"""
        return self._fetch_rss(
                'https://www.coindesk.com/arc/outboundfeeds/rss',
                'CoinDesk',
                limit=2
        )

    def get_news(self) -> List[Tuple[str, str, str]]:
        """Fetch all enabled RSS news sources
        Returns: List of (source, title, link)
        """
        self.news_list = []

        rss_config = self.config.get("rss_feeds", {})

        if rss_config.get("blb_rss"):
            print("Fetching Bloomberg RSS...")
            for title, link in self.bloomberg_rss():
                self.news_list.append(("Bloomberg", title, link))

        if rss_config.get("fnt_rss"):
            print("Fetching Financial Times RSS...")
            for title, link in self.financial_times_rss():
                self.news_list.append(("Financial Times", title, link))

        if rss_config.get("cnd_rss"):
            print("Fetching CoinDesk RSS...")
            for title, link in self.coindesk_rss():
                self.news_list.append(("CoinDesk", title, link))

        return self.news_list


if __name__ == "__main__":
    rss = RssScienceFeed(config_data)
    news = rss.get_news()

    print("\nRSS Headlines\n")
    for source, title, link in news:
        print(f"{source}: {title}")
        print(f"->{link}\n")

    teste=get_crypto()
    for key, value in teste.items():
        print(f"{key}: {value}")

    print(get_exchange_rate())
