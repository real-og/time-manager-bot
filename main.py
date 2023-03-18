from loader import dp, bot
from aiogram import executor
from handlers import *
import asyncio
import aioschedule as schedule
import logic
import json
import db
import texts
from datetime import datetime, timedelta
import logic


async def scheduled_saving():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(3)

schedule.every().day.at("00:00").do(logic.save_to_db)


async def main():
    asyncio.create_task(scheduled_saving())
    await dp.start_polling()

if __name__ == '__main__':
    print('starting')
    asyncio.run(main())
