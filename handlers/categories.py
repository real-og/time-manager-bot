from loader import dp
import texts
from aiogram import types
import keyboards as kb
from aiogram.dispatcher import FSMContext
import logic
from states import *

@dp.message_handler(state=State.categories)
async def handle_cats(message: types.Message, state: FSMContext):
    input = message.text
    if input == kb.add:
        await message.answer(texts.ask_for_name, reply_markup=kb.back_kb)
        await State.adding.set()
    if input == kb.remove:
        await message.answer(texts.ask_for_num, reply_markup=kb.back_kb)
        await State.removing.set()
    if input == kb.back:
        menu = await texts.compose_menu(state)
        await message.answer(menu, reply_markup=kb.menu_kb)
        await State.menu.set()

@dp.message_handler(state=State.adding)
async def add_cat(message: types.Message, state: FSMContext):
    input = message.text
    if input == kb.back:
        menu = await texts.compose_menu(state)
        await message.answer(menu, reply_markup=kb.menu_kb)
        await State.menu.set()
    else:
        await logic.add_to_state_list(state, 'cats', input)
        cats = await logic.get_state_var(state, 'cats')
        await message.answer(texts.added)
        await message.answer(texts.compose_cats(cats), reply_markup=kb.cats_kb)
        await State.categories.set()

@dp.message_handler(state=State.removing)
async def remove_cat(message: types.Message, state: FSMContext):
    input = message.text
    if input == kb.back:
        menu = await texts.compose_menu(state)
        await message.answer(menu, reply_markup=kb.menu_kb)
        await State.menu.set()
    else:
        cats = await logic.get_state_var(state, 'cats')
        if input in cats:
            await logic.remove_from_state_list(state, 'cats', input)
            cats.remove(input)
            await message.answer(texts.removed)
        else:
            await message.answer(texts.no_such_category)
        await message.answer(texts.compose_cats(cats), reply_markup=kb.cats_kb)
        await State.categories.set()


