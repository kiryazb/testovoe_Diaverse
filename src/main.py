from fastapi import FastAPI

from User.router import router as user_router
from Book.router import router as book_router
from ReservationSystem.router import router as reservation_router

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
