import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from help_functions.job_scheduler import del_text
from keyboards.reply.main_menu import MainMenu
from aiogram.filters import Text, or_f
from aiogram.types import ReplyKeyboardRemove
from aiogram import types, Router
from db import User
from aiogram.fsm.context import FSMContext
from states.game import Play
from help_functions.field import field
from datetime import datetime, timezone, timedelta

import inspect
import logging


logger = logging.getLogger(__name__)
router = Router()


@router.message(or_f(Text("Играть⚔"), Text('/game')))
async def state_handler(message: types.Message, state: FSMContext):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    user = await User.filter(tg_id=message.from_user.id).first()
    elapsed_time = user.game_at.replace(tzinfo=timezone.utc)
    now_time = datetime.now().replace(tzinfo=timezone.utc)
    proshedshee = now_time - elapsed_time
    hour = (timedelta(hours=24)-proshedshee).total_seconds()//3600
    minute = ((timedelta(hours=24)-proshedshee).total_seconds() - int(hour)*3600)//60

    if proshedshee < timedelta(hours=24):
        await message.answer(text=f'У вас недостаточно энергии. Вы сможете сыграть через:\n'
                                  f'Часы: {int(hour)}\n'
                                  f'Минуты: {int(minute)}\n\n'
                                  f'Я уведомлю вас когда энергия восполнится')
    else:
        mesage = await message.answer(f'Удачной игры!',
                                      reply_markup=ReplyKeyboardRemove())

        scheduler = AsyncIOScheduler()
        scheduler.add_job(del_text, 'date',
                          run_date=datetime.now() + timedelta(seconds=5),
                          args=[message.from_user.id, [mesage], scheduler])
        scheduler.start()

        bot_field, sheep_bot, bot_bottons = field('bot')
        player_field, sheep_player, player_bottons = field('player')

        player = await message.answer(text='Вот ваше игровое поле',
                                      reply_markup=player_field)
        bott = await message.answer(text='Вот поле Мистера Свин-Бота',
                                    reply_markup=bot_field
                                    )
        # await User.filter(tg_id=message.from_user.id).update(dificulity=int(message.text))

        mesage = await message.answer(text=f'Мистер Свин-Бот, любезно дает вам право начать игру, атакуйте!')

        triplsh, dvaplsh, odinplsh = 0, 0, 0
        tribtsh, dvabtsh, odinbtsh = 0, 0, 0
        opa = -1
        shoots = -1
        count_of_missed = -1
        await state.set_state(Play.one)
        await state.update_data(player=player, bott=bott, player_bottons=player_bottons, bot_bottons=bot_bottons,
                                sheep_player=sheep_player, sheep_bot=sheep_bot, tribtsh=tribtsh, dvabtsh=dvabtsh,
                                odinbtsh=odinbtsh, triplsh=triplsh, dvaplsh=dvaplsh, odinplsh=odinplsh, opa=opa,
                                shoots=shoots, count_of_missed=count_of_missed, mesage=mesage, last_shoot=[])
