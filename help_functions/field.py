from help_functions.final_place import final_place
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
import inspect
import logging


logger = logging.getLogger(__name__)


def field(whose: str):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    field = {i: str(i) for i in range(1, 26)}
    longness = 4
    tryes = 0
    ship_count = 0
    SHEEP = []
    final_place(field, tryes, ship_count, SHEEP)
    for voda in field.keys():
        if field[voda].isdigit():
            field[voda] = f'💦'
    main_keyboard = InlineKeyboardBuilder()
    bottons = []
    if whose == 'bot':
        for i in range(1, 26):
            bottons.append(InlineKeyboardButton(text=f'💦', callback_data=f'_bot_{i}_{field[i]}'))
    else:
        for i in range(1, 26):
            bottons.append(InlineKeyboardButton(text=field[i], callback_data=f'_player_{i}_{field[i]}'))

    for i in range(0, 25, 5):
        main_keyboard.row(*bottons[i:i+5])

    main_keyboard = main_keyboard.as_markup()

    return main_keyboard, SHEEP, bottons


def field2(bottons: list):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    main_keyboard = InlineKeyboardBuilder()
    for i in range(0, 25, 5):
        main_keyboard.row(*bottons[i:i+5])

    main_keyboard = main_keyboard.as_markup()

    return main_keyboard
