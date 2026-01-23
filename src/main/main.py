import os
from pathlib import Path
import json
from dotenv import load_dotenv

from src.scrapers.rss_feeds_worldnews import RssWorldFeed
from src.scrapers.tech_news import RssTechFeed
from src.scrapers.sports_news import RssSportsFeed
from src.scrapers.science_news import RssScienceFeed
from src.scrapers.entertainment_rss import RssEntertainmentFeed
from src.scrapers.finance_crypto import MoneyInfo, RssFinanceFeed
from src.scrapers.morning_weather import capture_weather_screenshot

from src.templates.email_template import build_email_html
from src.services.email_service import EmailService

# Load environment variables
load_dotenv()

# Load config
config_path = Path(__file__).parent.parent / 'configs' / 'config.json'
with open(config_path, 'r', encoding='utf-8') as f:
    config_data = json.load(f)


def collect_all_data():
    """Collect data from all sources"""
    print("\n" + "=" * 60)
    print("COLLECTING DATA...")
    print("=" * 60)

    data = {}

    # World News
    print("\nWorld news...")
    world_feed = RssWorldFeed(config_data)
    data['web_scrapper'] = world_feed.get_news()
    print(f"   Collected {len(data['web_scrapper'])} world news items")

    # Tech News
    print("\nTech news...")
    tech_feed = RssTechFeed(config_data)
    data['tech_news'] = tech_feed.get_news()
    print(f"   Collected {len(data['tech_news'])} tech news items")

    # Sports
    print("\nSports...")
    sports_feed = RssSportsFeed(config_data)
    data['sports_news'] = sports_feed.get_news()
    print(f"   Collected {len(data['sports_news'])} sports news items")

    # Science
    print("\nScience...")
    science_feed = RssScienceFeed(config_data)
    data['science_news'] = science_feed.get_news()
    print(f"   Collected {len(data['science_news'])} science news items")

    # Entertainment
    print("\nEntertainment...")
    ent_feed = RssEntertainmentFeed(config_data)
    data['entertainment_news'] = ent_feed.get_news()
    print(f"   Collected {len(data['entertainment_news'])} entertainment news items")

    # Finance
    print("\nFinance...")
    money = MoneyInfo(config_data)
    money_data = money.get_money()

    data['crypto_data'] = money_data.get('crypto')
    data['exchange_rates'] = money_data.get('exchange_rates')

    if data['crypto_data']:
        print(f"   Collected crypto data: {list(data['crypto_data'].keys())}")
    if data['exchange_rates']:
        print(f"   Collected {len(data['exchange_rates'])} exchange rates")

    finance_feed = RssFinanceFeed(config_data)
    data['finance_news'] = finance_feed.get_news()
    print(f"   Collected {len(data['finance_news'])} finance news items")

    # Weather Screenshot
    print("\nCapturing weather screenshot...")
    screenshot_path = Path(__file__).parent.parent / 'imgs' / 'morning_weather.png'

    try:
        # headless=True ensures it runs in background
        print("   Running browser automation...")
        success = capture_weather_screenshot(headless=True)
        
        if success and screenshot_path.exists():
            data['has_weather_screenshot'] = True
            print(f"   Weather screenshot captured successfully")
        else:
            print(f"   Failed to capture weather screenshot")
            data['has_weather_screenshot'] = False

    except Exception as e:
        print(f"   Weather screenshot check error: {e}")
        data['has_weather_screenshot'] = False

    print("\n" + "=" * 60)
    print("DATA COLLECTION COMPLETE!")
    print("=" * 60 + "\n")

    return data


def main():
    """Main function - collect data and send email"""

    print("\n" + "DAILY DIGEST AUTOMATION STARTED" + "\n")

    try:
        # Collect all data
        data = collect_all_data()

        # Build HTML email
        print("Building email HTML...")
        html_content = build_email_html(**data)
        print("   Email HTML built successfully\n")

        # Prepare images to embed
        images = {}
        screenshot_path = Path(__file__).parent.parent / 'imgs' / 'morning_weather.png'
        if screenshot_path.exists():
            images['weather_map'] = str(screenshot_path)
            print(f"   Weather screenshot will be embedded\n")

        # Send email
        print("Sending email...")
        email_service = EmailService()

        from datetime import datetime
        subject = f"Daily Digest - {datetime.now().strftime('%B %d, %Y')}"

        success = email_service.send_email(
            subject=subject,
            html_content=html_content,
            image_paths=images if images else None
        )

        print("\n" + "=" * 60)
        if success:
            print("EMAIL SENT SUCCESSFULLY!")
            print("=" * 60)
            print(f"Check your inbox: {os.getenv('RECIPIENT_EMAIL')}")
        else:
            print("FAILED TO SEND EMAIL")
            print("=" * 60)
            print("Check your .env file and email configuration")
        print("=" * 60 + "\n")

    except Exception as e:
        print("\n" + "=" * 60)
        print("ERROR OCCURRED")
        print("=" * 60)
        print(f"Error details: {str(e)}")
        print("=" * 60 + "\n")
        raise


if __name__ == '__main__':
    main()
