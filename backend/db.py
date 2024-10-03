import os

import aiosqlite

from apps.users.repository import UserRepository
from config import settings


async def init_db(connection: aiosqlite.Connection):
    repository = UserRepository()
    await repository.create_table(db=connection)


async def get_db() -> aiosqlite.Connection:
    database = os.path.join(settings.BACKEND_DIR, "db.sqlite3")
    db = await aiosqlite.connect(database)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()
