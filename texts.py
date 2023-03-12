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

def compose_time_delta(secs: int) -> str:
    text = ''
    if secs >= 60 * 60:
        text += f"{secs // (60 * 60)} ч  "
    if secs >= 60:
        text += f"{secs % (60 * 60) // 60} мин  "
    text += f"{secs % 60} сек"
    return text

async def compose_today_stat(state: FSMContext) -> str:
    data = await state.get_data()
    curr_action = data.get('curr_action')
    actions = data.get('actions')
    if curr_action:
        act = Action.get_entity(curr_action)
        text = f"<i>Прямо сейчас:</i>\n<b>{act.name}</b> уже {compose_time_delta(act.get_duration_secs())}"
    else:
        text = str(Action.get_entity(curr_action)) if curr_action else "<i>Прямо сейчас ничего не выполняете</i>"

    if len(actions) == 0:
        return text + '\n\n<i>Сегодня ещё без активностей ((</i>'
    text += '\n\n<b><i>***Сегодня уже сделано***</i></b>\n\n'
    text += 'Начало  | Действие | Длительность\n'
    for action_str in actions:
        action = Action.get_entity(action_str)
        text += f"{action.start.time()} <b>| {action.name} |</b> {compose_time_delta(action.get_duration_secs())}\n"


    text += "\n<b><i>***Суммарно за день***</i></b>\n\n"
    for name, secs in group_by_name(actions).items():
        text += f"<b>{name}: </b>{compose_time_delta(secs)}\n"
    return text

