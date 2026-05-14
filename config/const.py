import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_URL = os.getenv("DB_URL")
_father_id_raw = os.getenv("FATHER_ID")
father_id = int(_father_id_raw) if _father_id_raw else None
sticker_id = os.getenv("STICKER_ID")