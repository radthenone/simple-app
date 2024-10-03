import time
from typing import Dict, Optional

import bcrypt
import jwt
from config import settings
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.requests import Request
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from typing_extensions import Annotated


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def sign_jwt(user_id: int) -> str:
    payload = {"user_id": user_id, "expires": time.time() + 600}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    return token


def decode_jwt(token: str) -> Optional[dict]:
    try:
        decoded_token = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials.")


security = HTTPBearer()


def jwt_token(token: HTTPAuthorizationCredentials = Depends(security)):
    token_str = token.credentials
    token = decode_jwt(token_str)
    if token:
        return token

    raise HTTPException(status_code=401, detail="Invalid token")


def jwt_valid(token: Annotated[Dict, Depends(jwt_token)]) -> bool:
    if token:
        return True
    return False


def jwt_user_id(token: Annotated[Dict, Depends(jwt_token)]) -> Optional[int]:
    return token.get("user_id")
