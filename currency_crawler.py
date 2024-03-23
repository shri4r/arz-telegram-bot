import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lxml import etree

from db_functions import add_row, create_table


url = "http://www.tgju.org/"

ua = UserAgent()
header = {"user-agent": ua.chrome}

parser = etree.HTMLParser()  # Create an HTML parser object

main_page = requests.get(url, headers=header)
soup = BeautifulSoup(main_page.content, "lxml", parser=parser)

dollar_price_str = soup.find("tr", attrs={"data-market-row": "price_dollar_rl"}).td.string
pound_price_str = soup.find("tr", attrs={"data-market-row": "price_gbp"}).td.string
euro_price_str = soup.find("tr", attrs={"data-market-row": "price_eur"}).td.string


def fix_string(price_str_with_commas: str) -> str:
    """
    Removes commas from a string and trims non-digit characters from the end.

    Parameters:
    - price_str_with_commas (str): A string containing a price with commas.

    Returns:
    - str: The fixed string with commas removed and non-digit characters trimmed from the end.
    """
    fixed_string = price_str_with_commas.replace(",", "")

    while fixed_string and not fixed_string[-1].isdigit():
        fixed_string = fixed_string[:-1]

    if fixed_string:
        fixed_string = fixed_string[:-1]

    return fixed_string


if __name__ == "__main__":
    dollar = fix_string(dollar_price_str)
    pound = fix_string(pound_price_str)
    euro = fix_string(euro_price_str)

    create_table()
    add_row(dollar, pound, euro)
