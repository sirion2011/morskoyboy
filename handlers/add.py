from datetime import datetime, timedelta
from aiogram.filters import Command, Text, or_f
from aiogram import types, Router
from config.const import father_id
from aiogram.fsm.context import FSMContext
from states.ad_state import Add
from config import bot
from keyboards.inline.ad_yes_no_keyboard import ad_keyboard, ad_keyboard2, make_keyboard, ad_keyboard3, timedelta_keyboard
from db import User
from help_functions.job_scheduler import ad_deleter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import ReplyKeyboardRemove
from keyboards.reply import main_menu


router = Router()


@router.message(Command('ad'))
async def state_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == father_id:
        await message.answer(text=f'Выберите время, на которое хотите запостить рекламу',
                             reply_markup=timedelta_keyboard())
        await state.set_state(Add.timedelta)


@router.message(or_f(Text(f'24 часа'),
                     Text(f'48 часов'),
                     Text(f'Навсегда')))
async def state_handler11(message: types.Message, state: FSMContext):

    if message.from_user.id == father_id:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Напишите мне цифрой сколько будет кнопок в сообщении',
                               reply_markup=ReplyKeyboardRemove())
        if message.text == f'24 часа':
            data = 24
        elif message.text == f'48 часов':
            data = 48
        else:
            data = 100
        await state.update_data(timedelta=data)
        await state.set_state(Add.amount_od_buttoms)


@router.message(Add.amount_od_buttoms)
async def state_handler21(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(text=f'Напишите количество кнопок цифрой')
        await state.set_state(Add.amount_od_buttoms)
    else:
        if int(message.text) == 0:
            await bot.send_message(chat_id=father_id,
                                   text=f'Отправьте мне сообщение которое вы хотите переслать')
            await state.update_data(name_and_link={}, user_id=message.from_user.id)
            await state.set_state(Add.get_forward_message)
        else:
            await state.update_data(buttoms=int(message.text), name_and_link={}, user_id=message.from_user.id)
            await message.answer(text=f'Пришлите ссылку которую будет содержать кнопка')
            await state.set_state(Add.get_link)


@router.message(Add.get_link)
async def state_handler32(message: types.Message, state: FSMContext):
    await state.update_data(link=message.text)
    await message.answer(text=f'Вот ваша ссылка: {message.text}\n'
                              f'Все верно?', reply_markup=ad_keyboard())
    await state.set_state(Add.yes_no)


@router.message(Add.yes_no)
async def state_handler41(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = message.text
    user_id = data["user_id"]
    if text == f'Нет 0':
        await bot.send_message(chat_id=user_id, text=f'Пришлите новую ссылку')
        await state.set_state(Add.get_link)
    elif text == f'Да 0':
        await bot.send_message(chat_id=user_id, text=f'Пришлите название для кнопки с ссылкой\n{data["link"]}')
        await state.set_state(Add.get_name)

    elif text == f'Нет 2':
        await bot.send_message(chat_id=user_id, text=f'Пришлите новое название')
        await state.set_state(Add.get_name)
    elif text == f'Да 2':
        buttom = data["buttoms"]
        if buttom == 1:
            await bot.send_message(chat_id=father_id,
                                   text=f'Отправьте мне сообщение которое вы хотите переслать')
            name_and_link = data["name_and_link"]
            name_and_link[data["name"]] = data["link"]
            await state.update_data(name_and_link=name_and_link)
            await state.set_state(Add.get_forward_message)
        else:
            name_and_link = data["name_and_link"]
            name_and_link[data["name"]] = data["link"]
            await state.update_data(buttoms=int(buttom - 1), name_and_link=name_and_link,
                                    name=f'', link=f'')
            await bot.send_message(chat_id=user_id, text=f'Пришлите ссылку которую будет содержать кнопка')
            await state.set_state(Add.get_link)


@router.message(Add.get_name)
async def state_handler51(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text=f'Вот ваше название кнопки: {message.text}\n'
                              f'Все верно?', reply_markup=ad_keyboard2())
    await state.set_state(Add.yes_no)


@router.message(Add.forward_message)
async def state_handler66(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id == father_id:
        await bot.send_message(chat_id=father_id,
                               text=f'Отправьте мне сообщение которое вы хотите переслать')
        await state.set_state(Add.get_forward_message)


@router.message(Add.get_forward_message)
async def state_handler31(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await bot.copy_message(chat_id=father_id, from_chat_id=father_id,
                               message_id=message.message_id, reply_markup=make_keyboard(data["name_and_link"]))
    except Exception as e:
        await bot.copy_message(chat_id=father_id, from_chat_id=father_id,
                               message_id=message.message_id)

    await message.answer(text=f'Рассылать рекламу по личным сообщениям?', reply_markup=ad_keyboard3())
    await state.update_data(message_id=message.message_id)
    await state.set_state(Add.final)


@router.message(Add.final)
async def state_handler_final(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data["user_id"]
    message_id = data["message_id"]
    dictic = data["name_and_link"]
    delta = int(data["timedelta"])
    text = message.text
    if text == f'Нет 3':
        await bot.send_message(chat_id=user_id, text=f'Сообщение удалено', reply_markup=main_menu.MainMenu.main_menu())
    else:
        users = await User.all()

        for user in users:
            if dictic:
                try:
                    ad = await bot.copy_message(chat_id=user.tg_id, from_chat_id=father_id,
                                                message_id=message_id,
                                                reply_markup=make_keyboard(dictic))
                    if delta in [24, 48]:
                        scheduler = AsyncIOScheduler()
                        scheduler.add_job(ad_deleter, 'date',
                                          run_date=datetime.now() + timedelta(hours=delta),
                                          args=[user.tg_id, ad.message_id, scheduler])
                        scheduler.start()
                except Exception as e:
                    pass

            else:
                try:
                    ad = await bot.copy_message(chat_id=user.tg_id, from_chat_id=father_id,
                                                message_id=message_id)
                    if delta in [24, 48]:
                        scheduler = AsyncIOScheduler()
                        scheduler.add_job(ad_deleter, 'date',
                                          run_date=datetime.now() + timedelta(hours=delta),
                                          args=[user.tg_id, ad.message_id, scheduler])
                        scheduler.start()
                except Exception as e:
                    pass

    await state.clear()
    await state.set_state(None)