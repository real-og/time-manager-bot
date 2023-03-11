from typing import List, Any
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import FSMContext
from states import *
from datetime import datetime
import json

class Action():
    def __init__(self, name: str, start: datetime, end: datetime = None) -> None:
        self.name = name
        self.start = start
        self.end = end

    def finish(self):
        self.end = datetime.now()
    
    def json(self) -> str:
        data = {
            "name": self.name,
            "start": self.start.strftime("%Y-%m-%d %H:%M:%S"),
        }
        data['end'] = self.end.strftime("%Y-%m-%d %H:%M:%S") if self.end else None
        return json.dumps(data, indent=4)

    def __str__(self) -> str:
        return f"Action: {self.name} from {self.start} till {self.end}"

    @classmethod
    def get_entity(cls, action_str: str):
        data = json.loads(action_str)
        action = Action(data['name'],
                        datetime.strptime(data['start'], "%Y-%m-%d %H:%M:%S"))
        if data['end']:
            action.end = datetime.strptime(data['end'], "%Y-%m-%d %H:%M:%S")
        return action

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