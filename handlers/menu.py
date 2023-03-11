from loader import dp
import texts
from aiogram import types
from aiogram.dispatcher import FSMContext
import logic
import keyboards as kb
from states import *

@dp.message_handler(state=State.menu)
async def handle_menu(message: types.Message, state: FSMContext):
    input = message.text
    if input == kb.start:
        cats = await logic.get_state_var(state, 'cats')
        await message.answer(texts.choose_action, reply_markup=kb.compose_categories_kb(cats))
        await State.start_action.set()
    if input == kb.finish:
        await message.answer(texts.menu, reply_markup=kb.menu_kb)
        await State.menu.set()
    if input == kb.analysis:
        pass
    if input == kb.today_stat:
        pass
    if input == kb.categories:
        cats = await logic.get_state_var(state, 'cats')
        await message.answer(texts.compose_cats(cats), reply_markup=kb.cats_kb)
        await State.categories.set()
        
