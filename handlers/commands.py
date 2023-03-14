from loader import dp, bot, ADMIN_ID
import texts
from aiogram import types
import keyboards as kb
from aiogram.dispatcher import FSMContext
from states import *
import logic
import sys
import loader


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, str(message.from_user.id))

    lang_code = logic.check_language(message.from_user.language_code)
    print(lang_code)
    data = await state.get_data()
    cats = data.get('cats', loader.default_cats[lang_code])
    curr_action = data.get('curr_action')
    actions = data.get('actions', [])

    await state.update_data(cats=cats, curr_action=curr_action, actions=actions)
    menu = await texts.compose_menu(state, lang_code)
    await message.answer(menu, reply_markup=kb.get_menu_kb(lang_code))
    await State.menu.set()


