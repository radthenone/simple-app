import logging
from typing import Annotated

import aiosqlite
from db import get_db
from fastapi import APIRouter, Depends

from apps.auth.schema import LoginSchema, RegisterSchema
from apps.auth.service import AuthService
from apps.common.schema import ErrorResponse, SuccessResponse
from apps.users.repository import UserRepository

logs = logging.getLogger("simple-debug")

auth_router = APIRouter(
    prefix="/auth",
)
users_repository = UserRepository()
auth_service = AuthService(repository=users_repository)


@auth_router.post(
    "/register",
    responses={
        200: {
            "model": SuccessResponse,
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User created successfully",
                    }
                }
            },
        },
        400: {
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "examples": {
                        "user_exists": {
                            "summary": "User already exists",
                            "value": {"detail": "User already exists"},
                        },
                        "creation_failed": {
                            "summary": "Failed to create user",
                            "value": {"detail": "Failed to create user"},
                        },
                    }
                }
            },
        },
    },
)
async def register_user(
    register_schema: RegisterSchema,
    db: Annotated[aiosqlite.Connection, Depends(get_db)],
):
    return await auth_service.register_user(db, register_schema)


@auth_router.post(
    "/login",
    responses={
        200: {
            "model": SuccessResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "User logged in successfully"}
                }
            },
        },
        400: {
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_credentials": {
                            "summary": "Invalid email or password",
                            "value": {"detail": "Invalid email or password"},
                        },
                        "user_not_found": {
                            "summary": "User not found",
                            "value": {"detail": "User not found"},
                        },
                        "login_failed": {
                            "summary": "Failed to login user",
                            "value": {"detail": "Failed to login user"},
                        },
                    }
                }
            },
        },
    },
)
async def login_user(
    login_schema: LoginSchema,
    db: Annotated[aiosqlite.Connection, Depends(get_db)],
):
    return await auth_service.login_user(db, login_schema)
