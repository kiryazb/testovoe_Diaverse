from typing import Literal
from typing import get_args

from sqlalchemy import Integer, String, ForeignKey, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from User.models import User

GenreEnum = Literal["Romance", "Fantasy", "Science Fiction", "Mystery", "Horror"]


class Base(DeclarativeBase):
    pass


class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[GenreEnum] = mapped_column(
        Enum(
            *get_args(GenreEnum),
            name="genre_enum"),
        nullable=False)


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    page_count: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id))

    genres = relationship(Genre, secondary="book_genre", backref="books", lazy='selectin')


class BookGenre(Base):
    __tablename__ = "book_genre"

    book_id: Mapped[int] = mapped_column(Integer, ForeignKey(Book.id), primary_key=True)
    id: Mapped[int] = mapped_column(Integer, ForeignKey(Genre.id), primary_key=True)
