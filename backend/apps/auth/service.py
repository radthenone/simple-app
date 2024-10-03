from typing import Optional

import aiosqlite
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from apps.auth.handler import (
    sign_jwt,
    verify_password,
)
from apps.auth.schema import LoginSchema, RegisterSchema
from apps.users.interface import IUserRepository
from apps.users.schema import UserCreateSchema, UserModel


class AuthService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    async def authenticate_user(
        self,
        db: aiosqlite.Connection,
        email: str,
        password: str,
    ) -> Optional[UserModel]:
        user = await self.repository.get_user_by_email(db=db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    async def login_user(
        self,
        db: aiosqlite.Connection,
        login_schema: LoginSchema,
    ):
        user = await self.authenticate_user(
            db=db,
            email=login_schema.email,
            password=login_schema.password,
        )
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        if not user.is_active:
            await self.repository.set_user_active(user_id=user.id, db=db)
        token = sign_jwt(user_id=user.id)
        return JSONResponse(
            content={"access_token": token, "token_type": "bearer"},
            status_code=200,
        )

    async def register_user(
        self,
        db: aiosqlite.Connection,
        register_schema: RegisterSchema,
    ) -> Optional[JSONResponse]:
        if await self.repository.get_user_by_email(db=db, email=register_schema.email):
            raise HTTPException(status_code=400, detail="User already exists")
        user = await self.repository.create_user(
            db=db,
            user_schema=UserCreateSchema(
                username=register_schema.username,
                email=register_schema.email,
                password=register_schema.password,
            ),
        )
        if not user:
            raise HTTPException(status_code=400, detail="Failed to create user")
        return JSONResponse(
            content={"detail": "User created successfully"},
            status_code=201,
        )
