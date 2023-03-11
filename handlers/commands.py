from loader import dp
import texts
from aiogram import types
import keyboards as kb
from aiogram.dispatcher import FSMContext
from states import *
import logic


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await state.update_data(cats=logic.default_cats)
    await message.answer(texts.menu, reply_markup=kb.menu_kb)
    await State.menu.set()


