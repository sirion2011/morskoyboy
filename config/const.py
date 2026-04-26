import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_URL = os.getenv("DB_URL")
father_id = os.getenv("FATHER_ID")
sticker_id = os.getenv("STICKER_ID")
