from aiogram.filters import Text
from aiogram import types, Router
from keyboards.inline.premium_link import buy_keyboard, manager_keyboard
from config.init import bot
import inspect
import logging


logger = logging.getLogger(__name__)
router = Router()


@router.message(Text("Рефералка", ignore_case=True))
async def state_handler(message: types.Message):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    text_lor = (f'За каждого приглашенного друга, вы будете получать дополнительную жизнь.'
                f' Если вы соберете 3 дополнительные жизни, сможете возродиться, когда у вас закончатся настоящие жизни!')
    link = f'https://t.me/morskoyboy_bbot?start={message.from_user.id}'
    await message.answer(f'{text_lor}\n\nВаша реферальная ссылка: {link}', reply_markup=buy_keyboard())


@router.callback_query()
async def state_nahdler(callback_query: types.CallbackQuery):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    logger.debug(f"Данные callback: {callback_query.data}")
    if callback_query.data == f'buy':
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f'Вы можете купить дополнительные жизни за деньги\n'
                                    f'3 дополнительные жизни - 1$\n\n'
                                    f'Если вы хотите приобрести, свяжитесь с менеджером',
                               reply_markup=manager_keyboard())
