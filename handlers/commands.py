from loader import dp
import texts
from aiogram import types
import keyboards as kb
from aiogram.dispatcher import FSMContext
from states import *
import logic
import sys


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(sys.getsizeof(data))
    cats = data.get('cats', logic.default_cats)
    curr_action = data.get('curr_action')
    actions = data.get('actions', [])
   
    await state.update_data(cats=cats, curr_action=curr_action, actions=actions)
    await message.answer(texts.menu, reply_markup=kb.menu_kb)
    await State.menu.set()


