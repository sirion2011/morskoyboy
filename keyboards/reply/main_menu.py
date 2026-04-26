from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class MainMenu:

    def __init__(self):
        pass

    @staticmethod
    def main_menu():
        builder = ReplyKeyboardBuilder()
        builder.row(
            types.KeyboardButton(text="Профиль👤"),
        )
        builder.row(
            types.KeyboardButton(text="Рефералка"),
            types.KeyboardButton(text="Награда за победу")
        )
        builder.row(
            types.KeyboardButton(text="Играть⚔"),
        )
        return builder.as_markup(resize_keyboard=True)
