from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def prem_keyboard():
    premium = InlineKeyboardBuilder()
    buttoms = [
        InlineKeyboardButton(text='🎁', url="https://t.me/premium")
    ]
    premium.add(*buttoms)
    return premium.as_markup(resize_keyboard=True)


def buy_keyboard():
    buy = InlineKeyboardBuilder()
    buttoms = [
        InlineKeyboardButton(text='Купить дополнительные жизни', callback_data=f'buy')
    ]
    buy.add(*buttoms)
    return buy.as_markup(resize_keyboard=True)


def manager_keyboard():
    manager = InlineKeyboardBuilder()
    buttoms = [
        InlineKeyboardButton(text='Написать менеджеру', url=f't.me/sirion2011')
    ]
    manager.add(*buttoms)
    return manager.as_markup(resize_keyboard=True)
