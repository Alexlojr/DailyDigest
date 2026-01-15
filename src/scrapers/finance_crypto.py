import json
import requests
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


class MoneyInfo:
    def __init__(self,config_json):
        self.config = config_json
        self.list = {}

    def get_crypto(self):
        url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {'ids': 'bitcoin,ethereum', 'vs_currencies': 'usd'}
        response = requests.get(url, params=params)
        return response.json()


    def get_exchange_rates(self):
        """Get exchange rates - NO API KEY needed!"""
        try:
            url = 'https://api.exchangerate-api.com/v4/latest/USD'
            response = requests.get(url)
            data = response.json()

            rates = data['rates']
            return {
                'USD -> EUR': round(rates['EUR'], 2),
                'USD -> GBP': round(rates['GBP'], 2),
                'USD -> JPY': round(rates['JPY'], 2),
                'USD -> CNH': round(rates['CNH'], 2),
                'USD -> CAD': round(rates['CAD'], 2),
                'USD -> CHF': round(rates['CHF'], 2),
                'USD -> BRL': round(rates['BRL'], 2),
                'USD -> RUB': round(rates['RUB'], 2),

            }
        except Exception as e :
            print(f"Error fetching rates: {e}")
            return {}



    def get_money(self):
        self.list = {}

        list.append(self.get_crypto())
        list.append(self.get_exchange_rates())
        return list








class RssFinanceFeed:
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
    # rss = RssFinanceFeed(config_data)
    # news = rss.get_news()
    #
    # print("\nRSS Headlines\n")
    # for source, title, link in news:
    #     print(f"{source}: {title}")
    #     print(f"->{link}\n")

    money = MoneyInfo(config_data)


    rates = money.get_money()
    print(rates)
    # for pair, rate in rates.items():
    #     print(f"$1 {pair}: {rate}")
    #
    # ratec = money.get_crypto()
    # for criptomoeda, dados in ratec.items():
    #     preco = dados['usd']
    #     print(f"1 {criptomoeda}: ${preco} USD ")

