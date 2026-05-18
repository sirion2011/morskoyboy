from datetime import datetime
from aiogram import types, Router
from db import User

from keyboards.reply.main_menu import MainMenu
from aiogram.filters import Text, or_f
import inspect
import logging


logger = logging.getLogger(__name__)
router = Router()


@router.message(or_f(
    Text('Давай конечно'),
            Text('Нет, спасибо')
))
async def state_handler(message: types.Message):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    user = await User.filter(tg_id=message.from_user.id).first()
    user_id = message.from_user.id
    text = message.text

    if text == 'Нет, спасибо':
        text = (f'Вы не захотели воспользоваться дополнительными жизнями,'
                ' поэтому теперь возвращаетесь на первый уровень\n'
                'Удачи в будущих играх)')
        await message.answer(text=text, reply_markup=MainMenu.main_menu())
        await User.filter(tg_id=user_id).update(lives=3, dificulity=1, game_at=datetime.now())

    else:
        extra_lives = int(user.extra_life)
        dificulity = int(user.dificulity)
        text = f'Вы использовали одну дополнительную жизнь, поэтому остаётесь на уровне: {dificulity}'
        await message.answer(text=text, reply_markup=MainMenu.main_menu())
        await User.filter(tg_id=user_id).update(
            lives=1,
            extra_life=extra_lives - 1,
            game_at=datetime.now()
        )
