from typing import List

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

