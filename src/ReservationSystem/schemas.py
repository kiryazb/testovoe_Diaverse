from datetime import date
from typing import Optional

from pydantic import BaseModel


class Reservation(BaseModel):
    id: int
    user_id: int
    book_id: int
    date_from: date
    date_to: date


class ReservationCreate(Reservation):
    pass


class ReservationUpdate(Reservation):
    id: int
    user_id: Optional[int] = None
    book_id: Optional[int] = None
    date_from: Optional[int] = None
    date_to: Optional[date]
