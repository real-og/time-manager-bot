from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
import logging
import os



logging.basicConfig(level=logging.INFO)
SHEET_LINK = str(os.environ.get('SHEET_LINK'))
API_TOKEN = str(os.environ.get('BOT_TOKEN'))

storage = RedisStorage2(db=2)
# storage = MemoryStorage()
bot = Bot(token=API_TOKEN, parse_mode="HTML")

dp = Dispatcher(bot, storage=storage)