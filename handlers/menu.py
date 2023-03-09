from loader import dp
import texts
from aiogram import types
import keyboards as kb
from states import *

@dp.message_handler(state=State.menu)
async def handle_menu(message: types.Message):
    input = message.text
    if input == kb.start:
        await message.answer(texts.menu, reply_markup=kb.meny_kb)
        await State.menu.set()
    if input == kb.finish:
        await message.answer(texts.menu, reply_markup=kb.meny_kb)
        await State.menu.set()
    if input == kb.analysis:
        pass
    if input == kb.today_stat:
        pass
    if input == kb.categories:
        await message.answer(texts.compose_cats(['test1', 'test2']), reply_markup=kb.cats_kb)
        await State.categories.set()
        
