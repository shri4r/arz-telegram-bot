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


def find_dollar_price():
    """
    This function scrapes the current price of the dollar from the 'tgju.org' website.

    It finds the 'tr' element with the attribute 'data-market-row' set to 'price_dollar_rl',
    then it finds the 'td' element inside this 'tr' element and extracts the string inside it.

    If the 'tr' or 'td' elements are not found, or if the 'td' element does not contain a string,
    it prints an error message and returns 'N/A'.

    Returns:
        str: The current price of the dollar as a string, or 'N/A' if the price could not be found.
    """
    # Find the dollar tr element
    dollar_tr_element = soup.find("tr", attrs={"data-market-row": "price_dollar_rl"})

    if dollar_tr_element is not None:
        # Find the td element inside the tr element
        td_element = dollar_tr_element.td

        # Check if the td element and its string property were found
        if td_element is not None and td_element.string is not None:
            # Get the string inside the td element
            dollar_price: str = td_element.string.strip()
        else:
            dollar_price: str = "N/A"
            print("The td element was not found or it does not contain a string")
    else:
        dollar_price: str = "N/A"
        print("The dollar tr element was not found")

    return dollar_price


# This function has the same logic as the find_dollar_price function
def find_pound_price():
    pound_tr_element = soup.find("tr", attrs={"data-market-row": "price_gbp"})

    if pound_tr_element is not None:
        td_element = pound_tr_element.td
        if td_element is not None and td_element.string is not None:
            pound_price: str = td_element.string.strip()
        else:
            pound_price: str = "N/A"
            print("The td element was not found or it does not contain a string")
    else:
        pound_price: str = "N/A"
        print("The pound tr element was not found")

    return pound_price


# This function has the same logic as the find_dollar_price function
def find_euro_price():
    euro_tr_element = soup.find("tr", attrs={"data-market-row": "price_eur"})

    if euro_tr_element is not None:
        td_element = euro_tr_element.td
        if td_element is not None and td_element.string is not None:
            euro_price: str = td_element.string.strip()
        else:
            euro_price: str = "N/A"
            print("The td element was not found or it does not contain a string")
    else:
        euro_price: str = "N/A"
        print("The euro tr element was not found")

    return euro_price


def fix_string(price_with_commas: str) -> str:
    """
    Removes commas from a string and trims non-digit characters from the end.

    Parameters:
    - price_str_with_commas (str): A string containing a price with commas.

    Returns:
    - str: The fixed string with commas removed and non-digit characters trimmed from the end.
    """
    fixed_string = price_with_commas.replace(",", "")

    while fixed_string and not fixed_string[-1].isdigit():
        fixed_string = fixed_string[:-1]

    if fixed_string:
        fixed_string = fixed_string[:-1]

    return fixed_string


def main():
    dollar_price = find_dollar_price()
    pound_price = find_pound_price()
    euro_price = find_euro_price()

    dollar = fix_string(dollar_price)
    pound = fix_string(pound_price)
    euro = fix_string(euro_price)

    create_table()
    add_row(dollar, pound, euro)


if __name__ == "__main__":
    main()
