from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def ad_keyboard():
    add = ReplyKeyboardBuilder()
    buttoms = [
        KeyboardButton(text='Да 0'),
        KeyboardButton(text=f'Нет 0')
    ]
    add.add(*buttoms)
    return add.as_markup(resize_keyboard=True)


def ad_keyboard2():
    add = ReplyKeyboardBuilder()
    buttoms = [
        KeyboardButton(text='Да 2'),
        KeyboardButton(text=f'Нет 2')
    ]
    add.add(*buttoms)
    return add.as_markup(resize_keyboard=True)


def make_keyboard(dictic):
    make = InlineKeyboardBuilder()
    buttoms = [InlineKeyboardButton(text=str(name), url=str(link)) for name, link in dictic.items()]
    make.add(*buttoms)
    return make.as_markup(resize_keyboard=True, row_width=2)


def ad_keyboard3():
    add = ReplyKeyboardBuilder()
    buttoms = [
        KeyboardButton(text='Да 3'),
        KeyboardButton(text=f'Нет 3')
    ]
    add.add(*buttoms)
    return add.as_markup(resize_keyboard=True)


def timedelta_keyboard():
    time = ReplyKeyboardBuilder()
    buttoms = [
        KeyboardButton(text='24 часа'),
        KeyboardButton(text=f'48 часов'),
        KeyboardButton(text=f'Навсегда'),
    ]
    time.add(*buttoms)
    return time.as_markup(resize_keyboard=True, row_width=2)
