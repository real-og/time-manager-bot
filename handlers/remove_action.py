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
    print(22)
    input = message.text
    if input == kb.no:
        await message.answer(texts.aborted, reply_markup=kb.menu_kb)
    elif input == kb.yes:
        await logic.finish_current_action(state)
        await message.answer(texts.confirmed, reply_markup=kb.menu_kb)
    else:
        await message.answer(texts.wrong_input, reply_markup=kb.menu_kb)
    await State.menu.set()