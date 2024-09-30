import logging
from logging.config import dictConfig

from backend.db import init_db, get_db
from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.logger import LogConfig

from backend.apps.users.router import users_router

dictConfig(LogConfig().model_dump())
logger = logging.getLogger('mycoolapp')

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info('Starting up...')
    db = await get_db()
    await init_db(db)
    yield
    await db.close()
    logging.info('Shutting down...')

app = FastAPI(debug=True)
app.lifespan = lifespan


@app.get("/")
async def read_root():
    return {"Hello": "World"}
app.include_router(users_router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host='0.0.0.0', port=8000, log_level="info", reload=True)

