from loader import dp
import texts
from aiogram import types

@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message):
    await message.answer(texts.start)
