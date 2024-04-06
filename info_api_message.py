"""Generate a standard informative message from an API request"""
from flask import Flask, request, abort

import common.telegram_dispatcher as td

app = Flask(__name__)

@app.route('/send', methods=['POST'])
def send_message():
    """Send message through telegram from this API endpoint"""
    subject = request.form['subject']
    message = request.form['message']
    print(f'Received arguments: {subject}, {message}')

    f_subject = f"""
📢 Informational message!

» {subject} «
"""
    success, response = td.send_telegram_message(f_subject, message)

    if success:
        return f'Message sent successfully: {response}'

    abort(500, f'Failed to send message: {response}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6666)
