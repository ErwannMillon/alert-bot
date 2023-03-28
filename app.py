import json
import os

import dotenv
import fastapi
import requests
from fastapi import FastAPI

app = FastAPI()

dotenv.load_dotenv()
# from pyngrok import ngrok


TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram_notification(message):
    telegram_api_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    response = requests.post(telegram_api_url, json=data)
    if response.status_code != 200:
        print('Failed to send Telegram notification:', response.content)

@app.route('/', methods=['POST'])
async def handle_webhook(req: fastapi.Request) -> None:
    print(TELEGRAM_BOT_TOKEN)
    print(TELEGRAM_CHAT_ID)
    # data = json.loads(req.data)
    # data = await req
    data = await req.json()

    print(data)
    alert = data['incident']['condition_name']
    message = f'Google Cloud Monitoring alert: {alert}'
    send_telegram_notification(message)
    return fastapi.Response(status_code=200)

@app.route('/test')
def test(x):
    return "healthy"

    
if __name__ == '__main__':
    app.run()
