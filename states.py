from aiogram.dispatcher.filters.state import StatesGroup, State


class State(StatesGroup):
    menu = State()
    categories = State()
    removing = State()
    adding = State()
    start_action = State()
    confirm_removing = State()
    analytics_menu = State()
