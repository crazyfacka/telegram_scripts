# Telegram scripts

This repo has a bunch of scripts that are used to message random stuff that makes sense for my use case.
Use as you see fit.

## Existing scripts

**backup_done.py**
```
usage: backup_done.py backup_file error_file execution_time_in_seconds
```
Sends information about the backed up file, prints the log and humanizes the duration.

**high_mem.py**
```
usage: high_mem.py used_memory_in_bytes used_swap_in_bytes
```
Notifies of high resource usage, and lists the top 5 offending processes.

**info_message.py**
```
usage: echo "Message" | info_message.py message_subject
```
Receives the message via Unix pipe, and the message subject as first argument. As generic as it gets.

## Configuration

You need to obtain a `bot_token` and a `chat_id` from Telegram, as this sends a message directly to a chat.