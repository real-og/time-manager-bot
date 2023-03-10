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
        curr_action_str = await logic.get_state_var(state, 'curr_action')
        if curr_action_str == None:
            await message.answer(texts.nothing_happens, reply_markup=kb.menu_kb)
            return
        await message.answer(texts.compose_confirmation(logic.Action.get_entity(curr_action_str)),
                                                        reply_markup=kb.confirm_kb)
        await State.confirm_removing.set()
    if input == kb.analysis:
        await message.answer('в разработке', reply_markup=kb.menu_kb)
    if input == kb.today_stat:
        text = await texts.compose_today_stat(state)
        await message.answer(text, reply_markup=kb.menu_kb)
    if input == kb.categories:
        cats = await logic.get_state_var(state, 'cats')
        await message.answer(texts.compose_cats(cats), reply_markup=kb.cats_kb)
        await State.categories.set()
    if input == kb.help:
        await message.answer(texts.help, reply_markup=kb.menu_kb)
        
