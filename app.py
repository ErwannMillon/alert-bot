import asyncio
import os
from datetime import datetime, timedelta

from aiogram import Bot
from supabase_utils import get_supabase_client

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

print(TELEGRAM_BOT_TOKEN)
ERROR_THRESHOLD = 20
TIME_WINDOW_SECONDS = 60
TIME_WINDOW = timedelta(minutes=TIME_WINDOW_SECONDS*60)
POLL_INTERVAL = 3  # seconds


supabase = get_supabase_client()
bot_token = TELEGRAM_BOT_TOKEN
emergency_chat_id = TELEGRAM_CHAT_ID
bot = Bot(token=bot_token)
from dateutil.parser import parse


async def poll_errors():
    fucked = False
    while True:
        response = supabase.table('cluster_errors').select('created_at').order("created_at", desc=True).limit(ERROR_THRESHOLD).execute().data
        print(len(response))
        print(response)
        error_timestamps = sorted(
            (parse(row['created_at']) for row in response)
        )[:ERROR_THRESHOLD]
        oldest, newest = error_timestamps[0], error_timestamps[-1]
        delta = newest - oldest
        print(delta)
        if (newest - oldest) <= TIME_WINDOW:
            print("error rate exceeded threshold")
            # await bot.send_message(chat_id=emergency_chat_id, text='Error rate exceeded threshold https://media.giphy.com/media/QmKySYr0lCsrC/giphy.gif')
            # send_telegram_notification()
            await asyncio.sleep(TIME_WINDOW_SECONDS)
        await asyncio.sleep(POLL_INTERVAL)

if __name__ == '__main__':
    asyncio.run(poll_errors())
