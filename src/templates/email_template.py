from datetime import datetime


def build_email_html(
        web_scrapper=None,
        tech_news=None,
        sports_news=None,
        science_news=None,
        entertainment_news=None,
        finance_news=None,
        crypto_data=None,
        exchange_rates=None,
        has_weather_screenshot=False
):
    """
    Build comprehensive HTML email from all data sources

    Args:
        web_scrapper: List of (source, title, link) - World news
        tech_news: List of (source, title, link) - Tech news
        sports_news: List of (source, title, link) - Sports news
        science_news: List of (source, title, link) - Science news
        entertainment_news: List of (source, title, link) - Entertainment news
        finance_news: List of (source, title, link) - Finance news
        crypto_data: Dict of crypto prices
        exchange_rates: Dict of exchange rates
        has_weather_screenshot: Bool - whether weather screenshot exists
    """

    # Default empty lists/dicts if None
    web_scrapper = web_scrapper or []
    tech_news = tech_news or []
    sports_news = sports_news or []
    science_news = science_news or []
    entertainment_news = entertainment_news or []
    finance_news = finance_news or []
    crypto_data = crypto_data or {}
    exchange_rates = exchange_rates or {}

    # Get current date
    current_date = datetime.now().strftime('%B %d, %Y')

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background-color: #f4f6f8;
                padding: 20px;
                line-height: 1.6;
            }}

            .container {{
                max-width: 800px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                overflow: hidden;
                border: 1px solid #e1e4e8;
            }}

            .header {{
                background-color: #2c3e50;
                color: white;
                padding: 30px 30px;
                text-align: center;
                border-bottom: 4px solid #3498db;
            }}

            .header h1 {{
                font-size: 28px;
                margin-bottom: 5px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }}

            .header .date {{
                font-size: 14px;
                opacity: 0.8;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}

            .content {{
                padding: 30px;
            }}

            .section {{
                margin-bottom: 40px;
            }}

            .section-title {{
                font-size: 20px;
                color: #2c3e50;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #3498db;
                display: flex;
                align-items: center;
                gap: 10px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}

            /* Weather styles */
            .weather-screenshot {{
                margin-top: 15px;
                text-align: center;
            }}

            .weather-screenshot img {{
                width: 100%;
                max-width: 750px;
                border-radius: 4px;
                border: 1px solid #ddd;
                display: block;
                margin: 0 auto;
            }}

            /* Finance styles */
            .finance-grid {{
                display: grid;
                gap: 15px;
                margin-top: 15px;
            }}

            .crypto-item {{
                background-color: #f8f9fa;
                padding: 12px 15px;
                border-radius: 4px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border: 1px solid #e9ecef;
            }}

            .crypto-name {{
                font-weight: 600;
                color: #2c3e50;
                font-size: 15px;
            }}

            .crypto-price {{
                font-size: 16px;
                font-weight: 700;
                color: #2c3e50;
            }}

            .crypto-change {{
                font-size: 13px;
                margin-left: 10px;
                font-weight: 500;
            }}

            .crypto-change.positive {{
                color: #27ae60;
            }}

            .crypto-change.negative {{
                color: #c0392b;
            }}

            .exchange-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                gap: 10px;
                margin-top: 15px;
            }}

            .exchange-item {{
                background-color: #fff;
                padding: 10px;
                border-radius: 4px;
                text-align: center;
                border: 1px solid #dfe6e9;
            }}

            .exchange-pair {{
                font-size: 11px;
                color: #7f8c8d;
                text-transform: uppercase;
                margin-bottom: 2px;
            }}

            .exchange-rate {{
                font-size: 16px;
                font-weight: 600;
                color: #2c3e50;
            }}

            /* News styles */
            .news-list {{
                list-style: none;
            }}

            .news-item {{
                margin-bottom: 12px;
                padding: 12px;
                background-color: #fff;
                border: 1px solid #e1e4e8;
                border-radius: 4px;
                transition: background-color 0.2s;
            }}

            .news-item:hover {{
                background-color: #f1f2f6;
            }}

            .news-source {{
                display: inline-block;
                background-color: #34495e;
                color: white;
                padding: 2px 8px;
                border-radius: 2px;
                font-size: 11px;
                font-weight: bold;
                margin-bottom: 5px;
                text-transform: uppercase;
            }}

            .news-title {{
                color: #2980b9;
                text-decoration: none;
                font-size: 15px;
                font-weight: 500;
                display: block;
                line-height: 1.4;
            }}

            .news-title:hover {{
                text-decoration: underline;
                color: #1a5276;
            }}

            /* Footer */
            .footer {{
                background-color: #f8f9fa;
                padding: 20px;
                text-align: center;
                border-top: 1px solid #e9ecef;
            }}

            .footer p {{
                color: #7f8c8d;
                font-size: 12px;
            }}

            /* Empty state */
            .empty-state {{
                text-align: center;
                padding: 20px;
                color: #95a5a6;
                font-style: italic;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Header -->
            <div class="header">
                <h1>Daily Digest</h1>
                <p class="date">{current_date}</p>
            </div>

            <div class="content">
                <!-- Weather Screenshot Section -->
                {_build_weather_section(has_weather_screenshot)}

                <!-- Finance Section -->
                {_build_finance_section(crypto_data, exchange_rates, finance_news)}

                <!-- World News Section -->
                {_build_news_section("World News", web_scrapper)}

                <!-- Tech News Section -->
                {_build_news_section("Technology", tech_news)}

                <!-- Sports Section -->
                {_build_news_section("Sports", sports_news)}

                <!-- Science Section -->
                {_build_news_section("Science", science_news)}

                <!-- Entertainment Section -->
                {_build_news_section("Entertainment", entertainment_news)}
            </div>

            <!-- Footer -->
            <div class="footer">
                <p>Generated by Daily Digest Automation</p>
            </div>
        </div>
    </body>
    </html>
    """

    return html


def _build_weather_section(has_screenshot):
    """Build weather section HTML - only shows screenshot if available"""
    if not has_screenshot:
        return ""

    return """
    <div class="section">
        <h2 class="section-title">Weather Radar</h2>
        <div style="margin-top: 15px;">
            <img src="cid:weather_map" alt="Weather Radar Map" 
                 style="width: 100%; max-width: 750px; border-radius: 4px; 
                        border: 1px solid #ddd; display: block; margin: 0 auto;">
        </div>
    </div>
    """


def _build_finance_section(crypto_data, exchange_rates, finance_news):
    """Build finance section HTML"""
    if not crypto_data and not exchange_rates and not finance_news:
        return ""

    html = '<div class="section"><h2 class="section-title">Finance</h2>'

    # Crypto prices
    if crypto_data:
        html += '<h3 style="margin: 15px 0 10px 0; color: #2c3e50; font-size: 16px;">Cryptocurrency</h3>'
        html += '<div class="finance-grid">'

        for crypto_name, info in crypto_data.items():
            price = info.get('price', 0)
            change = info.get('change_24h', 0)
            change_class = 'positive' if change >= 0 else 'negative'
            arrow = '▲' if change >= 0 else '▼'

            html += f"""
            <div class="crypto-item">
                <div>
                    <div class="crypto-name">{crypto_name}</div>
                </div>
                <div style="text-align: right;">
                    <span class="crypto-price">${price:,.2f}</span>
                    <span class="crypto-change {change_class}">{arrow} {abs(change):.2f}%</span>
                </div>
            </div>
            """

        html += '</div>'

    # Exchange rates
    if exchange_rates:
        html += '<h3 style="margin: 15px 0 10px 0; color: #2c3e50; font-size: 16px;">Exchange Rates</h3>'
        html += '<div class="exchange-grid">'

        for pair, rate in exchange_rates.items():
            html += f"""
            <div class="exchange-item">
                <div class="exchange-pair">{pair}</div>
                <div class="exchange-rate">{rate}</div>
            </div>
            """

        html += '</div>'

    # Finance news
    if finance_news:
        html += '<h3 style="margin: 15px 0 10px 0; color: #2c3e50; font-size: 16px;">Financial News</h3>'
        html += '<ul class="news-list">'

        for source, title, link in finance_news[:5]:
            html += f"""
            <li class="news-item">
                <span class="news-source">{source}</span>
                <a href="{link}" class="news-title" target="_blank">{title}</a>
            </li>
            """

        html += '</ul>'

    html += '</div>'
    return html


def _build_news_section(section_title, news_list):
    """Build a news section HTML"""
    if not news_list:
        return ""

    html = f'<div class="section"><h2 class="section-title">{section_title}</h2>'

    if len(news_list) == 0:
        html += '<div class="empty-state">No news available</div>'
    else:
        html += '<ul class="news-list">'

        for source, title, link in news_list[:10]:  # Limit to 10 items per section
            html += f"""
            <li class="news-item">
                <span class="news-source">{source}</span>
                <a href="{link}" class="news-title" target="_blank">{title}</a>
            </li>
            """

        html += '</ul>'

    html += '</div>'
    return html


# Test function
if __name__ == "__main__":
    # Test data
    test_data = {
        'crypto_data': {
            'Bitcoin': {'price': 45230.50, 'change_24h': 2.5},
            'Ethereum': {'price': 2350.75, 'change_24h': -1.2}
        },
        'exchange_rates': {
            'USD → EUR': 0.92,
            'USD → GBP': 0.79,
            'USD → JPY': 148.50
        },
        'web_scrapper': [
            ('CNN', 'Breaking: Major development in tech sector', 'https://cnn.com/article1'),
            ('BBC', 'Global summit addresses climate change', 'https://bbc.com/article2')
        ],
        'tech_news': [
            ('TechCrunch', 'AI breakthrough announced by researchers', 'https://techcrunch.com/article1'),
        ],
        'finance_news': [
            ('Bloomberg', 'Markets reach new highs', 'https://bloomberg.com/article1'),
        ],
        'has_weather_screenshot': True  # Set to True to test weather section
    }

    html_output = build_email_html(**test_data)

    # Save to file for testing
    with open('test_email.html', 'w', encoding='utf-8') as f:
        f.write(html_output)

    print("Test email HTML generated successfully!")
    print("Open 'test_email.html' in your browser to preview")
