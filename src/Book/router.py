from cmath import inf
from typing import Union, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from Book.models import Book, Genre, BookGenre
from Book.schemas import BookRead, BookCreate, BookUpdate, BookDelete, GenreRead, GenreCreate, GenreUpdate, GenreDelete
from User.models import User
from database import get_async_session

router = APIRouter(
    prefix="/book",
    tags=["book"]
)


@router.get("/genre/{genre_id}", response_model=Union[GenreRead, None])
async def read_genre(genre_id: int, session=Depends(get_async_session)) -> Union[GenreRead, None]:
    query = select(Genre).where(Genre.id == genre_id)
    genre = await session.execute(query)
    genre = genre.fetchone()
    if not genre:
        return
    genre_read = GenreRead.from_orm(genre[0])
    return genre_read


@router.post("/genre", response_model=Union[GenreRead, None])
async def create_genre(genre: GenreCreate, session=Depends(get_async_session)) -> Union[GenreRead, None]:
    new_genre = Genre(**genre.dict())
    session.add(new_genre)
    await session.commit()
    return GenreRead.from_orm(new_genre)


@router.put("/genre", response_model=Union[GenreRead, None])
async def update_genre(genre: GenreUpdate, session=Depends(get_async_session)) -> Union[GenreRead, None]:
    query = select(Genre).where(Genre.id == genre.id)
    current_genre = await session.execute(query)
    current_genre = current_genre.scalar()
    if current_genre:
        genre_data = genre.dict(exclude_unset=True)
        for key, value in genre_data.items():
            if value:
                setattr(genre_data, key, value)
        await session.commit()
        return GenreRead.from_orm(current_genre)
    return None


@router.delete("/genre")
async def delete_genre(genre: GenreDelete, session=Depends(get_async_session)) -> dict:
    query = delete(Genre).where(Genre.id == genre.id)
    await session.execute(query)
    await session.commit()
    return {"detail": f"User {genre.id} deleted"}


@router.get("/{book_id}", response_model=Union[BookRead, None])
async def read_book(book_id: int, session=Depends(get_async_session)) -> Union[BookRead, None]:
    query = select(Book).where(User.id == book_id)
    book = await session.execute(query)
    book = book.fetchone()
    if not book:
        return
    return BookRead.from_orm(book[0])


@router.post("/")
async def create_book(book: BookCreate, session: AsyncSession = Depends(get_async_session)) -> dict:
    genre_names = [genre.name for genre in book.genres]
    genres = (await session.execute(select(Genre).where(Genre.name.in_(genre_names)))).scalars().all()
    new_book = Book(name=book.name, page_count=book.page_count, price=book.price, author_id=book.author_id)
    new_book.genres = genres
    session.add(new_book)
    await session.commit()
    return {"status": 200,
            "details": {
                "id": new_book.id,
                "name": new_book.name,
                "page_count": new_book.page_count,
                "author id": new_book.author_id,
                "genres": [genre.name for genre in new_book.genres], }}


@router.put("/")
async def update_book(book: BookUpdate, session: AsyncSession = Depends(get_async_session)) -> dict:
    query = select(Book).where(Book.id == book.id)
    genre_names = [genre.name for genre in book.genres]
    genres = (await session.execute(select(Genre).where(Genre.name.in_(genre_names)))).scalars().all()
    current_book = await session.execute(query)
    current_book = current_book.scalar()
    if current_book:
        book_data = book.dict(exclude_unset=True)
        for key, value in book_data.items():
            if value:
                if key == "genres":
                    value = genres
                setattr(current_book, key, value)
        await session.commit()
        return {"status": 200,
                "details": {
                    "id": current_book.id,
                    "name": current_book.name,
                    "page_count": current_book.page_count,
                    "author id": current_book.author_id,
                    "genres": [genre.name for genre in current_book.genres], }}

    return {"status": "200",
            "details": {}}


@router.delete("/")
async def delete_book(book: BookDelete, session=Depends(get_async_session)) -> dict:
    query = delete(Book).where(Book.id == book.id)
    await session.execute(query)
    await session.commit()
    return {"detail": f"Book {book.id} deleted"}


@router.get("/")
async def book_filter(
        price_from: int = Query(0, ge=0),
        price_to: int = Query(inf, gt=0),
        genres: List[int] = Query([]),
        authors: List[int] = Query([]),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    if not genres:
        genre_ids = (await session.execute(select(Genre.id))).scalars().all()
    else:
        genre_ids = genres

    if not authors:
        author_ids = (await session.execute(select(User.id))).scalars().all()
    else:
        author_ids = authors

    query = select(Book).join(BookGenre).join(Genre).where(
        Book.price >= price_from,
        Book.price <= price_to,
        Genre.id.in_(genre_ids),
        Book.author_id.in_(author_ids)
    ).group_by(Book.id)

    books = (await session.execute(query)).scalars().all()
    return {"status": 200,
            "details": books}
