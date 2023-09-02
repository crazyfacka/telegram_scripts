import humanize
import os
import subprocess
import sys

import common.telegram_dispatcher as td

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

    errors = ""
    with open(err_file) as f:
        for line in f:
            errors = errors + line

    f_info = get_file_info(bk_file)

    subject = "🟢📼 Backup complete!"
    text = f"""
It took {humanize.precisedelta(float(bk_time))}

{f_info[0]}
{f_info[1]}

Log:
{errors}
"""

    success, response = td.send_telegram_message(subject, text)

    if success:
        print("Message sent successfully:", response)
    else:
        print("Failed to send message:", response)

