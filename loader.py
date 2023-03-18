from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
import logging
import os


logging.basicConfig(level=logging.WARNING)
ADMIN_ID = str(os.environ.get('ADMIN_ID'))
API_TOKEN = str(os.environ.get('BOT_TOKEN'))

default_cats = {
    'ru': ['Сон', 'Дорога', 'Еда', 'Работа', 'Учёба'],
    'en': ['Working', 'Studing', 'Walking', 'Rest', 'Movies'],
}
supported_langs = ['en', 'ru']

# storage = RedisStorage2(db=2)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN, parse_mode="HTML")

dp = Dispatcher(bot, storage=storage)
