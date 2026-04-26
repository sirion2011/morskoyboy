from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class ExtraLiveKeyboard:

    def __init__(self):
        pass

    @staticmethod
    def extra_live():
        builder = ReplyKeyboardBuilder()
        builder.row(
            types.KeyboardButton(text="Давай конечно"),
        )
        builder.row(
            types.KeyboardButton(text="Нет, спасибо")
        )
        return builder.as_markup(resize_keyboard=True)