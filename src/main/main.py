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

from src.templates.email_template import build_email_html
from src.services.email_service import EmailService

# Load config
config_path = Path(__file__).parent.parent / 'configs' / 'config.json'
with open(config_path, 'r', encoding='utf-8') as f:
    config_data = json.load(f)


def collect_all_data():
    """Collect data from all sources"""
    print("Collecting data...")

    data = {}

    # World News
    print("  - World news...")
    world_feed = RssWorldFeed(config_data)
    data['web_scrapper'] = world_feed.get_news()

    # Tech News
    print("  - Tech news...")
    tech_feed = RssTechFeed(config_data)
    data['tech_news'] = tech_feed.get_news()

    # Sports
    print("  - Sports...")
    sports_feed = RssSportsFeed(config_data)
    data['sports_news'] = sports_feed.get_news()

    # Science
    print("  - Science...")
    science_feed = RssScienceFeed(config_data)
    data['science_news'] = science_feed.get_news()

    # Entertainment
    print("  - Entertainment...")
    ent_feed = RssEntertainmentFeed(config_data)
    data['entertainment_news'] = ent_feed.get_news()

    # Finance
    print("  - Finance...")
    money = MoneyInfo(config_data)
    money_data = money.get_money()

    data['crypto_data'] = money_data.get('crypto')
    data['exchange_rates'] = money_data.get('exchange_rates')

    finance_feed = RssFinanceFeed(config_data)
    data['finance_news'] = finance_feed.get_news()

    # Weather (add your weather scraper)
    # data['weather_data'] = {'temp': 25, 'condition': 'Clear', 'city': 'London', 'humidity': 60}

    print("✓ Data collected!\n")
    return data


def main():
    """Main function - collect data and send email"""

    # Collect all data
    data = collect_all_data()

    # Build HTML email
    print("Building email...")
    html_content = build_email_html(**data)

    # Send email
    print("Sending email...")
    email_service = EmailService()

    from datetime import datetime
    subject = f"Daily Digest - {datetime.now().strftime('%B %d, %Y')}"

    success = email_service.send_email(subject, html_content)

    if success:
        print("✓ Email sent successfully!")
    else:
        print("✗ Failed to send email")


if __name__ == '__main__':
    main()