from loader import dp
import texts
from aiogram import types
import keyboards as kb
from aiogram.dispatcher import FSMContext
import logic
from states import *
import matplotlib.pyplot as plt
import db
from datetime import datetime, timedelta
import os

@dp.message_handler(state=State.analytics_menu)
async def handle_analytics_choise(message: types.Message, state: FSMContext):
    lang_code = logic.check_language(message.from_user.language_code)
    input = message.text

    if input == kb.weekly[lang_code]:
        data = await state.get_data()
        img_name = logic.generate_weekly_diagram(message.from_user.id, data, lang_code)
        with open(img_name, 'rb') as photo:
            await message.answer_photo(photo)
        os.remove(img_name)
        



    if input == kb.compare[lang_code]:
        data = await state.get_data()
        await message.answer(texts.compose_comparison(message.from_user.id,
                                                      data,
                                                      lang_code),
                              reply_markup=kb.get_analytics_kb(lang_code))

    if input == kb.mystery[lang_code]:
        await message.answer(texts.mystery_message[lang_code],
                             reply_markup=kb.get_analytics_kb(lang_code))

    if input == kb.back[lang_code]:
        menu = await texts.compose_menu(state, lang_code)
        await message.answer(menu, reply_markup=kb.get_menu_kb(lang_code))
        await State.menu.set()

