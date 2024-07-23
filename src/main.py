from fastapi import FastAPI

from User.router import router as user_router
from Book.router import router as book_router
from ReservationSystem.router import router as reservation_router

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from config import REDIS_HOST, REDIS_PORT

app = FastAPI()

app.include_router(
    user_router,
)

app.include_router(
    book_router
)

app.include_router(
    reservation_router
)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(F"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
