import humanize
import json
import os
import requests
import subprocess
import sys

def send_telegram_message(bot_token, chat_id, bk_file, err_file, bk_time):
    base_url = f"https://api.telegram.org/bot{bot_token}/"
    send_message_url = f"{base_url}sendMessage"

    errors = ""
    with open(err_file) as f:
        for line in f:
            errors = errors + line

    f_info = get_file_info(bk_file)

    text = f"""
🟢📼 Backup complete!

It took {humanize.precisedelta(bk_time)}

{f_info[0]}
{f_info[1]}

Log:
{errors}
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

def get_file_info(filename):
    try:
        # Run the 'file' command and capture its output
        result = subprocess.check_output(['file', filename], stderr=subprocess.STDOUT, universal_newlines=True)

        # Get file size in human-readable format
        size_bytes = os.path.getsize(filename)
        size_human = humanize.naturalsize(size_bytes)

        return [result.strip(), size_human]  # Remove leading/trailing whitespace and newline
    except subprocess.CalledProcessError as e:
        return [f"Error: {e.output.strip()}", ""]

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: python {sys.argv[0]} backup_file error_file execution_time")
        sys.exit(1)

    bk_file = sys.argv[1]
    err_file = sys.argv[2]
    bk_time = sys.argv[3]

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(f'{__location__}/telegram_info.json') as f:
        telegram_info = json.load(f)

    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    bot_token = telegram_info['bot_token']

    # Replace 'CHAT_ID' with the chat ID where you want to send the message
    chat_id = telegram_info['chat_id']

    success, response = send_telegram_message(bot_token, chat_id, bk_file, err_file, bk_time)

    if success:
        print("Message sent successfully:", response)
    else:
        print("Failed to send message:", response)

