import logging
from typing import Annotated

import aiosqlite
from db import get_db
from fastapi import APIRouter, Depends

from apps.auth.handler import jwt_user_id, jwt_valid
from apps.common.schema import ErrorResponse
from apps.users.repository import UserRepository
from apps.users.schema import (
    UserModel,
    UserResponse,
    UserSchema,
    UserUpdateSchema,
)
from apps.users.service import UserService

logs = logging.getLogger("simple-debug")

users_router = APIRouter(
    prefix="/users",
)
users_repository = UserRepository()
users_service = UserService(repository=users_repository)


@users_router.get(
    "/account",
    responses={
        200: {
            "model": UserSchema,
        },
        404: {
            "model": ErrorResponse,
            "description": "User not found",
            "content": {
                "application/json": {
                    "examples": {
                        "user_not_found": {
                            "summary": "User not found",
                            "value": {
                                "detail": "User not found",
                                "status_code": 404,
                            },
                        }
                    }
                }
            },
        },
    },
)
async def get_user(
    user_id: Annotated[int, Depends(jwt_user_id)],
    db: Annotated[aiosqlite.Connection, Depends(get_db)],
):
    return await users_service.get_user(db=db, user_id=user_id)


@users_router.put(
    "/account",
    responses={
        201: {
            "model": UserModel,
        },
        400: {
            "model": ErrorResponse,
            "description": "User already exists",
            "content": {
                "application/json": {
                    "examples": {
                        "user_already_exists": {
                            "summary": "User already exists",
                            "value": {
                                "detail": "User already exists",
                                "status_code": 400,
                            },
                        }
                    }
                }
            },
        },
    },
)
async def update_user(
    user_update: UserUpdateSchema,
    user_id: Annotated[int, Depends(jwt_user_id)],
    db: Annotated[aiosqlite.Connection, Depends(get_db)],
):
    return await users_service.update_user(
        db=db, user_id=user_id, user_update=user_update
    )


@users_router.delete(
    "/account",
    responses={
        201: {
            "model": UserResponse,
            "description": "User deleted",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User deleted",
                        "status_code": 201,
                    }
                }
            },
        },
        404: {
            "model": ErrorResponse,
            "description": "User not found",
            "content": {
                "application/json": {
                    "examples": {
                        "user_not_found": {
                            "summary": "User not found",
                            "value": {
                                "detail": "User not found",
                                "status_code": 404,
                            },
                        }
                    }
                }
            },
        },
    },
)
async def delete_user(
    user_id: Annotated[int, Depends(jwt_user_id)],
    db: Annotated[aiosqlite.Connection, Depends(get_db)],
):
    return await users_service.delete_user(db=db, user_id=user_id)


@users_router.get(
    "/all",
    dependencies=[Depends(jwt_valid)],
    responses={
        200: {
            "model": list[UserSchema],
        },
        404: {
            "model": ErrorResponse,
            "description": "Users not found",
            "content": {
                "application/json": {
                    "examples": {
                        "users_not_found": {
                            "summary": "Users not found",
                            "value": {
                                "detail": "Users not found",
                                "status_code": 404,
                            },
                        }
                    }
                }
            },
        },
    },
)
async def get_users(
    db: Annotated[aiosqlite.Connection, Depends(get_db)],
):
    return await users_service.get_users(db=db)
