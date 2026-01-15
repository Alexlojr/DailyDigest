import requests
from bs4 import BeautifulSoup
from typing import Dict

def _safe_scrape(url: str, tag: str, attrs: Dict) -> tuple:
    """Helper to safely scrape with error handling"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        element = soup.find(tag, attrs)
        if element:
            # get link
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