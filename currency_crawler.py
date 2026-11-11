"""Fetch complete TGJU currency snapshots in tomans."""
import logging
import re
import sqlite3

import requests
from bs4 import BeautifulSoup

from db_functions import add_row, create_table

URL = "https://www.tgju.org/"
REQUEST_TIMEOUT = (5, 15)
MARKETS = ("price_dollar_rl", "price_gbp", "price_eur")
logger = logging.getLogger(__name__)


def fix_string(price_with_commas: str) -> int:
    """Parse positive whole rials and convert to whole tomans (round down)."""
    normalized = price_with_commas.strip().replace(",", "").replace("٬", "")
    if not re.fullmatch(r"\d+", normalized):
        raise ValueError("Currency price must contain only digits and separators")
    tomans = int(normalized) // 10
    if tomans <= 0:
        raise ValueError("Currency price must be positive")
    return tomans


def parse_prices(html: str) -> tuple:
    """Reject the entire snapshot if any currency is missing or malformed."""
    soup = BeautifulSoup(html, "lxml")
    prices = []
    for market in MARKETS:
        cell = soup.select_one(f'tr[data-market-row="{market}"] td')
        if cell is None:
            raise ValueError(f"Missing price cell for {market}")
        prices.append(fix_string(cell.get_text(strip=True)))
    return tuple(prices)


def fetch_prices() -> tuple:
    """Fetch with bounded waits; propagate network and HTTP errors."""
    with requests.get(
        URL, headers={"User-Agent": "ArzTelegramBot/1.0"}, timeout=REQUEST_TIMEOUT
    ) as response:
        response.raise_for_status()
        return parse_prices(response.text)


def refresh_prices() -> None:
    # Validate everything before touching the last successful snapshot.
    prices = fetch_prices()
    create_table()
    add_row(*prices)
    logger.info("Saved a new currency snapshot in tomans")


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    try:
        refresh_prices()
    except (requests.RequestException, ValueError, sqlite3.Error) as exc:
        logger.error("Refresh failed; previous prices retained: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
