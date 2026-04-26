from datetime import datetime, timezone
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db import User


async def profile_keyboard(user_id):
    user = await User.filter(tg_id=user_id).first()
    lives = user.lives
    elapsed_time = user.game_at.replace(tzinfo=timezone.utc)
    now_time = datetime.now().replace(tzinfo=timezone.utc)
    energy = ((now_time - elapsed_time).total_seconds()/3600) // 6

    keyboard = InlineKeyboardBuilder()
    lives_buttons = []
    for i in range(3):
        lives_buttons.append(InlineKeyboardButton(text="❤️", callback_data=f'profile_lives') if i < lives else
                             InlineKeyboardButton(text="🖤", callback_data=f'profile_lives'))
    keyboard.row(*lives_buttons)

    energy_buttons = []
    for i in range(4):
        energy_buttons.append(InlineKeyboardButton(text="⚡️", callback_data=f'profile_energy') if i < energy else
                             InlineKeyboardButton(text="✖️", callback_data=f'profile_energy'))
    keyboard.row(*energy_buttons)

    return keyboard.as_markup(resize_keybord=True)
