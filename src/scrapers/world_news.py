import requests
import json
from bs4 import BeautifulSoup
from pathlib import Path
from typing import List,Dict


#load config with proper path
config_path = Path(__file__).parent.parent / 'configs' / 'config.json'

try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
except FileNotFoundError:
    print(f'config.json not found at {config_path}')
    config_data = {}



class NewsScraper:
    def __init__(self, config_json):
        #load config json
        self.config = config_json
        #create return list
        self.titles_list: List[str] = []

    def _safe_scrape(self, url: str, tag: str, attrs: Dict) -> tuple:
        """Helper to safely scrape with error handling"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            element = soup.find(tag, attrs)
            if element:
                #get link
                title = element.text.strip()

                # Se o elemento for <a>, pega href direto
                if tag == 'a':
                    link = element.get('href', url)
                else:
                    # Senão, procura <a> dentro ou próximo
                    a_tag = element.find('a') or element.find_parent('a')
                    link = a_tag.get('href', url) if a_tag else url

                # Corrige links relativos
                if link.startswith('/'):
                    from urllib.parse import urljoin
                    link = urljoin(url, link)

                return title, link
            else:
                return f"[Element not found]", url

        except Exception as e:
            return f"[Error: {str(e)}]", url

    def get_cnn_news(self) -> tuple:
        #get CNN main headline with link
        return self._safe_scrape(
            'https://edition.cnn.com/',
            "h2",
            {"class": "container__title_url-text container_spotlight-package__title_url-text"}
        )

    def get_bbc_news(self) -> tuple:
        #get BBC main headline
        return self._safe_scrape(
            'https://www.bbc.com/',
            "h2",
            {"class": "sc-fa814188-3 jaHqrc"}
        )

    def get_nyt_news(self) -> tuple:
        #get NYT main headline
        return self._safe_scrape(
            'https://www.nytimes.com/section/world',
            "h3",
            {"class": "css-1ykb5sd e1hr934v2"}
        )

    def get_forbes_news(self) -> tuple:
        #et Forbes main headline
        return self._safe_scrape(
            'https://www.forbes.com/',
            "a",
            {"class": "qGitkxSR zPmmmf5g _436GZp59"}
        )

    def get_foxnews_news(self) -> tuple:
        #get Fox News main headline
        return self._safe_scrape(
            'https://foxnews.com/',
            "h3",
            {"class": "title"}
        )

    def get_jacobin_news(self) -> tuple:
        #get Jacobin main headline
        return self._safe_scrape(
            'https://jacobin.com/',
            "h2",
            {"class": "hm-dg__title hm-sd-py__title hm-sd-b-py__title"}
        )

    def get_news(self) -> List[tuple]:
        """Fetch all enabled news sources"""
        self.titles_list = []

        scrapers_config = self.config.get("web_scrapper", {})

        if scrapers_config.get("cnn_news"):
            print("Fetching CNN...")
            title, link = self.get_cnn_news()
            self.titles_list.append(("CNN", title, link))

        if scrapers_config.get("bbc_news"):
            print("Fetching BBC...")
            title, link = self.get_bbc_news()
            self.titles_list.append(("BBC", title, link))

        if scrapers_config.get("nyt_news"):
            print("Fetching NYT...")
            title, link = self.get_nyt_news()
            self.titles_list.append(("NYT", title, link))

        if scrapers_config.get("frb_news"):
            print("Fetching Forbes...")
            title, link = self.get_forbes_news()
            self.titles_list.append(("Forbes", title, link))

        if scrapers_config.get("fxn_news"):
            print("Fetching Fox News...")
            title, link = self.get_foxnews_news()
            self.titles_list.append(("Fox News", title, link))

        if scrapers_config.get("jcb_news"):
            print("Fetching Jacobin...")
            title, link = self.get_jacobin_news()
            self.titles_list.append(("Jacobin", title, link))

        return self.titles_list


if __name__ == '__main__':

    test=NewsScraper(config_data)
    news = test.get_news()
    print("\nHeadlines \n")
    for source, title, link in news:
        print(f"{source}: {title}")
        print(f"-> {link}\n")
