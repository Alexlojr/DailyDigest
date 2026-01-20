from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
import json
import time

# ===== PATHS =====
screenshot_dir = Path(__file__).parent.parent / 'imgs'
screenshot_dir.mkdir(parents=True, exist_ok=True)
file_path = screenshot_dir / "morning_weather.png"

print(f"Screenshot will be saved to: {file_path.absolute()}")

# Load config
config_path = Path(__file__).parent.parent / 'configs' / 'config.json'

try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
except FileNotFoundError:
    print(f'config.json not found at {config_path}')
    config_data = {}

city = config_data['weather']['city']



# ===== CHROME OPTIONS =====
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Force english
chrome_options.add_argument('--lang=en-US')
chrome_options.add_experimental_option('prefs', {
    'intl.accept_languages': 'en-US,en',
    'profile.default_content_setting_values.geolocation': 2
})

# Anti-bot
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=chrome_options)



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
    """Search with click by coordinates"""
    try:
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(
            EC.element_to_be_clickable((By.ID, 'search-q'))
        )

        search_box.click()
        search_box.clear()
        time.sleep(0.5)

        # Type city
        for char in city:
            search_box.send_keys(char)
            time.sleep(0.15)

        print(f'Typed: {city}')
        time.sleep(2)


        try:

            location = search_box.location
            size = search_box.size


            x_offset = size['width'] // 2
            y_offset = size['height'] + 10

            # Move mouse e clica
            actions = ActionChains(driver)
            actions.move_to_element(search_box).perform()
            time.sleep(0.3)
            actions.move_by_offset(0, y_offset).click().perform()

            print('Clicked dropdown by coordinates')
            time.sleep(3)
            return True

        except Exception as e:
            print(f"Coordinate click failed: {e}")
            return False

    except Exception as e:
        print(f"Search failed: {e}")
        return False


def take_screenshot():
    """Take and save screenshot"""
    try:
        print(f"Taking screenshot...")
        driver.save_screenshot(str(file_path))

        print(f"Screenshot saved to: {file_path.absolute()}")

        if file_path.exists():
            size = file_path.stat().st_size / 1024
            print(f"File size: {size:.1f} KB")
            return True
        else:
            print("Screenshot file not found!")
            return False

    except Exception as e:
        print(f"Screenshot failed: {e}")
        return False


if __name__ == '__main__':
    try:
        # 1. Open site
        driver.get("https://www.ventusky.com")
        driver.fullscreen_window()
        print("Site opened")
        time.sleep(3)

        # 2. Switch to rain radar
        weather_mode()

        # 3. Search city (SOLUÇÃO 2)
        if searchbar_search():
            print("Search successful")
        else:
            print("Search failed")

        # 4. Wait for map to fully load

        # 5. Take screenshot
        if take_screenshot():
            print("\nALL DONE!")
        else:
            print("\nScreenshot failed")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()

    finally:
        print("\nBrowser will stay open. Close manually or uncomment driver.quit()")
        driver.quit()