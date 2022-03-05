import json
import re

import requests
from flask import Flask, \
    request, \
    jsonify
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

URL = "https://api.telegram.org/bot5252585561:AAEfa2EszuSRIz83kYYZcoWP1mYs8Af4rGo/"


def write_json(data, filename="answer.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_updates():
    url = URL + 'getUpdates'
    r = requests.get(url)
    write_json(r.json())
    return r.json()


def send_message(chat_id, text="Wait a second"):
    url = URL + "sendMessage"
    answer = {"chat_id": chat_id, "text": text}
    r = requests.post(url, json=answer)
    return r.json()


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "GET":
        print("...")

    if request.method == "POST":
        r = request.get_json()
        chat_id = r["message"]["chat"]["id"]
        message = r["message"]["text"]

        pattern = r'/\w+'

        if re.search(pattern, message):
            price = price_of_bit(parse_text(message))
            send_message(chat_id, text=price)

        return jsonify(r)
    return "<hi>Test flask</hi>"


def parse_text(text):
    pattern = r'/\w+'
    crypto = re.search(pattern, text).group()
    return crypto[1:]


def price_of_bit(text):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'slug': 'bitcoin',
        'convert': f'{text}'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '881ca7de-a5a6-4971-885a-3d800be10159',
    }

    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    with open("updates.json", "w") as file:
        json.dump(response.json(), file, indent=2, ensure_ascii=False)
    data = json.loads(response.text)
    price = data["data"]["1"]["quote"][f'{text}']["price"]
    return price


if __name__ == "__main__":
    app.run()
