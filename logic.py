from typing import List, Any, Optional, Dict, Union
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import FSMContext
from states import *
from datetime import datetime, timedelta
import json
from aiogram import types
import db
from loader import dp, bot
import texts


default_cats = ['Сон', 'Дорога', 'Еда', 'Работа', 'Учёба']
supported_langs = ['en', 'ru']

def check_language(lang: str) -> str:
    return lang if lang in supported_langs else 'en'

class Action():
    def __init__(self, name: str, start: datetime = datetime.now(), end: datetime = None) -> None:
        self.name = name
        self.start = start
        self.end = end

    def finish(self):
        self.end = datetime.now()

    def get_duration_secs(self) -> int:
        end = self.end if self.end else datetime.now()
        return int((end - self.start).total_seconds())
    
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
    def get_entity(cls, action_str: str) -> Optional['Action']:
        if action_str == None:
            return None 
        data = json.loads(action_str)
        action = Action(data['name'],
                        datetime.strptime(data['start'], "%Y-%m-%d %H:%M:%S"))
        if data['end']:
            action.end = datetime.strptime(data['end'], "%Y-%m-%d %H:%M:%S")
        return action



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
    return data.get(var_name)

async def finish_current_action(state: FSMContext) -> None:
    data = await state.get_data()
    actions = data.get('actions', [])
    # print(actions)
    curr_action_str = data.get('curr_action')
    if curr_action_str:
        curr_action = Action.get_entity(curr_action_str)
        curr_action.finish()
        actions.append(curr_action.json())
        curr_action_str = None
    await state.update_data(curr_action=curr_action_str, actions=actions)

async def start_action(action: Action, state: FSMContext) -> None:
    await finish_current_action(state)
    if action:
        await state.update_data(curr_action=action.json())


def group_by_name(list: List[Union[Action, str]]) -> Dict[str, int]:
    """
    Returns:
        Dict[str, int]: the key is the name of action
        and the value is the number of spent seconds
    """
    result = dict()
    for item in list:
        if isinstance(item, str):
            item = Action.get_entity(item)
        if result.get(item.name):
            result[item.name] += item.get_duration_secs()
        else:
            result[item.name] = item.get_duration_secs()
    return result


async def save_to_db():
    users = db.get_users()
    for user in users:
        state = dp.current_state(chat=user['id'])
        data = await state.get_data()
        cur_action = Action.get_entity(data.get('curr_action'))
        if cur_action:
            cur_action.start = datetime.now()
        await start_action(cur_action, state)
        data = await state.get_data()
        db.add_report(user['id'], json.dumps(group_by_name(data['actions']), ensure_ascii=False))
        yesterday = datetime.now() - timedelta(days=1)
        yesterday = yesterday.strftime("%Y:%m:%d")
        await bot.send_message(user['id'], texts.compose_daily_report(yesterday, data['actions']))
        await state.update_data(actions=[])



    

