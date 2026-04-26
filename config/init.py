from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .const import BOT_TOKEN

bot = Bot(BOT_TOKEN, parse_mode='html')
dp = Dispatcher(storage=MemoryStorage())
