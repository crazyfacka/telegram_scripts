import json
import os
import requests

def send_telegram_message(bot_token, chat_id, subject, msg):
    base_url = f"https://api.telegram.org/bot{bot_token}/"
    send_message_url = f"{base_url}sendMessage"

    text = f"""
{subject}

{msg}
"""

    payload = {
        'chat_id': chat_id,
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

bot_token = telegram_info['bot_token']
chat_id = telegram_info['chat_id']