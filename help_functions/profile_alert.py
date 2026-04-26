from aiogram import types, Router
from config import bot
import inspect
import logging


logger = logging.getLogger(__name__)


router = Router()


@router.callback_query(lambda c: c.data and c.data == 'profile_lives')
async def player_callback(callback_query: types.CallbackQuery):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    logger.debug(f"Данные callback: {callback_query.data}")
    await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'Это все твои оставшиеся жизни',
                                    show_alert=True)


@router.callback_query(lambda c: c.data and c.data == 'profile_energy')
async def player_callback(callback_query: types.CallbackQuery):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    logger.debug(f"Данные callback: {callback_query.data}")
    await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'Это твоя энергия\n'
                                                                              f'Если все 4 энергии заряжены,'
                                                                              f' значит ты можешь играть',
                                    show_alert=True)


@router.callback_query(lambda c: c.data and c.data == 'extra_life_info')
async def player_callback(callback_query: types.CallbackQuery):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    logger.debug(f"Данные callback: {callback_query.data}")
    await bot.answer_callback_query(callback_query_id=callback_query.id,
                                    text=f'Теперь когда у вас закончатся жизни вы'
                                         f' сможете использовать эту чтобы продолжить игру',
                                    show_alert=True)
