import logging
from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.auth.router import auth_router
from apps.users.router import users_router
from db import get_db, init_db
from logger import LogConfig

dictConfig(LogConfig().model_dump())
logger = logging.getLogger("simple-debug")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting up...")
    db = await get_db()
    await init_db(db)
    yield
    await db.close()
    logging.info("Shutting down...")


app = FastAPI(debug=True)
app.lifespan = lifespan

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, tags=["Auth"])
app.include_router(users_router, tags=["Users"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
