from datetime import datetime
from typing import Optional

import pydantic
from pydantic import ConfigDict, EmailStr


class UserModel(pydantic.BaseModel):
    id: Optional[int] = None
    username: str
    password: str
    email: EmailStr
    is_active: bool = False
    is_admin: bool = False
    created_at: str = datetime.now().isoformat()
    updated_at: Optional[str] = None


class UserSchema(pydantic.BaseModel):
    username: str
    email: EmailStr
    is_active: bool = False


class UserCreateSchema(pydantic.BaseModel):
    username: str
    password: str
    email: EmailStr
    is_active: bool = False
    is_admin: bool = False
    created_at: str = datetime.now().isoformat()
    updated_at: Optional[str] = None

    model_config = ConfigDict(
        title="User Model",
        json_schema_extra={
            "example": {
                "username": "john_doe",
                "password": "secure_password",
                "email": "john@example.com",
            }
        },
    )


class UserUpdateSchema(pydantic.BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    updated_at: str = datetime.now().isoformat()

    model_config = ConfigDict(
        title="User Model",
        json_schema_extra={
            "example": {
                "username": "john_doe",
                "password": "secure_password",
                "email": "john@example.com",
            }
        },
    )


class UserResponse(pydantic.BaseModel):
    username: str
    email: EmailStr
    is_active: bool
