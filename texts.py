from typing import List
from datetime import datetime
from aiogram.dispatcher import FSMContext
from logic import Action, group_by_name

start = "lets go!"
start = {   'ru' : 'Поехали',
            'en' : "Let's go",
            'be' : "Пачынаеи" 
}

# menu = "Ты в меню"

async def compose_menu(state: FSMContext) -> str:
    text = '📋<b>Меню</b>📋\n\n'
    data = await state.get_data()
    act = Action.get_entity(data.get('curr_action'))
    if act:
        return text + f"<i>Сейчас: <b>{act.name}</b> уже <b>{compose_time_delta(act.get_duration_secs())}</b></i>"
    return text + "<i>Сейчас ничего не выполняется</i>"


def compose_cats(categories: List[str]) -> str:
    if categories == None or len(categories) == 0:
        return 'Нет кастомных'
    text = ''
    for i, cat in enumerate(categories):
        text += f"<b>{i+1}.</b> {cat}\n"
    return text

ask_for_num = 'Вводи <b>название</b> категории, которая будет удалёна🗑'
ask_for_name = "Вводи <b>название</b> кастомной категории📌"

added = '<i><b>Добавлено☑️</b></i>'
removed = '<i><b>Удалено☑️</b></i>'

choose_action = '📝<b>Что начинаешь делать?</b>\n\n<i>Выбирай из категорий или вводи текстом</i>'

def compose_started(name: str, start_datetime: datetime) -> str:
    return f"⏳ Начато <b>{name}</b> в {start_datetime.strftime('%H:%M:%S')}"

def compose_finished(action: Action) -> str:
    return f"⌛️ Окончено <b>{action.name}</b> спустя {compose_time_delta(action.get_duration_secs())}"

def compose_confirmation(curr_action: Action) -> str:
    return f"Точно закончить <b>{curr_action.name}?</b>"

confirmed = 'Сделано'
aborted = 'Отменено'
wrong_input = 'не понял ...\n\n<i>Используй клавиатуру или /start</i>'

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
        text += '\n\n<i>Сегодня ещё без законченных активностей ((</i>'
    else:
        text += '\n\n<b><i>***Сегодня уже сделано***</i></b>\n\n'
        text += 'Начало  | Действие | Длительность'
        for action_str in actions:
            action = Action.get_entity(action_str)
            text += f"\n{action.start.time()} <b>| {action.name} |</b> {compose_time_delta(action.get_duration_secs())}"

    if curr_action:
        actions.append(curr_action)
    if len(actions) != 0:
        text += "\n\n<b><i>***Суммарно за день***</i></b>\n\n"
        sorted_dict = sorted(group_by_name(actions).items(), key=lambda x: x[1], reverse=True)
        for name, secs in sorted_dict:
            text += f"<b>{name}: </b>{compose_time_delta(secs)}\n"
    return text

nothing_happens = "<i>Сейчас ничего не происходит</i>"
no_such_category = "<i>Такой категории нет</i>"

help = """<b><i>Этот бот помогает следить, на что уходят 24 часа в твоих сутках</i></b>

<b>"Начать"</b> - включай, когда начинаешь делать что-то новое: учить английский, готовить завтрак, играть к CS. Если что-то уже начато, оно автоматически завершится.

<b>"Закончить"</b> - если решил что-то закончить и ничего не начинать. ушёл в себя.

<b>"Категории"</b> - здесь ты можешь добавлять и удалять наиболее частые дела, чтобы потом более просто начинать и завершать их.

<b>"Статистика сегодня"</b> - все твои действия по порядку, а также суммарное время, потраченное на каждое занятие.

<b>"Аналитика"</b> - пиши @bot_deal, что хочешь здесь увидеть: отчёт по дням, отчет за неделю, а что в отчетах? а может график или диаграмму мм?"""

help = {'ru' : """<b><i>Этот бот помогает следить, на что уходят 24 часа в твоих сутках</i></b>\n
<b>"Начать"</b> - включай, когда начинаешь делать что-то новое: учить английский, готовить завтрак, играть к CS. Если что-то уже начато, оно автоматически завершится.\n
<b>"Закончить"</b> - если решил что-то закончить и ничего не начинать. ушёл в себя.\n
<b>"Категории"</b> - здесь ты можешь добавлять и удалять наиболее частые дела, чтобы потом более просто начинать и завершать их.\n
<b>"Статистика сегодня"</b> - все твои действия по порядку, а также суммарное время, потраченное на каждое занятие.\n
<b>"Аналитика"</b> - пиши @bot_deal, что хочешь здесь увидеть: отчёт по дням, отчет за неделю, а что в отчетах? а может график или диаграмму мм?""",

        'en' : """<b><i>This bot helps to keep track of how you spend your time during the day</i></b>\n
<b>"Start"</b> - choose when you start doing something new: learning English, cooking breakfast, playing CS. If something has already started, it will automatically finished.\n
<b>"Finish"</b> - if you decide to finish something and not start anything. Something you don't want to talk about or just staring ate the wall.\n
<b>"Categories"</b> - here you can manage the most frequent activities so that they appear as buttons when you decide to start something\n
<b>"Today stat"</b> - all your activities in order and  the total time spent on each one.\n
<b>"analytics"</b> - text @bot_deal to propose your ideas ans make it better"""}