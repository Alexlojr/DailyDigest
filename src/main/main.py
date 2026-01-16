import os
import smtplib
from email.message import EmailMessage
import json
from pathlib import Path
from src.scrapers.finance_crypto import RssFinanceFeed

config_path = Path(__file__).parent.parent / 'configs' / 'config.json'

try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
except FileNotFoundError:
    print(f'config.json not found at {config_path}')
    config_data = {}



test = RssFinanceFeed(config_data)
teste = test.get_news()

for source, title, link in teste[:6]:
    print(f"\n{source}: {title}")
    print(f"→ {link}")

