import json
import os
import requests
import sys

def send_telegram_message(bot_token, chat_id, subject, msg):
    base_url = f"https://api.telegram.org/bot{bot_token}/"
    send_message_url = f"{base_url}sendMessage"

    text = f"""
📢 Informational message!

» {subject} «

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

if __name__ == "__main__":
    if not sys.stdin.isatty():
        pipe_data = sys.stdin.read().strip()

    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} subject")
        sys.exit(1)

    subject = sys.argv[1]

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(f'{__location__}/telegram_info.json') as f:
        telegram_info = json.load(f)

    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    bot_token = telegram_info['bot_token']

    # Replace 'CHAT_ID' with the chat ID where you want to send the message
    chat_id = telegram_info['chat_id']

    success, response = send_telegram_message(bot_token, chat_id, subject, pipe_data)

    if success:
        print("Message sent successfully:", response)
    else:
        print("Failed to send message:", response)

