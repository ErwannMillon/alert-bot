import json
import os

import requests

# from pyngrok import ngrok

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram_notification(message):
    telegram_api_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    response = requests.post(telegram_api_url, json=data)
    if response.status_code != 200:
        print('Failed to send Telegram notification:', response.content)

def handle_webhook(request):
    data = json.loads(request.data)
    print(data)
    alert = data['incident']['condition_name']
    message = f'Google Cloud Monitoring alert: {alert}'
    send_telegram_notification(message)
    return 'OK'

from flask import Flask, request

app = Flask(__name__)
@app.route('/', methods=['POST'])
def webhook():
    print("aaa")
    return handle_webhook(request)
@app.route('/test')
def test():
    return "OK"

    
if __name__ == '__main__':
    app.run()
