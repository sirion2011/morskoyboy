import asyncio
import logging
import os

from config import commands, bot, dp
from db import init, on_shutdown
from handlers import start, game, profile, referral, premium, add, admin
from help_functions import bot_hod, profile_alert, extralifestate


logging.basicConfig(level=logging.INFO)


async def main():
    dp.include_routers(
        game.router,
        start.router,
        bot_hod.router,
        profile.router,
        profile_alert.router,
        referral.router,
        extralifestate.router,
        premium.router,
        add.router,
        admin.router,
    )
    dp.shutdown.register(on_shutdown)
    dp.startup.register(init)
    await bot.set_my_commands(commands)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except Exception as e:
        logging.exception("Unexpected error occurred: %s", e)
    except KeyboardInterrupt:
        logging.info('Bot stopped by user')
    finally:
        loop.close()
        os._exit(0)

