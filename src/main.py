from fastapi import FastAPI

from User.router import router as user_router

app = FastAPI()

app.include_router(
    user_router,
)
