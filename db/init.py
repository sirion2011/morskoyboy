from tortoise import Tortoise

from config import DB_URL

db = Tortoise()


async def init():
    await db.init(
        db_url=DB_URL,
        modules={
            'models':
                [
                    'db.models'
                ]
        }
    )

    await Tortoise.generate_schemas(safe=True)


async def on_shutdown():
    await db.close_connections()
