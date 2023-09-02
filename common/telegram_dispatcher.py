import json
import os
import requests

BOT_TOKEN = ""
CHAT_ID = ""

def send_telegram_message(subject, msg):
    base_url = f"https://api.telegram.org/bot{BOT_TOKEN}/"
    send_message_url = f"{base_url}sendMessage"

    text = f"""
{subject}

{msg}
"""

    payload = {
        'chat_id': CHAT_ID,
        'text': text,
    }

    response = requests.post(send_message_url, data=payload)
    result = response.json()

    if result['ok']:
        return True, result['result']
    else:
        return False, result['description']




__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(f'{__location__}/telegram_info.json') as f:
    telegram_info = json.load(f)

BOT_TOKEN = telegram_info['bot_token']
CHAT_ID = telegram_info['chat_id']