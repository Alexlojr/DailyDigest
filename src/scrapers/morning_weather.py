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

# Load config
config_path = Path(__file__).parent.parent / 'configs' / 'config.json'

try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
except FileNotFoundError:
    print(f'config.json not found at {config_path}')
    config_data = {}

city = config_data.get('weather', {}).get('city', 'London')


def get_chrome_options(headless=True):
    """Get Chrome options with anti-detection"""
    chrome_options = webdriver.ChromeOptions()

    # Headless mode for automation (set to False to see browser)
    if headless:
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--window-size=1920,1080')
    else:
        chrome_options.add_experimental_option("detach", True)

    # Force english
    chrome_options.add_argument('--lang=en-US')
    chrome_options.add_experimental_option('prefs', {
        'intl.accept_languages': 'en-US,en',
        'profile.default_content_setting_values.geolocation': 2
    })

    # Anti-bot detection
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Performance optimizations
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    return chrome_options


def weather_mode(driver):
    """Switch to radar mode"""
    try:
        wait = WebDriverWait(driver, 20)
        radar_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'rain'))
        )
        radar_button.click()
        print('   ✓ Radar mode activated')
        time.sleep(3)
        return True
    except Exception as e:
        print(f'   ✗ Failed to activate radar mode: {e}')
        return False


def searchbar_search(driver, city):
    """Search for city"""
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

        print(f'   ✓ Typed: {city}')
        time.sleep(2)

        # Click first dropdown result using coordinates
        try:
            location = search_box.location
            size = search_box.size

            x_offset = size['width'] // 2
            y_offset = size['height'] + 10

            # Move and click
            actions = ActionChains(driver)
            actions.move_to_element(search_box).perform()
            time.sleep(0.3)
            actions.move_by_offset(0, y_offset).click().perform()

            print('   ✓ Selected city from dropdown')
            time.sleep(3)
            return True

        except Exception as e:
            print(f"   ⚠️  Coordinate click failed: {e}")
            return False

    except Exception as e:
        print(f"   ✗ Search failed: {e}")
        return False


def take_screenshot(driver):
    """Take and save screenshot"""
    try:
        driver.save_screenshot(str(file_path))

        if file_path.exists():
            size = file_path.stat().st_size / 1024
            print(f"   ✓ Screenshot saved: {file_path.name} ({size:.1f} KB)")
            return True
        else:
            print("   ✗ Screenshot file not created!")
            return False

    except Exception as e:
        print(f"   ✗ Screenshot failed: {e}")
        return False


def capture_weather_screenshot(headless=True):
    """
    Main function to capture weather screenshot

    Args:
        headless: Run browser in headless mode (True for automation)

    Returns:
        bool: True if successful, False otherwise
    """
    driver = None

    try:
        print("\n🌤️  WEATHER SCREENSHOT CAPTURE")
        print("-" * 50)

        # Initialize driver
        chrome_options = get_chrome_options(headless=headless)
        driver = webdriver.Chrome(options=chrome_options)

        # 1. Open site
        print("1. Opening Ventusky...")
        driver.get("https://www.ventusky.com")
        if not headless:
            driver.fullscreen_window()
        else:
            driver.set_window_size(1920, 1080)
        time.sleep(3)
        print("   ✓ Site loaded")

        # 2. Switch to rain radar
        print("2. Switching to radar mode...")
        if not weather_mode(driver):
            return False

        # 3. Search city
        print(f"3. Searching for {city}...")
        if not searchbar_search(driver, city):
            print("   ⚠️  Search failed, but continuing...")

        # 4. Wait for map to load
        print("4. Waiting for map to render...")
        time.sleep(5)

        # 5. Take screenshot
        print("5. Capturing screenshot...")
        success = take_screenshot(driver)

        print("-" * 50)
        if success:
            print("✅ WEATHER SCREENSHOT COMPLETE!\n")
        else:
            print("❌ SCREENSHOT FAILED!\n")

        return success

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        if driver:
            driver.quit()


# For backwards compatibility
def main():
    """Legacy main function - calls the new function"""
    return capture_weather_screenshot(headless=False)


if __name__ == '__main__':
    # Run with browser visible for testing
    # For production, use: capture_weather_screenshot(headless=True)
    capture_weather_screenshot(headless=False)