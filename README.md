# Arz Telegram Bot

This Telegram bot shows US Dollar, British Pound, and Euro prices in **Iranian tomans**. It fetches prices from TGJU in rials, converts them numerically (1 toman = 10 rials), and stores complete snapshots in SQLite. Whole-toman prices are rounded down when the source contains a fractional toman.

## Features

- Fetches currency prices (USD, GBP, EUR) from a website
- Stores the prices in a SQLite3 database
- Refreshes prices at startup and every 5 minutes while the bot is running
- Displays each price in tomans, its last successful fetch time (UTC), and the source
- Warns when the last successful update is 15 minutes old or older
- Keeps the previous successful snapshot if a request fails or any currency is missing or malformed
- Handles an empty/missing database with a friendly unavailable message
- Supports the following commands:
 - `/start` - Displays a welcome message and available commands
 - `/dollar` - Shows the price of US Dollar
 - `/pound` - Shows the price of British Pound
 - `/euro` - Shows the price of Euro

## Prerequisites

- Python >= 3.9
- Required Python packages: `requests`, `beautifulsoup4`, `fake_useragent`, `lxml`, `python-telegram-bot`

## Installation

1. Clone the repository
2. Activate your virtualenv
3. Install the required packages: `pip install -r requirements.txt`. The `python-telegram-bot[job-queue]` extra provides the scheduler.
4. Replace the placeholder in `config.py` with your Telegram bot token. Keep your real token private and do not commit it.
5. Start the bot: `python telegram_bot.py`.

The bot creates `currencies.db` beside the source files and attempts a refresh before polling starts. No separate crawler process or cron job is needed. The process must stay running for scheduled updates; restart it after a server reboot using your usual process manager.

For a one-off refresh, run `python currency_crawler.py`. Existing databases remain compatible: stored prices were already converted to tomans by the original crawler, so do not divide them again. Invalid legacy rows are ignored when reading prices.

Refresh and stale intervals are defined by `REFRESH_INTERVAL_SECONDS` and `STALE_AFTER_SECONDS` in `telegram_bot.py`. Requests use HTTPS with a 5-second connection timeout and a 15-second read timeout, check HTTP status codes, and log failures. The displayed timestamp records a successful fetch, not the market's own publication time; fetching an unchanged source price does not prove the market has updated.

Run the offline regression suite with `python -m unittest discover -s tests -v`. Tests use temporary databases and mocked HTTP/Telegram calls; a real token is not required.

## Best Practice

To ensure responsible and ethical web scraping, it is recommended to follow these best practices:

1. Ask for permission: Before scraping any website, it is important to check if the website allows web scraping. Some websites may have specific terms and conditions or may require you to obtain permission before scraping their data. It is always a good practice to respect the website's policies and seek permission if necessary.

2. Limit the frequency: To prevent overloading the website's server and to avoid IP blocking, it is advisable to limit the frequency of scraping requests. Running the `currency_crawler.py` file every few minutes or at a reasonable interval helps distribute the load and reduces the chances of being blocked by the website.

By following these best practices, you can ensure that your web scraping activities are respectful, responsible, and compliant with the website's terms and conditions.

## Disclaimer

Please note that the crawling of the tgju website to fetch currency prices is subject to the terms and conditions of the website. By running `currency_crawler.py` file, you agree that the responsibility of crawling the tgju website and complying with its terms and conditions lies solely with you. I, as the developer of this bot, am not responsible for any misuse or violation of the website's terms and conditions.
