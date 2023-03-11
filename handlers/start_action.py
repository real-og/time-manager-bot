from loader import dp
import texts
from aiogram import types
import keyboards as kb
from aiogram.dispatcher import FSMContext
import logic
from datetime import datetime
from states import *

@dp.message_handler(state=State.start_action)
async def setup_category(message: types.Message, state: FSMContext):
    input = message.text
    if input == kb.back:
        await message.answer(texts.menu, reply_markup=kb.menu_kb)
    else:
        start_datetime = datetime.now()
        await logic.start_action(logic.Action(input, start_datetime), state)
        await message.answer(texts.compose_started(input, start_datetime), reply_markup=kb.menu_kb)
    await State.menu.set()