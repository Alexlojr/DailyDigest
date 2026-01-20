from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import os
import json
import time



screenshot_dir = Path("..DailyDigest/src/imgs/")
screenshot_dir.mkdir(parents=True, exist_ok=True)
file_path = screenshot_dir / "morning_weather.png"


# Load config
config_path = Path(__file__).parent.parent / 'configs' / 'config.json'

try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
except FileNotFoundError:
    print(f'config.json not found at {config_path}')
    config_data = {}

city = config_data['weather']['city']
# ====---==== #


# ===== CONFIGURE CHROME OPTIONS =====
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
# ====---==== #

# Force english
chrome_options.add_argument('--lang=en-US')
chrome_options.add_experimental_option('prefs', {
    'intl.accept_languages': 'en-US,en',
    'profile.default_content_setting_values.geolocation': 2  # Block geolocation
})
# ====---==== #


# ==== Anti-bot ==== #
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=chrome_options)
# ====---==== #

driver.save_screenshot(str(file_path))


def weather_mode():
    """Switch to radar mode"""
    wait = WebDriverWait(driver, 20)
    radar_button = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'rain'))
    )
    radar_button.click()
    print('Radar button clicked')
    time.sleep(3)


def searchbar_search():
    """Search for city - Click dropdown result"""
    try:
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(
            EC.element_to_be_clickable((By.ID, 'search-q'))
        )

        search_box.click()
        time.sleep(1)

        # Clear field
        search_box.clear()
        time.sleep(0.5)

        # Type city
        for char in city:
            search_box.send_keys(char)
            time.sleep(0.1)

        print(f'Typed: {city}')
        time.sleep(2)  # Espera dropdown aparecer

        # CLICAR NO PRIMEIRO RESULTADO DO DROPDOWN
        try:
            # Tenta vários seletores possíveis
            selectors = [
                '.search-results li:first-child',
                '.autocomplete-item:first-child',
                '[class*="result"]:first-child',
                'ul li:first-child',
            ]

            first_result = None
            for selector in selectors:
                try:
                    first_result = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if first_result:
                first_result.click()
                print('Clicked dropdown result')
            else:
                # Fallback: Enter
                search_box.send_keys(Keys.ENTER)
                print('Enter pressed (no dropdown found)')

        except Exception as e:
            print(f"Dropdown error: {e}, trying Enter")
            search_box.send_keys(Keys.ENTER)

        time.sleep(3)
        return True

    except Exception as e:
        print(f"Search failed: {e}")
        return False


if __name__ == '__main__':
    driver.get("https://www.ventusky.com")

    driver.fullscreen_window()
    print("Site opened")

    weather_mode()
    searchbar_search()
    driver.save_screenshot("viewport_screenshot.png")

    # driver.quit()