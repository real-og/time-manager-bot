from loader import dp
import texts
from aiogram import types
from aiogram.dispatcher import FSMContext
import logic
import keyboards as kb
from states import *

@dp.message_handler(state=State.menu)
async def handle_menu(message: types.Message, state: FSMContext):
    lang_code = message.from_user.language_code
    input = message.text
    if input == kb.start[lang_code]:
        cats = await logic.get_state_var(state, 'cats')
        await message.answer(texts.choose_action[lang_code],
                             reply_markup=kb.compose_categories_kb(cats))
        await State.start_action.set()

    if input == kb.finish[lang_code]:
        curr_action_str = await logic.get_state_var(state, 'curr_action')
        if curr_action_str == None:
            await message.answer(texts.nothing_happens[lang_code], reply_markup=kb.get_menu_kb(lang_code))
            return
        await message.answer(texts.compose_confirmation(logic.Action.get_entity(curr_action_str), lang_code),
                                                        reply_markup=kb.get_confirm_kb(lang_code))
        await State.confirm_removing.set()

    if input == kb.analysis[lang_code]:
        await message.answer(texts.analytics_menu[lang_code], reply_markup=kb.get_analytics_kb(lang_code))
        await State.analytics_menu.set()

    if input == kb.today_stat[lang_code]:
        text = await texts.compose_today_stat(state, lang_code)
        await message.answer(text, reply_markup=kb.get_menu_kb(lang_code))

    if input == kb.categories[lang_code]:
        cats = await logic.get_state_var(state, 'cats')
        await message.answer(texts.compose_cats(cats, lang_code), reply_markup=kb.get_cats_kb(lang_code))
        await State.categories.set()

    if input == kb.help[lang_code]:
        await message.answer(texts.help[lang_code], reply_markup=kb.get_menu_kb(lang_code))
        
