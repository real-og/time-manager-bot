from typing import List
from datetime import datetime
from aiogram.dispatcher import FSMContext
from logic import Action, group_by_name

start = "lets go!"

menu = "Ты в меню"

def compose_cats(categories: List[str]) -> str:
    if categories == None or len(categories) == 0:
        return 'Нет кастомных'
    text = ''
    for i, cat in enumerate(categories):
        text += f"<b>{i+1}.</b> {cat}\n"
    return text

ask_for_num = 'Вводи название категории, которая будет удалёна'
ask_for_name = "Вводи имя"

added = 'Добавлено'
removed = 'Удалено'

choose_action = 'что делаешь - из клавы или вводи сам'

def compose_started(name: str, start_datetime: datetime) -> str:
    return f"Начато <b>{name}</b> в {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}"

def compose_confirmation(curr_action: Action) -> str:
    return f"точно закончить {curr_action}"

confirmed = 'Сделано'
aborted = 'Отменено'
wrong_input = 'не понял'

async def compose_today_stat(state: FSMContext) -> str:
    data = await state.get_data()
    curr_action = data.get('curr_action')
    actions = data.get('actions')
    text = str(Action.get_entity(curr_action)) if curr_action else "Сейчас ничего не выполняете"
    if len(actions) == 0:
        return text + '\n\nСегодня ничего не выполняли.'
    text += '\n\nСегодня делали:\n\n'
    for action_str in actions:
        action = Action.get_entity(action_str)

        text += f"{action.start.time()} - {action.end.time()} <b>{action.name} | </b>"
        if action.get_duration_mins() >= 60:
            text += f'{action.get_duration_mins() / 60}ч {action.get_duration_mins() % 60} мин\n'
        else:
            text += f'{action.get_duration_mins()} мин\n'

    text += "*************\nПо категориям:\n\n"
    for name, mins in group_by_name(actions).items():
        text += f"<b>{name}</b> {mins / 60}ч {mins % 60}мин\n"
    return text

