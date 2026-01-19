from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import json

#load config with proper path
config_path = Path(__file__).parent.parent / 'configs' / 'config.json'

try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
except FileNotFoundError:
    print(f'config.json not found at {config_path}')
    config_data = {}


city = config_data['weather']['city']



#https://www.windy.com



chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
"""configure driver"""
driver = webdriver.Chrome(options = chrome_options)
driver.get("https://www.windy.com")


def weather_mode():
    wait = WebDriverWait(driver, 20)
    radar_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-ident="radar"]')))
    radar_button.click()
    print('radar button clicked')

def searchbar_search():
    search_box = driver.find_element(By.ID, 'q')
    search_box.send_keys(city)
    search_box.send_keys(Keys.ENTER)
    print('search box clicked')




#driver.quit()

if __name__ == '__main__':
    weather_mode()
    searchbar_search()


