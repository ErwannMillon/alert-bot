import datetime
import json
import os
import time
import traceback

import dotenv
import requests
from supabase import create_client
from tqdm import tqdm

dotenv.load_dotenv()

def get_supabase_client():
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase

supabase = get_supabase_client()
def create_supabase_row(data, table_name="cluster_errors"):
    # try a few times bc the supabase python package is sketchy
    for i in range(5):
        try:
            supabase = get_supabase_client()
            response = supabase.table(table_name).insert(data).execute()
            return
        except:
            print("SUPABASE ERROR")
            traceback.print_exc()
        time.sleep(1)


def send_telegram_notification(message):
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    print(TELEGRAM_BOT_TOKEN)
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    try:
        error = {
            "error_message": message,
        }
        create_supabase_row(error)
        telegram_api_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
        data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
        response = requests.post(telegram_api_url, json=data)
        if response.status_code != 200:
            print('Failed to send Telegram notification:', response.content)
    except:
        print("caught exception: Failed to send Telegram notification")
        traceback.print_exc()
if __name__ == '__main__':
    send_telegram_notification("test")

