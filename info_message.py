"""Generate a standard informative message"""
import sys

import common.telegram_dispatcher as td

if __name__ == "__main__":
    if not sys.stdin.isatty():
        pipe_data = sys.stdin.read().strip()

    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} subject")
        sys.exit(1)

    subject = f"""
📢 Informational message!

» {sys.argv[1]} «
"""

    success, response = td.send_telegram_message(subject, pipe_data)

    if success:
        print("Message sent successfully:", response)
    else:
        print("Failed to send message:", response)
