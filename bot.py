import requests

URL = "https://api.telegram.org/bot5252585561:AAEfa2EszuSRIz83kYYZcoWP1mYs8Af4rGo/"
"https://api.telegram.org/bot5252585561:AAEfa2EszuSRIz83kYYZcoWP1mYs8Af4rGo/sendMessage?chat_id=427305163&text=trgtr"


def send_message(text="ERROR"):
    try:
        url = URL + "sendMessage"
        answer = {"chat_id": 427305163, "text": text}
        requests.post(url, json=answer)
    except Exception as e:
        print(e)
