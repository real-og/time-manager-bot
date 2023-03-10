from typing import List, Any
from aiogram.dispatcher import FSMContext

default_cats = ['Сон', 'Дорога', 'Еда', 'Работа', 'Учёба']

def get_categories(id: int) -> List[str]:
    pass

async def add_to_state_list(state: FSMContext, list_name: str, item: Any):
    data = await state.get_data()
    if data.get(list_name):
        data[list_name].append(item)
    else:
        data[list_name] = list(item)
    await state.update_data(cats=data['cats'])

async def remove_from_state_list(state: FSMContext, list_name: str, item: Any):
    data = await state.get_data()
    if data.get(list_name):
        try:
            data[list_name].remove(item)
        except ValueError:
            pass
    else:
        return
    await state.update_data(cats=data['cats'])

async def get_state_var(state: FSMContext, var_name: str) -> Any:
    data = await state.get_data()
    if data.get(var_name):
        return data[var_name]
    return None