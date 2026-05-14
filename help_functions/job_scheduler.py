from config import bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def del_text(user_id, list_of_messages, scheduler: AsyncIOScheduler):
    try:
        for message in list_of_messages:
            await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    except Exception as e:
        scheduler.shutdown(wait=False)


async def energy_alert(user_id, scheduler: AsyncIOScheduler):
    try:
        await bot.send_message(chat_id=user_id, text=f'Ваша энергия поностью восстановилась,'
                                                     f' самое время бросить вызов Мистер Свин-боту)')
    except Exception as e:
        scheduler.shutdown(wait=False)


async def ad_deleter(user_id, message_id, scheduler: AsyncIOScheduler):
    try:
        await bot.delete_message(chat_id=user_id, message_id=message_id)
    except Exception as e:
        scheduler.shutdown(wait=False)