"""Compute a message when high memory or swap usage is detected"""
import sys
import humanize
import psutil

import common.telegram_dispatcher as td

def get_top_memory_processes(num_processes=5):
    """List top memory consuming processes"""
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

    subject = "🟡🖥️ High memory or swap usage!"
    text = f"""
Memory: {mem}%
Swap: {swap}%

Top 5 memory-consuming processes:
{get_top_memory_processes()}
"""

    success, response = td.send_telegram_message(subject, text)

    if success:
        print("Message sent successfully:", response)
    else:
        print("Failed to send message:", response)

