import humanize
import json
import psutil
import requests
import sys

def send_telegram_message(bot_token, chat_id, mem, swap):
    base_url = f"https://api.telegram.org/bot{bot_token}/"
    send_message_url = f"{base_url}sendMessage"

    text = f"""
🟡🖥️ High memory or swap usage!

Memory: {mem}%
Swap: {swap}%

Top 5 memory-consuming processes:
{get_top_memory_processes()}
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

def get_top_memory_processes(num_processes=5):
    process_list = []

    for process in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            process_info = process.info
            process_list.append((process_info['pid'], process_info['name'], process_info['memory_info'].rss))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    top_processes = sorted(process_list, key=lambda x: x[2], reverse=True)[:num_processes]

    processes_text = ""
    for idx, (pid, name, memory_usage) in enumerate(top_processes, start=1):
        memory_usage_human = humanize.naturalsize(memory_usage)
        processes_text = processes_text + f"{idx}. PID: {pid}, Name: {name}, Memory Usage: {memory_usage_human}\n"

    return processes_text

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} mem swap")
        sys.exit(1)

    mem = sys.argv[1]
    swap = sys.argv[2]

    with open('telegram_info.json') as f:
        telegram_info = json.load(f)

    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    bot_token = telegram_info['bot_token']

    # Replace 'CHAT_ID' with the chat ID where you want to send the message
    chat_id = telegram_info['chat_id']

    success, response = send_telegram_message(bot_token, chat_id, mem, swap)

    if success:
        print("Message sent successfully:", response)
    else:
        print("Failed to send message:", response)

