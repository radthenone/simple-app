import pydantic
from pydantic import ConfigDict, EmailStr


class LoginSchema(pydantic.BaseModel):
    email: str
    password: str

    model_config = ConfigDict(
        title="User Model",
        json_schema_extra={
            "example": {
                "email": "john@example.com",
                "password": "secure_password",
            }
        },
    )


class RegisterSchema(pydantic.BaseModel):
    username: str
    password: str
    email: EmailStr

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


class TokenResponse(pydantic.BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        title="Token Model",
        json_schema_extra={
            "example": {
                "access_token": "token",
                "token_type": "bearer",
            }
        },
    )
