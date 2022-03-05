import json
import pprint

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


def price_of_bit():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'slug': 'bitcoin',
        'convert': 'RUB'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '881ca7de-a5a6-4971-885a-3d800be10159',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        with open("updates.json", "w") as file:
            json.dump(response.json(), file, indent=2, ensure_ascii=False)
        data = json.loads(response.text)
        return data["data"]["1"]["quote"]["RUB"]["price"]
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        pprint.pprint(e)
