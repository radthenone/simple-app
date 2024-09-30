import logging

import aiosqlite
from apps.users.schema import User
from backend.apps.users.db import (
    create_user as create_user_from_db,
)
from backend.apps.users.db import (
    exists_user as exists_user_from_db,
)
from backend.apps.users.db import (
    get_user as get_user_from_db,
)
from backend.db import get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

logs = logging.getLogger("mycoolapp")

users_router = APIRouter(
    prefix="/users",
)


@users_router.get("/{user_id}")
async def get_user(user_id: int, db: aiosqlite.Connection = Depends(get_db)):
    user_db = await get_user_from_db(db, user_id)
    if user_db:
        logs.info(user_db.model_dump())
        return JSONResponse(content=user_db.model_dump(), status_code=200)
    return HTTPException(status_code=404, detail="User not found")


@users_router.post("/create")
async def create_user(user: User, db: aiosqlite.Connection = Depends(get_db)):
    if await exists_user_from_db(db, user.email):
        logging.error("User already exists")
        return HTTPException(status_code=400, detail="User already exists")
    user_db = await create_user_from_db(db, user)
    if user_db is None:
        logging.error("Failed to create user: user_db is None")
        return JSONResponse(content="Failed to create user", status_code=400)
    else:
        logging.info(f"User created: {user_db.model_dump()}")

        return JSONResponse(
            content=user_db.model_dump(
                exclude={"is_active", "is_admin", "created_at", "updated_at"}
            ),
            status_code=200,
        )
