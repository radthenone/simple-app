import os
from typing import Optional


from backend.apps.users.schema import User
import aiosqlite
import logging

logger = logging.getLogger('mycoolapp')

async def create_users_table(connection: aiosqlite.Connection, table_name: str = 'users'):
    async with connection.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';") as cursor:
        if await cursor.fetchone() is None:
            schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
            async with connection:
                with open(schema_path, 'r') as f:
                    await connection.executescript(f.read())
            print("Table 'users' created.")
        else:
            print("Table 'users' already exists.")

async def get_user(connection: aiosqlite.Connection, user_id: int) -> Optional[User]:
    async with connection.execute("SELECT * FROM users WHERE id = ?", (user_id,)) as cursor:
        user = await cursor.fetchone()
        if user:
            return User(**user)

        return None


async def create_user(connection: aiosqlite.Connection, user_schema: User) -> Optional[User]:
    try:
        await connection.execute("""
            INSERT INTO users (username, password, email, is_active, is_admin, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_schema.username,
            user_schema.password,
            user_schema.email,
            user_schema.is_active,
            user_schema.is_admin,
            user_schema.created_at
        ))

        await connection.commit()

        async with connection.execute("SELECT last_insert_rowid()") as cursor:
            user_id_row = await cursor.fetchone()
            if user_id_row is None:
                logging.error("Failed to retrieve last inserted user ID.")
                return None

            user_id = user_id_row[0]

            return await get_user(connection, user_id)

    except Exception as e:
        logging.error(f"Error creating user: {e}")
        return None


async def exists_user(connection: aiosqlite.Connection, user_email: str) -> bool:
    async with connection.execute("SELECT * FROM users WHERE email = ?", (user_email,)) as cursor:
        user = await cursor.fetchone()
        return user is not None