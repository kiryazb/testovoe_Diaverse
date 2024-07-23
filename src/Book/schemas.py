from pydantic import BaseModel
from typing import List, Literal, Optional

GenreEnum = Literal["Romance", "Fantasy", "Science Fiction", "Mystery", "Horror"]


class Genre(BaseModel):
    name: GenreEnum


class GenreCreate(Genre):
    pass


class GenreRead(Genre):
    pass

    class Config:
        orm_mode = True
        from_attributes = True


class GenreUpdate(Genre):
    pass


class GenreDelete(Genre):
    pass


class Book(BaseModel):
    id: int
    name: str
    page_count: int
    author_id: int
    genres: List[Genre]


class BookCreate(Book):
    pass


class BookRead(Book):
    genres: List[Genre] = []

    class Config:
        orm_mode = True
        from_attributes = True


class BookUpdate(Book):
    name: Optional[str] = None
    page_count: Optional[int] = None
    author_id: Optional[int] = None
    genres: Optional[List[Genre]] = None


class BookDelete(Book):
    pass
