from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ref_keyboard():
    extra_life = InlineKeyboardBuilder()
    buttoms = [
        InlineKeyboardButton(text='❣', callback_data=f'extra_life_info')
    ]
    extra_life.add(*buttoms)
    return extra_life.as_markup(resize_keyboard=True)
