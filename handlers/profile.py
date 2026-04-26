from aiogram.filters import Text
from aiogram import types, Router
from db.models import User
from keyboards.inline.profile_keyboard import profile_keyboard
import inspect
import logging


logger = logging.getLogger(__name__)
router = Router()


@router.message(Text("Профиль👤", ignore_case=True))
async def state_handler(message: types.Message):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    user = await User.filter(tg_id=message.from_user.id).first()
    keyboard = await profile_keyboard(message.from_user.id)
    text = (f'Профиль👤\n\n'
            f'Уровень: {int(user.dificulity)}\n'
            f'Дополнительные жизни: {int(user.extra_life)}')
    await message.answer(text=text, reply_markup=keyboard)

