from typing import List
from datetime import datetime
from aiogram.dispatcher import FSMContext
from logic import Action, group_by_name
import json
import db

start = "lets go!"
start = {
    'ru' : 'Поехали',
    'en' : "Let's go",
    'be' : "Пачынаеи" 
}

menu_header = {
    'ru': "📋<b>Меню</b>📋",
    'en': "📋<b>Menu</b>📋"
}

async def compose_menu(state: FSMContext, lang: str = 'en') -> str:
    text = f'{menu_header[lang]}\n\n'
    data = await state.get_data()
    act = Action.get_entity(data.get('curr_action'))
    if act:
        if lang == 'ru':
            return text + f"<i>Сейчас: <b>{act.name}</b> уже <b>{compose_time_delta(act.get_duration_secs(), lang)}</b></i>"
        else:
            return text + f"<i>Now: <b>{act.name}</b> for <b>{compose_time_delta(act.get_duration_secs(), lang)}</b></i>"
    return text + f"<i>{nothing_happens[lang]}</i>"


def compose_cats(categories: List[str], lang: str = 'en') -> str:
    if categories == None or len(categories) == 0:
        return no_custom_cats[lang]
    text = ''
    for i, cat in enumerate(categories):
        text += f"<b>{i+1}.</b> {cat}\n"
    return text

no_custom_cats = {
    'ru': "Нет кастомных",
    'en': "No custom categories"
}

ask_for_num = 'Вводи <b>название</b> категории, которая будет удалёна🗑'
ask_for_num = {
    'ru': "Вводи <b>название</b> категории, которая будет удалёна🗑",
    'en': "Type <b>the name</b> of category to remove🗑"
}

ask_for_name = "Вводи <b>название</b> кастомной категории📌"
ask_for_name = {
    'ru': "Вводи <b>название</b> кастомной категории📌",
    'en': "Type <b>the name</b> of your custom category📌"
}

added = '<i><b>Добавлено☑️</b></i>'
added = {
    'ru': "<i><b>Добавлено☑️</b></i>",
    'en': "<i><b>Added☑️</b></i>"
}

removed = '<i><b>Удалено☑️</b></i>'
removed = {
    'ru': "<i><b>Удалено☑️</b></i>",
    'en': "<i><b>Removed☑️</b></i>"
}

choose_action = '📝<b>Что начинаешь делать?</b>\n\n<i>Выбирай из категорий или вводи текстом</i>'
choose_action = {
    'ru': "📝<b>Что начинаешь делать?</b>\n\n<i>Выбирай из категорий или вводи текстом</i>",
    'en': "📝<b>What are you goint to start?</b>\n\n<i>Choose from categories below or type your one</i>"
}

def compose_started(name: str, start_datetime: datetime, lang: str = 'en') -> str:
    if lang == 'ru':
        return f"⏳ Начато <b>{name}</b> в {start_datetime.strftime('%H:%M:%S')}"
    else:
        return f"⏳ Started <b>{name}</b> at {start_datetime.strftime('%H:%M:%S')}"

def compose_finished(action: Action, lang: str = 'en') -> str:
    if lang == 'ru':
        return f"⌛️ Окончено <b>{action.name}</b> спустя {compose_time_delta(action.get_duration_secs(), lang)}"
    else:
        return f"⌛️ Finished <b>{action.name}</b> after {compose_time_delta(action.get_duration_secs(), lang)}"

def compose_confirmation(curr_action: Action, lang: str = 'en') -> str:
    if lang == 'ru':
        return f"Точно закончить <b>{curr_action.name}?</b>"
    else:
        return f"Are you sure to finish <b>{curr_action.name}?</b>"

confirmed = 'Сделано'
confirmed = {
    'ru': "Сделано",
    'en': "Done"
}

aborted = 'Отменено'
aborted = {
    'ru': "Отменено",
    'en': "Aborted"
}

wrong_input = 'не понял ...\n\n<i>Используй клавиатуру или /start</i>'
wrong_input = {
    'ru': "не понял ...\n\n<i>Используй клавиатуру или /start</i>",
    'en': "can't understand ...\n\n<i>Use buttons or /start</i>"
}

def compose_time_delta(secs: int, lang: str = 'en') -> str:
    text = ''
    if secs >= 60 * 60:
        text += f"{secs // (60 * 60)} {hour_name[lang]}  "
    if secs >= 60:
        text += f"{secs % (60 * 60) // 60} {min_name[lang]}  "
    text += f"{secs % 60} {sec_name[lang]}"
    return text

sec_name = {
    'ru': "сек",
    'en': "sec"
}

min_name = {
    'ru': "мин",
    'en': " min"
}

hour_name = {
    'ru': "ч",
    'en': "h"
}

async def compose_today_stat(state: FSMContext, lang: str = 'en') -> str:
    data = await state.get_data()
    curr_action = data.get('curr_action')
    actions = data.get('actions')
    if curr_action:
        act = Action.get_entity(curr_action)
        if lang == 'ru':
            text = f"<i>Прямо сейчас:</i>\n<b>{act.name}</b> уже {compose_time_delta(act.get_duration_secs(), lang)}"
        else:
            text = f"<i>Now:</i>\n<b>{act.name}</b> lasts for {compose_time_delta(act.get_duration_secs(), lang)}"
    else:
        text = str(Action.get_entity(curr_action)) if curr_action else nothing_happens[lang]

    if len(actions) == 0:
        text += '\n\n' + no_accomplished[lang]
    else:
        text += f'\n\n{accomplished_header[lang]}\n\n'
        text += table_header[lang]
        for action_str in actions:
            action = Action.get_entity(action_str)
            text += f"\n{action.start.time()} <b>| {action.name} |</b> {compose_time_delta(action.get_duration_secs(), lang)}"

    if curr_action:
        actions.append(curr_action)
    if len(actions) != 0:
        text += f"\n\n{total_the_day[lang]}\n\n"
        sorted_dict = sorted(group_by_name(actions).items(), key=lambda x: x[1], reverse=True)
        for name, secs in sorted_dict:
            text += f"<b>{name}: </b>{compose_time_delta(secs, lang)}\n"
    return text

total_the_day = {
    'ru': "<b><i>***Суммарно за день***</i></b>",
    'en': "<b><i>***During the day in total***</i></b>"
}

table_header = {
    'ru': "Начало  | Действие | Длительность",
    'en': "Start   | Action | Duration"
}

accomplished_header = {
    'ru': "<b><i>***Сегодня уже сделано***</i></b>",
    'en': "<b><i>***Today finished***</i></b>"
}

no_accomplished = {
    'ru': "<i>Сегодня ещё без законченных активностей ((</i>",
    'en': "<i>There is no finished actions yet</i>"
}

nothing_happens = "<i>Сейчас ничего не происходит</i>"
nothing_happens = {
    'ru': "<i>Сейчас ничего не происходит</i>",
    'en': "<i>You're doing nothing now</i>"
}

no_such_category = "<i>Такой категории нет</i>"
no_such_category= {
    'ru' : '<i>Такой категории нет</i>',
    'en' : '<i>No such categorie</i>'
}

help = {
    'ru' : """<b><i>Этот бот помогает следить, на что уходят 24 часа в твоих сутках</i></b>\n
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

in_development = {
    'ru' : 'В разработке', 
    'en' : 'In progress'
}

def compose_daily_report(date : str, actions: List) -> str:
    text = f"<b>{date}</b>\n\n"
    if actions == None:
        return text
    sorted_dict = sorted(group_by_name(actions).items(), key=lambda x: x[1], reverse=True)
    for name, secs in sorted_dict:
        text += f"<b>{name}</b> - {compose_time_delta(secs)}\n"
    return text

mystery_message = {
    'ru': """<i><b>Этот бот скорее для резюме, однако выполняет то, на что заявлен</b></i>\n
Если тебе интересно сотрудничать: нужен софт, нужен разработчик, дизайнер либо какое-то \
решение для бизнеса или стартпа, хочешь автоматизировать свои процессы, собрать данные и \
составить статистику, - пиши @bot_deal\n
<i>Ну и фидбэк по этому боту тоже приятно ))</i>""",

    'en': """<i><b>This bot is more about resume but still has some purpose</b></i>\n
If you're interested in cooperation: you need good software, need an engineer or \
designer for your business or startup, you have some crazy ideas or wanna collect \
statistics, then text me @bot_deal\n
<i>This particular bot feedback appreciated too</i>"""
}

analytics_menu = {
    'ru': "<i><b>Немного аналитики</b></i>",
    'en': "<i><b>Some statistics</b></i>"
}

no_yesterday_report = {
    'ru' : '<i>Вчера ничего не было</i>',
    'en' : '<i>There are no yesterday activities</i>'
}

no_today_report = {
    'ru' : '<i>Сегодня ничего не было</i>',
    'en' : '<i>There are no today activities</i>'
}

diff_header = {
    'ru': "<i><b>Разница со вчера</b></i>",
    'en': "<i><b>Difference from yesterday</b></i>"
}

def compose_comparison(id: int, today_data: dict, lang:str = 'en') -> str:
    text = diff_header[lang] + '\n\n'
    if today_data.get('curr_action') and (today_data['actions'] != None):
        today_data['actions'].append(today_data['curr_action'])
    yest_reports = db.get_report_by_date(id, datetime.now().date())

    if not yest_reports:
        return no_yesterday_report[lang]
    
    if not today_data['actions']:
        return no_today_report[lang]

    yest_dict = yest_reports[0]['actions']

    today_dict = group_by_name(today_data['actions'])

    for k in yest_dict:
        today = today_dict.get(k, 0)
        diff = today - yest_dict[k]
        if diff < 0:
            text += f'🔴↘️<b>{k}:</b> -{compose_time_delta(abs(diff), lang)}\n'
        else:
            text += f'🟢↗️<b>{k}:</b> +{compose_time_delta(diff, lang)}\n'

    for k in today_dict:
        if not yest_dict.get(k):
            text += f'🟢↗️<b>{k}:</b> +{compose_time_delta(today_dict[k], lang)}\n'
    return(text)






    
    


