import asyncio
import os
import traceback
from datetime import datetime, timedelta

import pytz
from aiogram import Bot

from alerting import get_supabase_client, send_telegram_notification

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

print(TELEGRAM_BOT_TOKEN)
ERROR_THRESHOLD = int(os.getenv("ERROR_THRESHOLD", 10))
TIME_WINDOW_SECONDS = 60
TIME_WINDOW = timedelta(minutes=TIME_WINDOW_SECONDS/60)
POLL_INTERVAL = 3  # seconds


supabase = get_supabase_client()
bot_token = TELEGRAM_BOT_TOKEN
emergency_chat_id = TELEGRAM_CHAT_ID
bot = Bot(token=bot_token)
from dateutil.parser import parse


async def poll_errors():
    fucked = False
    while True:
        try:
            response = supabase.table('cluster_errors').select('created_at').order("created_at", desc=True).limit(ERROR_THRESHOLD).execute().data
            # print(len(response))
            # print(response)
            error_timestamps = sorted(
                (parse(row['created_at']) for row in response)
            )[:ERROR_THRESHOLD]
            if not error_timestamps:
                continue
            filtered_timestamps = [timestamp for timestamp in error_timestamps if datetime.now(pytz.timezone(error_timestamps[0].tzname())) - timestamp <= TIME_WINDOW]
            print("len errors", len(filtered_timestamps))
            if len(filtered_timestamps) >= ERROR_THRESHOLD:
                print("error rate exceeded threshold")
                await bot.send_message(chat_id=emergency_chat_id, text='Error rate exceeded threshold https://media.giphy.com/media/QmKySYr0lCsrC/giphy.gif')
                # send_telegram_notification()
                await asyncio.sleep(TIME_WINDOW_SECONDS)

            await asyncio.sleep(POLL_INTERVAL)
            print("waited")
        except:
            print("caught exception: Failed to send Telegram notification")
            traceback.print_exc()
            send_telegram_notification(f"caught exception: Failure in emergency aoert bot : {traceback.format_exc()}")
            await asyncio.sleep(POLL_INTERVAL)


if __name__ == '__main__':
    asyncio.run(poll_errors())
