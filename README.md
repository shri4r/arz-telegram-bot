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

- Python 3.x
- Required Python packages: `requests`, `beautifulsoup4`, `fake_useragent`, `lxml`, `python-telegram-bot`

## Installation

1. Clone the repository
2. Activate your virtualenv
3. Install the required packages -> ```pip install -r requirements.txt```