from loader import dp, bot
import texts
from aiogram import types
import keyboards as kb
from aiogram.dispatcher import FSMContext
from states import *
import logic
import sys


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await bot.send_message(277961206, str(message.from_user.id))

    data = await state.get_data()
    cats = data.get('cats', logic.default_cats)
    curr_action = data.get('curr_action')
    actions = data.get('actions', [])

    await state.update_data(cats=cats, curr_action=curr_action, actions=actions)
    menu = await texts.compose_menu(state)
    await message.answer(menu, reply_markup=kb.menu_kb)
    await State.menu.set()


