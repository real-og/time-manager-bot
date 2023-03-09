from loader import dp
import texts
from aiogram import types
import keyboards as kb
from states import *

@dp.message_handler(state=State.categories)
async def show_cats(message: types.Message):
    input = message.text
    if input == kb.add:
        await message.answer(texts.ask_for_name, reply_markup=kb.back)
        await State.adding.set()
    if input == kb.remove:
        await message.answer(texts.ask_for_num, reply_markup=kb.back_kb)
        await State.removing.set()
    if input == kb.back:
        await message.answer(texts.menu, reply_markup=kb.menu_kb)
        await State.menu.set()

@dp.message_handler(state=State.adding)
async def add_cat(message: types.Message):
    input = message.text
    if input == kb.back:
        await message.answer(texts.menu, reply_markup=kb.menu_kb)
        await State.menu.set()
    else:
        await message.answer(texts.added)
        await message.answer(texts.compose_cats(['test1', 'test2']), reply_markup=kb.cats_kb)
        await State.categories.set()

@dp.message_handler(state=State.removing)
async def remove_cat(message: types.Message):
    input = message.text
    if input == kb.back:
        await message.answer(texts.menu, reply_markup=kb.menu_kb)
        await State.menu.set()
    else:
        await message.answer(texts.removed)
        await message.answer(texts.compose_cats(['test1', 'test2']), reply_markup=kb.cats_kb)
        await State.categories.set()


