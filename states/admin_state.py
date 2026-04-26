from aiogram.fsm.state import StatesGroup, State


class Present(StatesGroup):
    username = State()
