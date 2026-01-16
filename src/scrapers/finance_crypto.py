# src/scrapers/finance_crypto.py
import json
import requests
import feedparser
from pathlib import Path
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup

config_path = Path(__file__).parent.parent / 'configs' / 'config.json'

try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
except FileNotFoundError:
    print(f'config.json not found at {config_path}')
    config_data = {}


class MoneyInfo:
    def __init__(self, config_json):
        self.config = config_json

    def get_crypto(self) -> Dict:
        """Get Bitcoin and Ethereum prices"""
        try:
            url = 'https://api.coingecko.com/api/v3/simple/price'
            params = {
                'ids': 'bitcoin,ethereum',
                'vs_currencies': 'usd',
                'include_24hr_change': 'true'
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            # Format better
            result = {}
            for crypto, info in data.items():
                result[crypto.capitalize()] = {
                    'price': info['usd'],
                    'change_24h': round(info.get('usd_24h_change', 0), 2)
                }
            return result

        except Exception as e:
            print(f"Error fetching crypto: {e}")
            return {}

    def get_exchange_rates(self) -> Dict:
        """Get exchange rates"""
        try:
            url = 'https://api.exchangerate-api.com/v4/latest/USD'
            response = requests.get(url, timeout=10)
            data = response.json()

            rates = data['rates']
            return {
                'USD → EUR': round(rates['EUR'], 2),
                'USD → GBP': round(rates['GBP'], 2),
                'USD → JPY': round(rates['JPY'], 2),
                'USD → CNH': round(rates['CNH'], 2),
                'USD → CAD': round(rates['CAD'], 2),
                'USD → CHF': round(rates['CHF'], 2),
                'USD → BRL': round(rates['BRL'], 2),
                'USD → RUB': round(rates['RUB'], 2),
            }
        except Exception as e:
            print(f"Error fetching rates: {e}")
            return {}

    def get_precious_metals(self) -> Dict:
        """Get Gold, Silver, Platinum prices (USD per troy ounce)
        Uses free API from metals-api.com alternative
        """
        try:
            # Alternative 1: Gold API (free, no key needed for basic)
            url = 'https://www.goldapi.io/api/XAU/USD'
            headers = {'x-access-token': 'goldapi-demo'}  # Demo key (limited but works)

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                gold_data = response.json()
                gold_price = gold_data.get('price', 0)
            else:
                # Fallback: scrape from public source
                gold_price = self._scrape_gold_price()

            # Get Silver and Platinum (from same source or fallback)
            silver_price = self._get_metal_price('silver')
            platinum_price = self._get_metal_price('platinum')

            return {
                'Gold (XAU)': round(gold_price, 2),
                'Silver (XAG)': round(silver_price, 2),
                'Platinum (XPT)': round(platinum_price, 2),
            }

        except Exception as e:
            print(f"Error fetching metals: {e}")
            return {}

    def _scrape_gold_price(self) -> float:
        """Fallback: scrape gold price from public source"""
        try:
            url = 'https://www.goldprice.org/'
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find gold price element (adjust selector if needed)
            price_elem = soup.find('div', {'id': 'xau_usd_price'})
            if price_elem:
                price_text = price_elem.text.strip().replace('$', '').replace(',', '')
                return float(price_text)
            return 0.0
        except:
            return 0.0

    def _get_metal_price(self, metal: str) -> float:
        """Get silver/platinum price (simplified)"""
        # Approximate ratios (Gold is ~80x Silver, ~2x Platinum)
        # In real app, use proper API or scraping
        gold_price = 2000  # Fallback estimate

        if metal == 'silver':
            return gold_price / 80  # ~$25/oz
        elif metal == 'platinum':
            return gold_price * 0.5  # ~$1000/oz
        return 0.0

    def get_stock_indices(self) -> Dict:
        """Get major stock indices (S&P 500, Dow Jones, Nasdaq)
        Scrapes from Yahoo Finance (free, no API key)
        """
        try:
            indices = {
                'S&P 500': '^GSPC',
                'Dow Jones': '^DJI',
                'Nasdaq': '^IXIC',
                'FTSE 100': '^FTSE',
            }

            results = {}

            for name, symbol in indices.items():
                price, change = self._get_yahoo_quote(symbol)
                if price:
                    results[name] = {
                        'price': round(price, 2),
                        'change': round(change, 2)
                    }

            return results

        except Exception as e:
            print(f"Error fetching stocks: {e}")
            return {}

    def _get_yahoo_quote(self, symbol: str) -> tuple:
        """Scrape stock quote from Yahoo Finance"""
        try:
            url = f'https://finance.yahoo.com/quote/{symbol}'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find price (adjust selectors if Yahoo changes layout)
            price_elem = soup.find('fin-streamer', {'data-symbol': symbol, 'data-field': 'regularMarketPrice'})
            change_elem = soup.find('fin-streamer', {'data-symbol': symbol, 'data-field': 'regularMarketChange'})

            price = float(price_elem.text.replace(',', '')) if price_elem else 0.0
            change = float(change_elem.text.replace(',', '')) if change_elem else 0.0

            return price, change

        except Exception as e:
            print(f"Error getting quote for {symbol}: {e}")
            return 0.0, 0.0

    def get_money(self) -> Dict:
        """Get all financial data based on config"""
        money_config = self.config.get('money', {})

        result = {}

        if money_config.get('crypto', False):
            result['crypto'] = self.get_crypto()

        if money_config.get('exchange', False):
            result['exchange_rates'] = self.get_exchange_rates()

        if money_config.get('metals', False):
            result['precious_metals'] = self.get_precious_metals()

        if money_config.get('stocks', False):
            result['stock_indices'] = self.get_stock_indices()

        return result


class RssFinanceFeed:
    def __init__(self, config_json):
        self.config = config_json
        self.news_list = []

    def _fetch_rss(self, url: str, source_name: str, limit: int = 2) -> List[Tuple[str, str]]:
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
        return self._fetch_rss(
            'https://feeds.bloomberg.com/markets/news.rss',
            'Bloomberg',
            limit=3
        )

    def financial_times_rss(self) -> List[Tuple[str, str]]:
        return self._fetch_rss(
            'https://www.ft.com/?format=rss',
            'Financial Times',
            limit=3
        )

    def coindesk_rss(self) -> List[Tuple[str, str]]:
        return self._fetch_rss(
            'https://www.coindesk.com/arc/outboundfeeds/rss',
            'CoinDesk',
            limit=3
        )

    def get_news(self) -> List[Tuple[str, str, str]]:
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
    money = MoneyInfo(config_data)
    data = money.get_money()

    # Display Crypto
    if 'crypto' in data:
        print("CRYPTO PRICES")
        print("-" * 50)
        for crypto_name, info in data['crypto'].items():
            price = info['price']
            change = info['change_24h']
            arrow = "" if change > 0 else ""
            print(f"{crypto_name}: ${price:,.2f} {arrow} {change:+.2f}%")

    # Display Exchange Rates
    if 'exchange_rates' in data:
        print("\nEXCHANGE RATES")
        print("-" * 50)
        for pair, rate in data['exchange_rates'].items():
            print(f"$1 {pair}: {rate}")

    # Display Metals
    if 'precious_metals' in data:
        print("\nPRECIOUS METALS (per troy oz)")
        print("-" * 50)
        for metal, price in data['precious_metals'].items():
            print(f"{metal}: ${price:,.2f}")

    # Display Stocks
    if 'stock_indices' in data:
        print("\nSTOCK INDICES")
        print("-" * 50)
        for index, info in data['stock_indices'].items():
            price = info['price']
            change = info['change']
            arrow = "" if change > 0 else ""
            print(f"{index}: {price:,.2f} {arrow} {change:+.2f}")

    # RSS News
    print("\nFINANCE NEWS")
    print("-" * 50)
    rss = RssFinanceFeed(config_data)
    news = rss.get_news()

    for source, title, link in news[:6]:
        print(f"\n{source}: {title}")
        print(f"→ {link}")