import logging
import os
from datetime import datetime
from typing import Optional

import aiosqlite

from apps.users.interface import IUserRepository
from apps.users.schema import UserCreateSchema, UserModel, UserUpdateSchema
from apps.users.utils import hash_password

logger = logging.getLogger("simple-debug")


class UserRepository(IUserRepository):
    def __init__(self, table_name: str = "users"):
        self.table_name = table_name

    @staticmethod
    async def get_last_user(
        db: aiosqlite.Connection,
    ) -> Optional[int]:
        async with db.execute("SELECT last_insert_rowid()") as cursor:
            user_id_row = await cursor.fetchone()
            if user_id_row is None:
                logging.error("Failed to retrieve last inserted user ID.")
                return None

            user_id = user_id_row[0]

            return user_id

    async def set_user_active(
        self,
        user_id: int,
        db: aiosqlite.Connection,
    ):
        await db.execute("UPDATE users SET is_active = 1 WHERE id = ?", (user_id,))
        await db.commit()

    async def create_table(
        self,
        db: aiosqlite.Connection,
    ):
        async with db.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}';"
        ) as cursor:
            if await cursor.fetchone() is None:
                schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
                async with db:
                    with open(schema_path, "r") as f:
                        await db.executescript(f.read())
                logger.info("Table 'users' created.")
            else:
                logger.info("Table 'users' already exists.")

    async def get_user_by_email(
        self,
        db: aiosqlite.Connection,
        email: str,
    ) -> Optional[UserModel]:
        async with db.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ) as cursor:
            user = await cursor.fetchone()
            if user:
                return UserModel(**user)

            return None

    async def get_user(
        self,
        db: aiosqlite.Connection,
        user_id: int,
    ) -> Optional[UserModel]:
        async with db.execute("SELECT * FROM users WHERE id = ?", (user_id,)) as cursor:
            user = await cursor.fetchone()
            if user:
                return UserModel(**user)

            return None

    async def create_user(
        self,
        db: aiosqlite.Connection,
        user_schema: UserCreateSchema,
    ) -> Optional[UserModel]:
        try:
            await db.execute(
                """
                INSERT INTO users (username, password, email, is_active, is_admin, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    user_schema.username,
                    hash_password(user_schema.password),
                    user_schema.email,
                    user_schema.is_active,
                    user_schema.is_admin,
                    user_schema.created_at,
                    user_schema.updated_at,
                ),
            )

            await db.commit()

            user_id = await self.get_last_user(db)

            return await self.get_user(db, user_id)

        except Exception as e:
            logging.error(f"Error creating user: {e}")
            return None

    async def update_user(
        self,
        user_id: int,
        user_update: UserUpdateSchema,
        db: aiosqlite.Connection,
    ) -> Optional[UserModel]:
        try:
            await db.execute(
                """
                UPDATE users
                SET username = ?, password = ?, email = ?, updated_at = ?
                WHERE id = ?
            """,
                (
                    user_update.username,
                    hash_password(user_update.password),
                    user_update.email,
                    user_update.updated_at,
                    user_id,
                ),
            )

            await db.commit()

            return await self.get_user(db, user_id)

        except Exception as e:
            logging.error(f"Error updating user: {e}")
            return None

    async def delete_user(
        self,
        user_id: int,
        db: aiosqlite.Connection,
    ) -> bool:
        try:
            await db.execute("DELETE FROM users WHERE id = ?", (user_id,))
            await db.commit()

            return True

        except Exception as e:
            logging.error(f"Error deleting user: {e}")
            return False

    async def get_users(
        self,
        db: aiosqlite.Connection,
    ) -> list[UserModel]:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return [UserModel(**user) for user in users]
