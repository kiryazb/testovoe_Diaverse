from datetime import date
from typing import Literal
from typing import get_args

from sqlalchemy import Integer, String, ForeignKey, Enum, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from Book.models import Book
from User.models import User


class Base(DeclarativeBase):
    pass


class ReservationBook(Base):
    __tablename__ = "reservation_book"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey(Book.id), nullable=False)
    date_from: Mapped[date] = mapped_column(Date, nullable=False)
    date_to: Mapped[date] = mapped_column(Date, nullable=False)
