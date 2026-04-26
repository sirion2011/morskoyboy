import asyncio
import datetime
import random
from help_functions.next_shoot import next_shoot, moove
from help_functions.field import field2
from db import User
from config.const import father_id, sticker_id
from aiogram.types import InlineKeyboardButton
from aiogram import types, Router
from config import bot
from help_functions.bokovye import bokkovye
from aiogram.fsm.context import FSMContext
from states.game import Play
from keyboards.reply.main_menu import MainMenu
from keyboards.reply.extra_lifes_keyboard import ExtraLiveKeyboard
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from help_functions.job_scheduler import del_text, energy_alert
import inspect
import logging


logger = logging.getLogger(__name__)

router = Router()

hod_bd = {}


@router.callback_query(lambda c: c.data and c.data.startswith('_'), Play.one)
async def player_callback(callback_query: types.CallbackQuery, state: FSMContext):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    logger.debug(f"Данные callback: {callback_query.data}")
    user_id = callback_query.from_user.id
    data = await state.get_data()
    player = data['player']
    bott = data['bott']
    player_bottons = data['player_bottons']
    bot_bottons = data['bot_bottons']
    player_sheep, bot_sheep = data['sheep_player'], data['sheep_bot']
    mesage = data['mesage']
    last_shoot = data["last_shoot"]
    user = await User.filter(tg_id=user_id).first()
    dificulity = user.dificulity
    try:
        hod_bd[user_id]
    except Exception as e:
        hod_bd[user_id] = 'player'
    if data['count_of_missed'] == -1:
        count_of_missed = []
    else:
        count_of_missed = data['count_of_missed']
    if data['shoots'] == -1:
        shoots = [i for i in range(1, 26)]
    else:
        shoots = data['shoots']
    if data['opa'] == -1:
        opa = [0]
    else:
        opa = data['opa']
    if data['tribtsh'] == 0:
        triplsh, dvaplsh, odinplsh = player_sheep[0:3], player_sheep[3:5], [player_sheep[5]]
        tribtsh, dvabtsh, odinbtsh = bot_sheep[0:3], bot_sheep[3:5], [bot_sheep[5]]
    else:
        triplsh, dvaplsh, odinplsh = data['triplsh'], data['dvaplsh'], data['odinplsh']
        tribtsh, dvabtsh, odinbtsh = data['tribtsh'], data['dvabtsh'], data['odinbtsh']

    triplsh2, dvaplsh2, odinplsh2 = player_sheep[0:3], player_sheep[3:5], [player_sheep[5]]
    tribtsh2, dvabtsh2, odinbtsh2 = bot_sheep[0:3], bot_sheep[3:5], [bot_sheep[5]]
    triplb, dvaplb, odinplb = bokkovye(triplsh2), bokkovye(dvaplsh2), bokkovye(odinplsh2)
    tribtb, dvabtb, odinbtb = bokkovye(tribtsh2), bokkovye(dvabtsh2), bokkovye(odinbtsh2)

    if hod_bd[user_id] == 'bot':
        await bot.answer_callback_query(callback_query.id, text=f'Сейчас ходит Мистер Свин-Бот\nДождитесь своего хода',
                                        show_alert=True)
    else:
        shoot = int(callback_query.data[-3]) if callback_query.data[-4] == '_' else int(
            str(callback_query.data[-4]) + str(callback_query.data[-3]))
        if callback_query.data.startswith(f'_player_'):
            if hod_bd[user_id] == 'player':
                await bot.answer_callback_query(callback_query.id, text=f'Это твое поле, ты не можешь его атаковать',
                                                show_alert=True)
        else:
            if shoot in (tribtsh + dvabtsh + odinbtsh) and len(tribtsh + dvabtsh + odinbtsh) == 1 and dificulity == 5:
                await bot.answer_callback_query(callback_query.id)
                index = bot_sheep.index(shoot)
                bokovye = []
                bokovye.append(dvabtb + odinbtb) if shoot in tribtsh else -1
                bokovye.append(tribtb + odinbtb) if shoot in dvabtsh else -1
                bokovye.append(dvabtb + tribtb) if shoot in odinbtsh else -1
                bot_sheep = moove(bot_sheep, shoot, shoots, bokovye)
                new_sheep = bot_sheep[index]
                tribtsh = bot_sheep[:3]
                dvabtsh = bot_sheep[3:5]
                odinbtsh = [bot_sheep[5]]
                last_shoot = ["last_shoot"]
                bot_bottons[shoot-1] = InlineKeyboardButton(text=f'💦', callback_data=f'_bot_{shoot}_💦')
                bot_bottons[new_sheep-1] = InlineKeyboardButton(text=f'💦', callback_data=f'_bot_{new_sheep}_❌')

                hod_bd[user_id] = 'bot'
                bot_bottons[int(shoot) - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_bot_{shoot}_✖')
                new_keyboard = field2(bot_bottons)
                await bot.edit_message_reply_markup(chat_id=user_id, message_id=bott.message_id,
                                                    reply_markup=new_keyboard)

                try:
                    mesage = await bot.edit_message_text(chat_id=user_id, message_id=mesage.message_id,
                                                         text=f'Ты промахнуся)\n'
                                                              f'Сейчас ход Великого Мистера Свин-Бота')
                except Exception as e:
                    pass
                try:
                    await bots_attack(user_id, player, player_bottons, triplsh, dvaplsh, odinplsh, triplb, dvaplb,
                                  odinplb, player_sheep, opa, shoots, count_of_missed, mesage, last_shoot)
                except Exception as e:
                    await state.clear()
                    await state.set_state(None)
                    pass

                if not (triplsh + dvaplsh + odinplsh):
                    await state.clear()
                    await state.set_state(None)
                    scheduler = AsyncIOScheduler()
                    scheduler.add_job(del_text, 'date',
                                      run_date=datetime.datetime.now() + datetime.timedelta(seconds=10),
                                      args=[user_id, [bott, player, mesage], scheduler])

                    scheduler.add_job(energy_alert, trigger='date',
                                      run_date=datetime.datetime.now() + datetime.timedelta(hours=24),
                                      args=[user_id, scheduler])
                    scheduler.start()
                    user = await User.filter(tg_id=user_id).first()
                    dificulity = user.dificulity
                    lives = int(user.lives) - 1
                    text = (f'Ты проиграл(\n Теперь ты снова возвращаетесь на уровень 1.\n'
                            f' Желаю удачи в будующих играх!') if int(user.lives == 0) else \
                        (f'Ты проиграл, но у тебя еще остались жизни чтобы попробовать снова,'
                         f' когда ваша энергия восполнится')
                    if lives == 0:
                        if user.extra_life <= 2:
                            await User.filter(tg_id=user_id).update(lives=3, dificulity=1,
                                                                    game_at=datetime.datetime.now())
                            await bot.send_message(chat_id=user_id, text=text, reply_markup=MainMenu.main_menu())
                            del hod_bd[user_id]

                        else:
                            await bot.send_message(chat_id=user_id,
                                                   text=f'У тебя достаточно дополнительных жизней,'
                                                        f' желаешь ли ты ими воспользоваться,'
                                                        f' чтобы не потерять игровой прогресс?',
                                                   reply_markup=ExtraLiveKeyboard.extra_live())

                    else:
                        del hod_bd[user_id]
                        await bot.send_message(chat_id=user_id, text=text, reply_markup=MainMenu.main_menu())
                        await User.filter(tg_id=user_id).update(lives=lives, game_at=datetime.datetime.now())

            if shoot in tribtsh or shoot in dvabtsh or shoot in odinbtsh:
                await bot.answer_callback_query(callback_query.id)
                if shoot in tribtsh:
                    tribtsh.remove(shoot)
                    if not tribtsh:
                        for i in tribtb:
                            bot_bottons[int(i - 1)] = InlineKeyboardButton(text=f'✖', callback_data=f'_bot_{i}_✖')
                elif shoot in dvabtsh:
                    dvabtsh.remove(shoot)
                    if not dvabtsh:
                        for i in dvabtb:
                            bot_bottons[int(i - 1)] = InlineKeyboardButton(text=f'✖', callback_data=f'_bot_{i}_✖')
                elif shoot in odinbtsh:
                    odinbtsh.remove(shoot)
                    if not odinbtsh:
                        for i in odinbtb:
                            bot_bottons[int(i - 1)] = InlineKeyboardButton(text=f'✖', callback_data=f'_bot_{i}_✖')

                hod_bd[user_id] = 'player'
                bot_bottons[int(shoot) - 1] = InlineKeyboardButton(text=f'❌', callback_data=f'_bot_{shoot}_❌')
                new_keyboard = field2(bot_bottons)
                await bot.edit_message_reply_markup(chat_id=user_id, message_id=bott.message_id,
                                                    reply_markup=new_keyboard)
                try:
                    mesage = await bot.edit_message_text(chat_id=user_id, message_id=mesage.message_id, text=f'Ты попал!\n'
                                                                                                         f'Ходи еще раз')
                except Exception as e:
                    pass
            else:
                if callback_query.data[-1] == '💦':
                    hod_bd[user_id] = 'bot'
                    await bot.answer_callback_query(callback_query.id)
                    bot_bottons[int(shoot) - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_bot_{shoot}_✖')
                    new_keyboard = field2(bot_bottons)
                    await bot.edit_message_reply_markup(chat_id=user_id, message_id=bott.message_id,
                                                        reply_markup=new_keyboard)

                    try:
                        mesage = await bot.edit_message_text(chat_id=user_id, message_id=mesage.message_id,
                                                         text=f'Ты промахнуся)\n'
                                                              f'Сейчас ход Великого Мистера Свин-Бота')
                    except Exception as e:
                        pass
                    try:
                        await bots_attack(user_id, player, player_bottons, triplsh, dvaplsh, odinplsh, triplb, dvaplb,
                                      odinplb, player_sheep, opa, shoots, count_of_missed, mesage, last_shoot)
                    except Exception as e:
                        await state.clear()
                        await state.set_state(None)
                        pass

                    if not (triplsh + dvaplsh + odinplsh):
                        await state.clear()
                        await state.set_state(None)
                        scheduler = AsyncIOScheduler()
                        scheduler.add_job(del_text, 'date',
                                          run_date=datetime.datetime.now() + datetime.timedelta(seconds=10),
                                          args=[user_id, [bott, player, mesage], scheduler])

                        scheduler.add_job(energy_alert, trigger='date',
                                          run_date=datetime.datetime.now() + datetime.timedelta(hours=24),
                                          args=[user_id, scheduler])
                        scheduler.start()
                        user = await User.filter(tg_id=user_id).first()
                        dificulity = user.dificulity
                        lives = int(user.lives) - 1
                        text = (f'Ты проиграл(\n Теперь ты снова возвращаетесь на уровень 1.\n'
                            f' Желаю удачи в будующих играх!') if int(user.lives == 0) else \
                        (f'Ты проиграл, но у тебя еще остались жизни чтобы попробовать снова,'
                         f' когда ваша энергия восполнится')
                        if lives == 0:
                            if user.extra_life <= 2:
                                await User.filter(tg_id=user_id).update(lives=3, dificulity=1, game_at=datetime.datetime.now())
                                await bot.send_message(chat_id=user_id, text=text, reply_markup=MainMenu.main_menu())
                                del hod_bd[user_id]

                            else:
                                await bot.send_message(chat_id=user_id,
                                                       text=f'У тебя достаточно дополнительных жизней,'
                                                            f' желаешь ли ты ими воспользоваться,'
                                                            f' чтобы не потерять игровой прогресс?',
                                                       reply_markup=ExtraLiveKeyboard.extra_live())

                        else:
                            del hod_bd[user_id]
                            await bot.send_message(chat_id=user_id, text=text, reply_markup=MainMenu.main_menu())
                            await User.filter(tg_id=user_id).update(lives=lives, game_at=datetime.datetime.now())

                elif callback_query.data[-1] == '✖' or (
                        callback_query.data[-1] == f'❌' and bot_bottons[shoot - 1].text == f'❌'):
                    hod_bd[user_id] = 'player'
                    await bot.answer_callback_query(callback_query.id, text=f'Ты уже проверял эту клеточку',
                                                    show_alert=True)

        if not (tribtsh + dvabtsh + odinbtsh):
            await bot.answer_callback_query(callback_query.id)
            user = await User.filter(tg_id=user_id).first()
            dificulity = user.dificulity

            if dificulity == 1:
                text = f'Неплохо для новичка!\n Ты уверенно прошел первый уровень, но это только начало, дальше я не буду так поддаваться)'
            elif dificulity == 2:
                text = f'Ух ты!\nВот тут конечно тебе сильно повезло, ну да ладно, победа есть победа... Увидимся на следующих уровнях)'
            elif dificulity == 3:
                text = f'Глазам своим не верю, как я так проигрываю? Надо бы подсобраться и больше не допускать таких ошибок'
            elif dificulity == 4:
                text = f'Да не может быть, чтобы меня кто то обыграл на четвертом уровне!!!\nЭто просто немыслимо, может мне пора на пенсию уже?'
            else:
                name = callback_query.from_user.username if callback_query.from_user.username else callback_query.from_user.first_name
                await bot.send_message(chat_id=father_id, text=f'Гвоздь мне в кеды!\nЭтот сопляк {name} смог обыграть меня и пройти 5 уровень')
                text = f'Это просто невозможно...\nЧтобы я, легендарный Мистер Свин-Бот, проигра какому то сопляку, просто немыслимо... Походу мне и правда пора заканчивать карьеру(\nА с тобой, везунчик, скоро свяжутся, жди свой приз и удачи)'
                dificulity = 0

            await bot.send_message(chat_id=user_id, text=text, reply_markup=MainMenu.main_menu())
            del hod_bd[user_id]
            await User.filter(tg_id=user_id).update(game_at=datetime.datetime.now(), dificulity=int(dificulity+1))
            await state.clear()
            await state.set_state(None)
            scheduler = AsyncIOScheduler()
            scheduler.add_job(del_text, 'date',
                              run_date=datetime.datetime.now() + datetime.timedelta(seconds=10),
                              args=[user_id, [bott, player, mesage], scheduler])
            scheduler.add_job(energy_alert, trigger='date',
                              run_date=datetime.datetime.now() + datetime.timedelta(hours=24),
                              args=[user_id, scheduler])
            scheduler.start()

    await state.update_data(player=player, bott=bott, player_bottons=player_bottons, bot_bottons=bot_bottons,
                            sheep_player=player_sheep, sheep_bot=bot_sheep, tribtsh=tribtsh, dvabtsh=dvabtsh,
                            odinbtsh=odinbtsh, triplsh=triplsh, dvaplsh=dvaplsh, odinplsh=odinplsh, opa=opa,
                            shoots=shoots, count_of_missed=count_of_missed, mesage=mesage, last_shoot=last_shoot)
    await state.set_state(Play.one)


async def bots_attack(user_id, player, player_bottons, triplsh, dvaplsh, odinplsh, triplb, dvaplb, odinplb,
                      player_sheep, opa, shoots, count_of_missed, mesage, last_shoot):
    logger.info(f"Файл: {__file__}, Функция: {inspect.currentframe().f_code.co_name}")
    prev_hod = opa[0]
    zaderzka = random.choice([2, 3, 4, 5])
    user = await User.filter(tg_id=user_id).first()
    dificulity = user.dificulity

    if dificulity == 1:
        smilik = await bot.send_sticker(chat_id=user_id, sticker=sticker_id)
        await asyncio.sleep(zaderzka)
        while True:
            new_keyboard = player
            if prev_hod != 0:
                shoot = next_shoot(prev_hod, player_sheep, dificulity, player_bottons)
            else:
                if len(count_of_missed) < 6:
                    shoot = random.choice(shoots)
                    while shoot in player_sheep:
                        shoot = random.choice(shoots)
                else:
                    shoot = random.choice(shoots)
                # shoot = random.choice(player_sheep)
            if shoot in triplsh:
                count_of_missed = []
                text = 'Мистер Свин-Бот попал в твой корабль\nОн продолжит атаковать'
                prev_hod = shoot
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot - 1}_✖')
                triplsh.remove(shoot)
                if not triplsh:
                    count_of_missed = []
                    prev_hod = 0
                    for i in triplb:
                        shoots.remove(i) if i in shoots else -1
                        player_bottons[int(i - 1)] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{i}_✖')
                new_keyboard = field2(player_bottons)
                break

            elif shoot in dvaplsh:
                count_of_missed = []
                text = 'Мистер Свин-Бот попал в твой корабль\nОн продолжит атаковать'
                prev_hod = shoot
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot - 1}_✖')
                dvaplsh.remove(shoot)
                if not dvaplsh:
                    count_of_missed = []
                    prev_hod = 0
                    for i in dvaplb:
                        shoots.remove(i) if i in shoots else -1
                        player_bottons[int(i - 1)] = InlineKeyboardButton(text='✖', callback_data=f'_player_{i}_✖')
                new_keyboard = field2(player_bottons)
                break

            elif shoot in odinplsh:
                count_of_missed = []
                text = 'Мистер Свин-Бот попал в твой корабль\nОн продолжит атаковать'
                prev_hod = shoot
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot - 1}_✖')
                odinplsh.remove(shoot)
                if not odinplsh:
                    count_of_missed = []
                    prev_hod = 0
                    for i in odinplb:
                        shoots.remove(i) if i in shoots else -1
                        player_bottons[int(i - 1)] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{i}_✖')
                new_keyboard = field2(player_bottons)
                break

            elif player_bottons[shoot - 1].callback_data[-1] == '💦':
                count_of_missed.append(shoot)
                text = 'Толстый Свин промахнулся\nТвоя очередь ходить'
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot}_✖')
                hod_bd[user_id] = 'player'
                new_keyboard = field2(player_bottons)
                break

            elif player_bottons[shoot - 1].text == f'✖':
                pass
        opa[0] = prev_hod
        shoots.remove(shoot)
        try:
            await bot.delete_message(chat_id=user_id, message_id=smilik.message_id)
            await bot.edit_message_reply_markup(chat_id=user_id, message_id=player.message_id,
                                            reply_markup=new_keyboard)
        except Exception as e:
            pass
        a = [i for i in player_sheep if i in shoots]
        if not (triplsh + dvaplsh + odinplsh) or a == []:
            hod_bd[user_id] = 'player'
        try:
            mesage = await bot.edit_message_text(chat_id=user_id, message_id=mesage.message_id, text=text)
        except Exception as e:
            pass
        if hod_bd[user_id] == 'bot':
            await bots_attack(user_id, player, player_bottons, triplsh, dvaplsh, odinplsh, triplb, dvaplb,
                              odinplb, player_sheep, opa, shoots, count_of_missed, mesage, last_shoot)

    elif dificulity == 2:
        smilik = await bot.send_sticker(chat_id=user_id, sticker=sticker_id)
        await asyncio.sleep(zaderzka)

        while True:
            new_keyboard = player
            if prev_hod != 0:
                shoot = next_shoot(prev_hod, player_sheep, dificulity, player_bottons)
            else:
                step = random.choice([3, 3, 4, 4, 4, 4, 4, 4, 4])
                if len(count_of_missed) == step or len(count_of_missed) == 5:
                    shoot = random.choice(player_sheep)
                else:
                    shoot = random.choice(shoots)
                    # shoot = random.choice(player_sheep)

            if shoot in triplsh:
                count_of_missed = []
                text = 'Мистер Свин-Бот попал в твой корабль\nОн продолжит атаковать'
                prev_hod = shoot
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot - 1}_✖')
                triplsh.remove(shoot)
                if not triplsh:
                    prev_hod = 0
                    for i in triplb:
                        shoots.remove(i) if i in shoots else -1
                        player_bottons[int(i - 1)] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{i}_✖')
                new_keyboard = field2(player_bottons)
                break

            elif shoot in dvaplsh:
                count_of_missed = []
                text = 'Мистер Свин-Бот попал в твой корабль\nОн продолжит атаковать'
                prev_hod = shoot
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot - 1}_✖')
                dvaplsh.remove(shoot)
                if not dvaplsh:
                    prev_hod = 0
                    for i in dvaplb:
                        shoots.remove(i) if i in shoots else -1
                        player_bottons[int(i - 1)] = InlineKeyboardButton(text='✖', callback_data=f'_player_{i}_✖')
                new_keyboard = field2(player_bottons)
                break

            elif shoot in odinplsh:
                count_of_missed = []
                text = 'Мистер Свин-Бот попал в твой корабль\nОн продолжит атаковать'
                prev_hod = shoot
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot - 1}_✖')
                odinplsh.remove(shoot)
                if not odinplsh:
                    prev_hod = 0
                    for i in odinplb:
                        shoots.remove(i) if i in shoots else -1
                        player_bottons[int(i - 1)] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{i}_✖')
                new_keyboard = field2(player_bottons)
                break

            elif player_bottons[shoot - 1].callback_data[-1] == '💦':
                count_of_missed.append(shoot)
                text = 'Толстый Свин промахнулся\nТвоя очередь ходить'
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot}_✖')
                hod_bd[user_id] = 'player'
                new_keyboard = field2(player_bottons)
                break

            elif player_bottons[shoot - 1].text == f'✖':
                pass
        opa[0] = prev_hod
        shoots.remove(shoot)
        try:
            await bot.delete_message(chat_id=user_id, message_id=smilik.message_id)
            await bot.edit_message_reply_markup(chat_id=user_id, message_id=player.message_id,
                                            reply_markup=new_keyboard)
        except Exception as e:
            pass

        a = [i for i in player_sheep if i in shoots]
        if not (triplsh + dvaplsh + odinplsh) or a == []:
            hod_bd[user_id] = 'player'
        try:
            mesage = await bot.edit_message_text(chat_id=user_id, message_id=mesage.message_id, text=text)
        except Exception as e:
            pass
        if hod_bd[user_id] == 'bot':
            await bots_attack(user_id, player, player_bottons, triplsh, dvaplsh, odinplsh, triplb, dvaplb,
                              odinplb, player_sheep, opa, shoots, count_of_missed, mesage, last_shoot)

    elif dificulity == 3:

        smilik = await bot.send_sticker(chat_id=user_id, sticker=sticker_id)
        await asyncio.sleep(zaderzka)

        while True:
            new_keyboard = player
            if prev_hod != 0:
                shoot = next_shoot(prev_hod, player_sheep, dificulity, player_bottons)
            else:
                step = random.choice([2, 2, 2, 2, 3, 3, 3, 3, 3])
                if len(count_of_missed) == step or len(count_of_missed) == 4:
                    shoot = random.choice(player_sheep)
                else:
                    shoot = random.choice(shoots)
                    # shoot = random.choice(player_sheep)
            if shoot in triplsh:
                count_of_missed = []
                text = 'Мистер Свин-Бот попал в твой корабль\nОн продолжит атаковать'
                prev_hod = shoot
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot - 1}_✖')
                triplsh.remove(shoot)
                if not triplsh:
                    count_of_missed = []
                    prev_hod = 0
                    for i in triplb:
                        shoots.remove(i) if i in shoots else -1
                        player_bottons[int(i - 1)] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{i}_✖')
                new_keyboard = field2(player_bottons)
                break

            elif shoot in dvaplsh:
                count_of_missed = []
                text = 'Мистер Свин-Бот попал в твой корабль\nОн продолжит атаковать'
                prev_hod = shoot
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot - 1}_✖')
                dvaplsh.remove(shoot)
                if not dvaplsh:
                    count_of_missed = []
                    prev_hod = 0
                    for i in dvaplb:
                        shoots.remove(i) if i in shoots else -1
                        player_bottons[int(i - 1)] = InlineKeyboardButton(text='✖', callback_data=f'_player_{i}_✖')
                new_keyboard = field2(player_bottons)
                break

            elif shoot in odinplsh:
                count_of_missed = []
                text = 'Мистер Свин-Бот попал в твой корабль\nОн продолжит атаковать'
                prev_hod = shoot
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot - 1}_✖')
                odinplsh.remove(shoot)
                if not odinplsh:
                    count_of_missed = []
                    prev_hod = 0
                    for i in odinplb:
                        shoots.remove(i) if i in shoots else -1
                        player_bottons[int(i - 1)] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{i}_✖')
                new_keyboard = field2(player_bottons)
                break

            elif player_bottons[shoot - 1].callback_data[-1] == '💦':
                count_of_missed.append(shoot)
                text = 'Толстый Свин промахнулся\nТвоя очередь ходить'
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot}_✖')
                hod_bd[user_id] = 'player'
                new_keyboard = field2(player_bottons)
                break

            elif player_bottons[shoot - 1].text == f'✖':
                pass
        opa[0] = prev_hod
        shoots.remove(shoot)
        try:
            await bot.delete_message(chat_id=user_id, message_id=smilik.message_id)
            await bot.edit_message_reply_markup(chat_id=user_id, message_id=player.message_id,
                                            reply_markup=new_keyboard)
        except Exception as e:
            pass
        a = [i for i in player_sheep if i in shoots]
        if not (triplsh + dvaplsh + odinplsh) or a == []:
            hod_bd[user_id] = 'player'

        try:
            mesage = await bot.edit_message_text(chat_id=user_id, message_id=mesage.message_id, text=text)
        except Exception as e:
            pass

        if hod_bd[user_id] == 'bot':
            await bots_attack(user_id, player, player_bottons, triplsh, dvaplsh, odinplsh, triplb, dvaplb,
                              odinplb, player_sheep, opa, shoots, count_of_missed, mesage, last_shoot)

    elif dificulity == 4:

        smilik = await bot.send_sticker(chat_id=user_id, sticker=sticker_id)
        await asyncio.sleep(zaderzka)

        while True:
            new_keyboard = player
            if prev_hod != 0:
                shoot = next_shoot(prev_hod, player_sheep, dificulity, player_bottons)
            else:
                step = random.choice([1, 1, 1, 1, 2, 2, 2, 2, 2])
                if len(count_of_missed) == step or len(count_of_missed) == 3:
                    shoot = random.choice(player_sheep)
                else:
                    shoot = random.choice(shoots)
                    # shoot = random.choice(player_sheep)

            if shoot in triplsh:
                count_of_missed = []
                text = 'Мистер Свин-Бот попал в твой корабль\nОн продолжит атаковать'
                prev_hod = shoot
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot - 1}_✖')
                triplsh.remove(shoot)
                if not triplsh:
                    count_of_missed = []
                    prev_hod = 0
                    for i in triplb:
                        shoots.remove(i) if i in shoots else -1
                        player_bottons[int(i - 1)] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{i}_✖')
                new_keyboard = field2(player_bottons)
                break

            elif shoot in dvaplsh:
                count_of_missed = []
                text = 'Мистер Свин-Бот попал в твой корабль\nОн продолжит атаковать'
                prev_hod = shoot
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot - 1}_✖')
                dvaplsh.remove(shoot)
                if not dvaplsh:
                    count_of_missed = []
                    prev_hod = 0
                    for i in dvaplb:
                        shoots.remove(i) if i in shoots else -1
                        player_bottons[int(i - 1)] = InlineKeyboardButton(text='✖', callback_data=f'_player_{i}_✖')
                new_keyboard = field2(player_bottons)
                break

            elif shoot in odinplsh:
                count_of_missed = []
                text = 'Мистер Свин-Бот попал в твой корабль\nОн продолжит атаковать'
                prev_hod = shoot
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot - 1}_✖')
                odinplsh.remove(shoot)
                if not odinplsh:
                    count_of_missed = []
                    prev_hod = 0
                    for i in odinplb:
                        shoots.remove(i) if i in shoots else -1
                        player_bottons[int(i - 1)] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{i}_✖')
                new_keyboard = field2(player_bottons)
                break

            elif player_bottons[shoot - 1].callback_data[-1] == '💦':
                count_of_missed.append(shoot)
                text = 'Толстый Свин промахнулся\nТвоя очередь ходить'
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot}_✖')
                hod_bd[user_id] = 'player'
                new_keyboard = field2(player_bottons)
                break

            elif player_bottons[shoot - 1].text == f'✖':
                pass
        opa[0] = prev_hod
        shoots.remove(shoot)
        try:
            await bot.delete_message(chat_id=user_id, message_id=smilik.message_id)
            await bot.edit_message_reply_markup(chat_id=user_id, message_id=player.message_id,
                                            reply_markup=new_keyboard)
        except Exception as e:
            pass
        a = [i for i in player_sheep if i in shoots]
        if not (triplsh + dvaplsh + odinplsh) or a == []:
            hod_bd[user_id] = 'player'

        try:
            mesage = await bot.edit_message_text(chat_id=user_id, message_id=mesage.message_id, text=text)
        except Exception as e:
            pass

        if hod_bd[user_id] == 'bot':
            await bots_attack(user_id, player, player_bottons, triplsh, dvaplsh, odinplsh, triplb, dvaplb,
                              odinplb, player_sheep, opa, shoots, count_of_missed, mesage, last_shoot)

    elif dificulity == 5:

        smilik = await bot.send_sticker(chat_id=user_id, sticker=sticker_id)
        await asyncio.sleep(zaderzka)
        while True:
            new_keyboard = player
            if prev_hod != 0:
                shoot = next_shoot(prev_hod, player_sheep, dificulity, player_bottons)
                if last_shoot == ["last_shoot"]:
                    shoot = random.choice(player_sheep)
                #дописать чтобы в нужный момент стреляло исключительно по кораблю
            else:
                step = random.choice([0, 1, 1, 1, 1, 1, 1, 1, 1])
                if len(count_of_missed) == step or len(count_of_missed) == 2:
                    shoot = random.choice(player_sheep)
                else:
                    shoot = random.choice(shoots)
                    if last_shoot == ["last_shoot"]:
                        shoot = random.choice(player_sheep)
                    #shoot = random.choice(player_sheep)

            if shoot in triplsh:
                count_of_missed = []
                text = 'Мистер Свин-Бот попал в твой корабль\nОн продолжит атаковать'
                prev_hod = shoot
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot - 1}_✖')
                triplsh.remove(shoot)
                if not triplsh:
                    count_of_missed = []
                    prev_hod = 0
                    for i in triplb:
                        shoots.remove(i) if i in shoots else -1
                        player_bottons[int(i - 1)] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{i}_✖')
                new_keyboard = field2(player_bottons)
                break

            elif shoot in dvaplsh:
                count_of_missed = []
                text = 'Мистер Свин-Бот попал в твой корабль\nОн продолжит атаковать'
                prev_hod = shoot
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot - 1}_✖')
                dvaplsh.remove(shoot)
                if not dvaplsh:
                    count_of_missed = []
                    prev_hod = 0
                    for i in dvaplb:
                        shoots.remove(i) if i in shoots else -1
                        player_bottons[int(i - 1)] = InlineKeyboardButton(text='✖', callback_data=f'_player_{i}_✖')
                new_keyboard = field2(player_bottons)
                break

            elif shoot in odinplsh:
                count_of_missed = []
                text = 'Мистер Свин-Бот попал в твой корабль\nОн продолжит атаковать'
                prev_hod = shoot
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot - 1}_✖')
                odinplsh.remove(shoot)
                if not odinplsh:
                    count_of_missed = []
                    prev_hod = 0
                    for i in odinplb:
                        shoots.remove(i) if i in shoots else -1
                        player_bottons[int(i - 1)] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{i}_✖')
                new_keyboard = field2(player_bottons)
                break

            elif player_bottons[shoot - 1].callback_data[-1] == '💦':
                count_of_missed.append(shoot)
                text = 'Толстый Свин промахнулся\nТвоя очередь ходить'
                player_bottons[shoot - 1] = InlineKeyboardButton(text=f'✖', callback_data=f'_player_{shoot}_✖')
                hod_bd[user_id] = 'player'
                new_keyboard = field2(player_bottons)
                break

            elif player_bottons[shoot - 1].text == f'✖':
                pass
        opa[0] = prev_hod
        shoots.remove(shoot)
        try:
            await bot.delete_message(chat_id=user_id, message_id=smilik.message_id)
            await bot.edit_message_reply_markup(chat_id=user_id, message_id=player.message_id,
                                            reply_markup=new_keyboard)
        except Exception as e:
            pass
        a = [i for i in player_sheep if i in shoots]
        if not (triplsh + dvaplsh + odinplsh) or a == []:
            hod_bd[user_id] = 'player'
        try:
            mesage = await bot.edit_message_text(chat_id=user_id, message_id=mesage.message_id, text=text)
        except Exception as e:
            pass

        if hod_bd[user_id] == 'bot':
            await bots_attack(user_id, player, player_bottons, triplsh, dvaplsh, odinplsh, triplb, dvaplb,
                              odinplb, player_sheep, opa, shoots, count_of_missed, mesage, last_shoot)
