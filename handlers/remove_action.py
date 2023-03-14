from loader import dp
import texts
from aiogram import types
import keyboards as kb
from aiogram.dispatcher import FSMContext
import logic
from datetime import datetime
from states import *

@dp.message_handler(state=State.confirm_removing)
async def confirm_removing(message: types.Message, state: FSMContext):
    lang_code = logic.check_language(message.from_user.language_code)
    input = message.text
    if input == kb.no[lang_code]:
        await message.answer(texts.aborted[lang_code], reply_markup=kb.get_menu_kb(lang_code))
    elif input == kb.yes[lang_code]:
        curr_action = await logic.get_state_var(state, 'curr_action')
        text = texts.compose_finished(logic.Action.get_entity(curr_action), lang_code)
        await logic.finish_current_action(state)
        await message.answer(text, reply_markup=kb.get_menu_kb(lang_code))
    else:
        await message.answer(texts.wrong_input[lang_code], reply_markup=kb.get_menu_kb(lang_code))
    await State.menu.set()