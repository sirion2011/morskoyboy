from aiogram.filters import Command
from aiogram import types, Router
from config.const import father_id
from aiogram.fsm.context import FSMContext
from states.admin_state import Present
from keyboards.reply.main_menu import MainMenu
from db import User


router = Router()


@router.message(Command(f'present'))
async def state_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == father_id:
        await message.answer(f'Напишите мне username пользователя, который покупает 3 жизни')
        await state.set_state(Present.username)


@router.message(Present.username)
async def state_handler2(message: types.Message, state: FSMContext):
    if message.from_user.id == father_id:
        if message.text.startswith(f'@'):
            user = await User.filter(username=f'{message.text[1:]}').first()
            if not user:
                await message.answer(text=f'Пользователь {message.text} не найден в базе данных')
                await state.set_state(Present.username)
                return

            await message.answer(text=f'Игрок {message.text} получил 3 дополнительные жизни',
                                 reply_markup=MainMenu.main_menu())
            extra_lifes = int(user.extra_life) + 3
            await User.filter(username=f'{message.text[1:]}').update(extra_life=extra_lifes)
            await state.clear()
            await state.set_state(None)

        else:
            await message.answer(text=f'Напишиете пожалуйста правильный username, пример: @sirion2011')
            await state.set_state(Present.username)


@router.message(Command("count"))
async def state_handler3(message: types.Message):
    if message.from_user.id == father_id:
        count = await User.all().count()
        await message.answer(text=f'На данный момент Мистер Свин-Бот насчитывает {int(count)} пользователей')