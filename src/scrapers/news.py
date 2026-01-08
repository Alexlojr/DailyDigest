import requests
import json
from bs4 import BeautifulSoup


class NewsScraper:
    def __init__(self, config_json):
        self.config_json = config_json

    def get_cnn_news(self)-> str:
        #get cnn main headline news
        target = requests.get('https://edition.cnn.com/')
        news_soup = BeautifulSoup(target.text,"html.parser")
        cnn_title = news_soup.find("h2",{"class":"container__title_url-text container_lead-package__title_url-text"}).text
        return cnn_title

    def get_bbc_news(self)-> str:
        #get bbc main headline news
        target = requests.get('https://www.bbc.com/')
        news_soup = BeautifulSoup(target.text,"html.parser")
        bbc_title = news_soup.find("h2",{"class":"sc-fa814188-3 jaHqrc"}).text
        return bbc_title

    def get_nyt_news(self)-> str:
        #get NYT main headline news
        target = requests.get('https://www.nytimes.com/section/world')
        news_soup = BeautifulSoup(target.text,"html.parser")
        nyt_title = news_soup.find("h3",{"class":"css-1ykb5sd e1hr934v2"}).text
        return nyt_title

    def get_forbes_news(self)-> str:
        #get forbes main headline news
        target = requests.get('https://www.forbes.com/')
        news_soup = BeautifulSoup(target.text,"html.parser")
        forbes_title = news_soup.find("a", {"class": "qGitkxSR zPmmmf5g _436GZp59"}).text
        return forbes_title

    def get_foxnews_news(self)-> str:
        target = requests.get('https://foxnews.com/')
        news_soup = BeautifulSoup(target.text,"html.parser")
        foxnews_title = news_soup.find("h3",{"class":"title"}).text
        return foxnews_title

    def get_jacobin_news(self)-> str:
        target = requests.get('https://jacobin.com/')
        news_soup = BeautifulSoup(target.text,"html.parser")
        jacobin_title = news_soup.find("h2",{"class":"hm-dg__title hm-sd-py__title hm-sd-b-py__title"}).text
        return jacobin_title



    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config_data = json.load(f)
    except FileNotFoundError:
        print('config.json not found')

    titles_list = []

    def get_news(self,config_data:dict,titles_list:list) -> list:

        if config_data["web_scrapper"]["ccn_news"]:
            titles_list.append(self.get_cnn_news())

        if config_data["web_scrapper"]["bbc_news"]:
            titles_list.append(self.get_bbc_news())

        if config_data["web_scrapper"]["nyt_news"]:
            titles_list.append(self.get_nyt_news())

        if config_data["web_scrapper"]["frb_news"]:
            titles_list.append(self.get_forbes_news())

        if config_data["web_scrapper"]["fxn_news"]:
            titles_list.append(self.get_foxnews_news())

        if config_data["web_scrapper"]["jcb_news"]:
            titles_list.append(self.get_jacobin_news())


        return titles_list


if __name__ == '__main__':
    test=NewsScraper
    print(test)