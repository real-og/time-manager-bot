from aiogram.dispatcher.filters.state import StatesGroup, State

class State(StatesGroup):
    menu = State()
    categories = State()
    removing = State()
    adding = State()
    start_action = State()