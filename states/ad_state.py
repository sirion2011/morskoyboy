from aiogram.fsm.state import StatesGroup, State


class Add(StatesGroup):
    amount_od_buttoms = State()
    timedelta = State()
    get_link = State()
    get_name = State()
    yes_no = State()
    forward_message = State()
    get_forward_message = State()
    final = State()
