from aiogram.filters import Text
from aiogram import types, Router
from keyboards.inline.premium_link import prem_keyboard
import inspect
import logging


logger = logging.getLogger(__name__)
router = Router()


@router.message(Text("Награда за победу", ignore_case=True))
async def state_handler(message: types.Message):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    await message.answer(text=f'Когда вы победите Мистера Свин-бота,'
                              f' и пройдете пятый уровень сложности,'
                              f' Мистер Свин-бот, как честный игрок, подарит вам на ваш выбор'
                              f' Telegram Premium или любой подарок стоимостью до 1000 звезд',
                         reply_markup=prem_keyboard())
