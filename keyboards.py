from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from typing import List

start = '✍️ Начать'
finish = '💤 Закончить'
categories = '📌Категории'
analysis = 'Аналитика'
today_stat = '📈Статистика сегодня'
help = '❓Помощь'
menu_kb = ReplyKeyboardMarkup(keyboard = [[start, finish],
                                          [categories, analysis],
                                          [today_stat, help]],
                              resize_keyboard=True,
                              one_time_keyboard=True)
add = '➕Добавить'
remove = '♻️Удалить'
back = '🔙Назад'
cats_kb = ReplyKeyboardMarkup(keyboard = [[add, remove],
                                          [back]],
                              resize_keyboard=True,
                              one_time_keyboard=True)

back_kb = ReplyKeyboardMarkup(keyboard = [[back]],
                              resize_keyboard=True,
                              one_time_keyboard=True)

def compose_categories_kb(cats: List[str]) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
    
    for cat in cats:
        kb.insert(KeyboardButton(cat))
    kb.row(back)
    return kb

yes = 'Да'
no = 'Нет'
confirm_kb = ReplyKeyboardMarkup(keyboard = [[yes, no]],
                                resize_keyboard=True,
                                one_time_keyboard=True)


