import requests
from asyncio import sleep

URL = "https://api.telegram.org/bot5160776370:AAH50HwNs07N_6SvuTxK82gDSpV2OD03Iuw/"
"https://api.telegram.org/bot5252585561:AAEfa2EszuSRIz83kYYZcoWP1mYs8Af4rGo/sendMessage?chat_id=427305163&text=trgtr"


async def send_message(text="ERROR"):
    try:
        url = URL + "sendMessage"
        answer = {"chat_id": 427305163, "text": text}
        requests.post(url, json=answer)
    except Exception as e:
        print(e)


async def send_message1(text="ERROR"):
    while True:
        try:
            url = URL + "sendMessage"
            answer = {"chat_id": 427305163, "text": text}
            requests.post(url, json=answer)
            await sleep(3)
        except Exception as e:
            print(e)
