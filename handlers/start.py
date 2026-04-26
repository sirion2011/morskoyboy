from aiogram.filters import Command
from aiogram import types, Router
from db.models import User
from keyboards.reply.main_menu import MainMenu
from config import bot
from keyboards.inline.referral_keyboard import ref_keyboard

import inspect
import logging


logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("start", ignore_case=True))
async def state_handler(message: types.Message):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    existing_user = await User.filter(tg_id=message.from_user.id).first()
    if not existing_user:
        if message.text != '/start':
            referral_id = int(message.text[7:])
            await User.create(
                tg_id=message.from_user.id,
                name=message.from_user.first_name,
                username=message.from_user.username,
                referral_id=referral_id,
                hod=f'j',
                game_at=f'2023-10-31 23:19:11.358533'
            )
            name = f'@{message.from_user.username if message.from_user.username else message.from_user.first_name}'
            await bot.send_message(chat_id=referral_id,
                                   text=f'Ты получаешь дополнительную жизнь за своего друга {name}',
                                   reply_markup=ref_keyboard())
            user = await User.filter(tg_id=referral_id).first()
            extra_life = int(user.extra_life)
            await User.filter(tg_id=referral_id).update(extra_life=extra_life+1)
        else:
            await User.create(
                tg_id=message.from_user.id,
                name=message.from_user.first_name,
                username=message.from_user.username,
                hod=f'j',
                game_at=f'2023-10-31 23:19:11.358533'
            )
    await message.answer(f'Тебя приветствует Мистер Свин-бот!\n'
                         f'Это первый телеграмм бот, который раздает телеграмм премиум за игру,'
                         f' все что тебе для этого надо, это пройти пятый уровень сложности в игре морской бой.\n'
                         f'Всего у тебя будет три жизни, и при поражении боту, ты будешь терять одну жизнь.'
                         f' А в случае пройгрыша, будешь начинать сначала!\n'
                         f'Однако ты также можешь докупать жизни, получать дополнительные жизни'
                         f' за приглашенных друзей и получать подарки в виде жизней\n\n'
                         f'Желаю тебе веселой игры!',
                         reply_markup=MainMenu.main_menu())

    #await User.filter(tg_id=message.from_user.id).update(lives=1, extra_life=3, game_at=f'2023-10-31 23:19:11.358533')
