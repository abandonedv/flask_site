import requests
from main import write_json
import re


def parse_text(text):
    pattern = r'/\w+'
    crypto = re.search(pattern, text).group()
    return crypto


def get_price(text):
    url = "https://yobit.net/api/2/btc_usd/ticker"
    r = requests.get(url).json()
    price = r["ticker"]["last"]
    # price = r[-1]["price_usd"]
    # # write_json(r.json(), filename="price.json")
    return price


def main():
    print(get_price(parse_text("сколько стоит ")))


if __name__ == "__main__":
    main()
