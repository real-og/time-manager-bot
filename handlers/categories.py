from loader import dp
import texts
from aiogram import types
import keyboards as kb
from aiogram.dispatcher import FSMContext
import logic
from states import *

@dp.message_handler(state=State.categories)
async def handle_cats(message: types.Message, state: FSMContext):
    lang_code = logic.check_language(message.from_user.language_code)
    input = message.text
    if input == kb.add[lang_code]:
        await message.answer(texts.ask_for_name[lang_code], reply_markup=kb.get_back_kb(lang_code))
        await State.adding.set()
    if input == kb.remove[lang_code]:
        await message.answer(texts.ask_for_num[lang_code], reply_markup=kb.get_back_kb(lang_code))
        await State.removing.set()
    if input == kb.back[lang_code]:
        menu = await texts.compose_menu(state, lang_code)
        await message.answer(menu, reply_markup=kb.get_menu_kb(lang_code))
        await State.menu.set()

@dp.message_handler(state=State.adding)
async def add_cat(message: types.Message, state: FSMContext):
    lang_code = logic.check_language(message.from_user.language_code)
    input = message.text
    if input == kb.back[lang_code]:
        menu = await texts.compose_menu(state, lang_code)
        await message.answer(menu, reply_markup=kb.get_menu_kb(lang_code))
        await State.menu.set()
    else:
        await logic.add_to_state_list(state, 'cats', input)
        cats = await logic.get_state_var(state, 'cats')
        await message.answer(texts.added[lang_code])
        await message.answer(texts.compose_cats(cats, lang_code), reply_markup=kb.get_cats_kb(lang_code))
        await State.categories.set()

@dp.message_handler(state=State.removing)
async def remove_cat(message: types.Message, state: FSMContext):
    lang_code = logic.check_language(message.from_user.language_code)
    input = message.text
    if input == kb.back[lang_code]:
        menu = await texts.compose_menu(state, lang_code)
        await message.answer(menu, reply_markup=kb.get_menu_kb(lang_code))
        await State.menu.set()
    else:
        cats = await logic.get_state_var(state, 'cats')
        if input in cats:
            await logic.remove_from_state_list(state, 'cats', input)
            cats.remove(input)
            await message.answer(texts.removed[lang_code])
        else:
            await message.answer(texts.no_such_category[lang_code])
        await message.answer(texts.compose_cats(cats, lang_code), reply_markup=kb.get_cats_kb(lang_code))
        await State.categories.set()


