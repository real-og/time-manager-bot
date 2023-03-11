from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from typing import List

start = 'Начать'
finish = 'Закончить'
categories = 'Категории'
analysis = 'Аналитика'
today_stat = 'Статистика сегодня'
menu_kb = ReplyKeyboardMarkup(keyboard = [[start, finish],
                                          [categories, analysis],
                                          [today_stat]],
                              resize_keyboard=True,
                              one_time_keyboard=True)
add = 'Добавить'
remove = 'Удалить'
back = 'Назад'
cats_kb = ReplyKeyboardMarkup(keyboard = [[add, remove],
                                          [back]],
                              resize_keyboard=True,
                              one_time_keyboard=True)

back_kb = ReplyKeyboardMarkup(keyboard = [[back]],
                              resize_keyboard=True,
                              one_time_keyboard=True)

def compose_categories_kb(cats: List[str]) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for cat in cats:
        kb.add(KeyboardButton(cat))
    kb.add(back)
    return kb


