from abc import ABC, abstractmethod
from typing import Optional

import aiosqlite

from apps.users.schema import UserCreateSchema, UserModel, UserSchema, UserUpdateSchema


class IUserRepository(ABC):
    @abstractmethod
    async def create_table(
        self,
        db: aiosqlite.Connection,
    ):
        raise NotImplementedError

    @abstractmethod
    async def set_user_active(
        self,
        user_id: int,
        db: aiosqlite.Connection,
    ):
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_email(
        self,
        db: aiosqlite.Connection,
        email: str,
    ) -> Optional[UserModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_user(
        self,
        db: aiosqlite.Connection,
        user_id: int,
    ) -> Optional[UserModel]:
        raise NotImplementedError

    @abstractmethod
    async def create_user(
        self,
        db: aiosqlite.Connection,
        user_schema: UserCreateSchema,
    ) -> Optional[UserModel]:
        raise NotImplementedError

    @abstractmethod
    async def update_user(
        self,
        user_id: int,
        user_update: UserUpdateSchema,
        db: aiosqlite.Connection,
    ) -> Optional[UserModel]:
        raise NotImplementedError

    @abstractmethod
    async def delete_user(
        self,
        user_id: int,
        db: aiosqlite.Connection,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_users(
        self,
        db: aiosqlite.Connection,
    ) -> list[UserModel]:
        raise NotImplementedError
