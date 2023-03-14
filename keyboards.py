from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from typing import List

start = '✍️ Начать'
start = {
    'ru' : '✍️ Начать',
    'en' : '✍️ Start'
}

finish = '💤 Закончить'
finish = {
    'ru' : '💤 Закончить',
    'en' : '💤 Finish'
}

categories = '📌Категории'
categories = {
    'ru' : '📌Категории',
    'en' : '📌Categories'
}

analysis = 'Аналитика'
analysis = {
    'ru' : 'Аналитика',
    'en' : 'Analytics'
}

today_stat = '📈Статистика сегодня'
today_stat = {
    'ru' : '📈Статистика сегодня',
    'en' : '📈Today stat'
}

help = '❓Помощь'
help = {
    'ru' : '❓Помощь',
    'en' : '❓Help'
}

menu_kb = ReplyKeyboardMarkup(keyboard = [[start, finish],
                                          [categories, analysis],
                                          [today_stat, help]],
                              resize_keyboard=True,
                              one_time_keyboard=True)
add = '➕Добавить'
add = {
    'ru' : '➕Добавить',
    'en' : '➕Add'
}

remove = '♻️Удалить'
remove = {
    'ru' : '♻️Удалить',
    'en' : '♻️Remove'
}

back = '🔙Назад'
back = {
    'ru' : '🔙Назад',
    'en' : '🔙Back'
}
cats_kb = ReplyKeyboardMarkup(keyboard = [[add, remove],
                                          [back]],
                              resize_keyboard=True,
                              one_time_keyboard=True)

back_kb = ReplyKeyboardMarkup(keyboard = [[back]],
                              resize_keyboard=True,
                              one_time_keyboard=True)

def compose_categories_kb(cats: List[str], lang: str = 'en') -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
    for cat in cats:
        kb.insert(KeyboardButton(cat))
    kb.row(back[lang])
    return kb

yes = 'Да'
yes = {
    'ru' : 'Да',
    'en' : 'Yes'
}

no = 'Нет'
no = {
    'ru' : 'Нет',
    'en' : 'No'
}
confirm_kb = ReplyKeyboardMarkup(keyboard = [[yes, no]],
                                resize_keyboard=True,
                                one_time_keyboard=True)


