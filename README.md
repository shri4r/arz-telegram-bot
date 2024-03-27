# Arz Telegram Bot

This is a Telegram bot that shows the current price of US Dollar, British Pound, and Euro currencies in Iranian Rial. The bot retrieves the currency prices from a website, stores them in a SQLite3 database, and displays the prices to users upon request.

## Features

- Fetches currency prices (USD, GBP, EUR) from a website
- Stores the prices in a SQLite3 database
- Displays the current price of each currency to users via a Telegram bot
- Supports the following commands:
 - `/start` - Displays a welcome message and available commands
 - `/dollar` - Shows the price of US Dollar
 - `/pound` - Shows the price of British Pound
 - `/euro` - Shows the price of Euro

## Prerequisites

- Python >= 3.8
- Required Python packages: `requests`, `beautifulsoup4`, `fake_useragent`, `lxml`, `python-telegram-bot`

## Installation

1. Clone the repository
2. Activate your virtualenv
3. Install the required packages -> ```pip install -r requirements.txt```

## Best Practice

To ensure responsible and ethical web scraping, it is recommended to follow these best practices:

1. Ask for permission: Before scraping any website, it is important to check if the website allows web scraping. Some websites may have specific terms and conditions or may require you to obtain permission before scraping their data. It is always a good practice to respect the website's policies and seek permission if necessary.

2. Limit the frequency: To prevent overloading the website's server and to avoid IP blocking, it is advisable to limit the frequency of scraping requests. Running the `currency_crawler.py` file every few minutes or at a reasonable interval helps distribute the load and reduces the chances of being blocked by the website.

By following these best practices, you can ensure that your web scraping activities are respectful, responsible, and compliant with the website's terms and conditions.

## Disclaimer

Please note that the crawling of the tgju website to fetch currency prices is subject to the terms and conditions of the website. By running `currency_crawler.py` file, you agree that the responsibility of crawling the tgju website and complying with its terms and conditions lies solely with you. I, as the developer of this bot, am not responsible for any misuse or violation of the website's terms and conditions.