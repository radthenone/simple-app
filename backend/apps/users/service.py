import logging
from typing import Optional

import aiosqlite
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from apps.users.interface import IUserRepository
from apps.users.schema import UserCreateSchema, UserModel, UserSchema, UserUpdateSchema

logger = logging.getLogger("simple-debug")


class UserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def is_user(
        self,
        db: aiosqlite.Connection,
        user_id: int,
    ) -> bool:
        user = await self.repository.get_user(db=db, user_id=user_id)
        if user:
            return True
        return False

    async def create_user(
        self,
        db: aiosqlite.Connection,
        user_schema: UserCreateSchema,
    ):
        try:
            user = await self.repository.create_user(db=db, user_schema=user_schema)
            if not user:
                raise HTTPException(status_code=400, detail="Failed to create user")
            return user

        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise HTTPException(status_code=400, detail="User already exists")

    async def get_user(
        self,
        db: aiosqlite.Connection,
        user_id: int,
    ) -> Optional[JSONResponse]:
        user = await self.repository.get_user(db=db, user_id=user_id)
        if user:
            return JSONResponse(
                content=UserSchema(
                    username=user.username,
                    email=user.email,
                    is_active=user.is_active,
                ).model_dump(),
                status_code=200,
            )

        raise HTTPException(status_code=404, detail="User not found")

    async def update_user(
        self,
        db: aiosqlite.Connection,
        user_id: int,
        user_update: UserUpdateSchema,
    ):
        user = await self.repository.update_user(
            db=db, user_id=user_id, user_update=user_update
        )
        if user:
            return JSONResponse(
                content=user.model_dump(),
                status_code=200,
            )

        raise HTTPException(status_code=404, detail="User not found")

    async def delete_user(
        self,
        db: aiosqlite.Connection,
        user_id: int,
    ):
        try:
            if await self.repository.delete_user(db=db, user_id=user_id):
                return JSONResponse(
                    content={"detail": "User deleted", "status_code": 201},
                    status_code=200,
                )

        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            raise HTTPException(status_code=404, detail="User not found")

    async def get_users(
        self,
        db: aiosqlite.Connection,
    ):
        users = await self.repository.get_users(db=db)
        if users:
            return JSONResponse(
                content=[
                    UserSchema(
                        username=user.username,
                        email=user.email,
                        is_active=user.is_active,
                    ).model_dump()
                    for user in users
                ],
                status_code=200,
            )

        raise HTTPException(status_code=404, detail="Users not found")
