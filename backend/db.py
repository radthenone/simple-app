import aiosqlite
from backend.config import BACKEND_DIR
from backend.apps.users.db import create_users_table
import os



async def init_db(connection: aiosqlite.Connection):
    await create_users_table(connection)

async def get_db() -> aiosqlite.Connection:
    database = os.path.join(BACKEND_DIR, "db.sqlite3")
    db = await aiosqlite.connect(database)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()
